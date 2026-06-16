"""
slideless — validador determinístico

Roda regex/DOM checks sobre o HTML gerado SEM precisar de LLM. Cobre um
subconjunto dos anti-patterns (references/anti-patterns.md) que pode ser
detectado sintaticamente. O resto (tom editorial, semântica de cor etc.)
fica para /auditar (LLM).

Stdlib only — sem beautifulsoup, sem playwright.

Uso:
    python validar.py <arquivo.html>
    python validar.py <arquivo.html> --quick      # só identifica modelo
    python validar.py <arquivo.html> --strict     # warnings viram erros
    python validar.py <arquivo.html> --json       # saída JSON
    python validar.py <pasta> --stats             # telemetria do pool: tabula os eixos do parti

Exit code: 0 se sem erros, 1 se houver pelo menos um erro.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import List, Optional

SEVERITY_ERROR = "error"
SEVERITY_WARN = "warn"
SEVERITY_INFO = "info"

# Tokens semânticos que precisam de override em [data-theme="dark"]
REQUIRED_DARK_OVERRIDES = [
    "--color-bg",
    "--color-bg-elevated",
    "--color-bg-sunken",
    "--color-fg",
    "--color-fg-muted",
    "--color-fg-subtle",
    "--color-border",
    "--color-border-strong",
    "--color-accent",
]

# ─── Categoria P (Pasteurização / AI-tells) — v4 ─────────────────────────
# Fontes-assinatura de IA (1ª e 2ª geração). Ver references/type-kits.md.
BANNED_FONTS = [
    "Space Grotesk", "Instrument Serif", "Syne", "Geist", "Poppins",
    "Montserrat", "Bebas Neue", "Playfair Display",
]

# Vocabulário fechado do campo nao-vai-ter (references/direcao-de-arte.md §8).
# feature declarada → regex que NÃO pode casar no HTML.
# Regex refinadas para EVITAR falso positivo (validador sem credibilidade é ignorado):
# - em-italico-accent só dispara com cor NÃO-neutra (color:inherit é a neutralização correta)
# - kicker-dot exige ::before CIRCULAR (fio lateral 2px é a alternativa recomendada, não o tell)
# - badge-pill exige seletor de badge/pill/tag/chip (999px no theme-toggle é chrome legítimo)
# Comentários CSS/HTML são removidos antes do match (ver _scrub) — um tell citado num
# comentário explicativo não é o tell presente no documento.
NAO_VAI_TER_REGEX = {
    "glow-radial":          r"body::(?:before|after)[^{]*\{[^}]*radial-gradient|--glow-(?:warm|cool|hero)\s*:",
    "kicker-dot":           r"\.kicker[^{]*::before\s*\{[^}]*border-radius\s*:\s*(?:50%|9{3,})|\.kicker__dot|class=\"[^\"]*kicker[^\"]*dot",
    "hover-lift":           r":hover[^}]*translateY\(\s*-",
    "grid-3-cards":         r"repeat\(\s*3\s*,\s*(?:minmax\([^)]*\)|1fr)\s*\)",
    "em-italico-accent":    r"(?:h[1-6]|\.title[\w-]*)\s+em\s*\{[^}]*color\s*:\s*(?!inherit|currentcolor|unset|initial)[^;\s]",
    "gradient-text":        r"background-clip:\s*text|-webkit-background-clip:\s*text",
    "glassmorphism":        r"backdrop-filter:\s*blur",
    "card-com-filete":      r"\.(?:card|ve-card)[^{]*\{[^}]*border-(?:left|top):\s*[3-9]px\s+solid\s+var\(--color-",
    "stagger-linear":       r"calc\(\s*var\(\s*--i\b[^)]*\)\s*\*",
    "counter-animado":      r"(?:animateCount|countUp|counter\s*\()",
    "timeline-dot":         r"\.timeline__dot",
    "badge-pill":           r"\.(?:badge|pill|tag|chip)[\w-]*[^{]*\{[^}]*border-radius\s*:\s*9{3,}",
    "sombra-difusa-em-tudo": r"box-shadow:\s*0\s+\d+px\s+\d+px",  # heurística: checada por contagem
    "fade-up":              r"opacity:\s*0\s*;[^}]*translateY\(\s*\d|translateY\(\s*\d+px\s*\)\s*;[^}]*opacity:\s*0",
    "divider-laranja":      r'data-background-color="var\(--itau-orange\)"',
    # Renúncias de AMBIÇÃO (v5) — features de A2-cheio/A3 que um documento sóbrio declara não ter.
    # NÃO incluir "glass"/"glassmorphism" aqui no sentido de backdrop-filter, pois o topbar usa
    # blur legítimo (chrome); a renúncia a vidro-de-painel decorativo já é coberta por glassmorphism.
    "aurora":               r"\.aurora\b",
    "aurora-saturada":      r"\.aurora\b",
    "webgl":                r"getContext\(\s*['\"]webgl|new\s+Gradient\s*\(",
    "conic-glow":           r"conic-gradient|@property\s+--ang\b",
    "cursor-proximity":     r"pointermove[\s\S]{0,400}(?:fontVariationSettings|font-variation-settings)",
    "spring-bouncy":        r"linear\(\s*0[^)]*1\.[1-9]|cubic-bezier\([^)]*,\s*1\.[5-9]\d*\s*,",
}

# Títulos-categoria banidos como h2 (headline deve ser tese, não rótulo)
BANNED_H2 = [
    "visão geral", "visao geral", "principais destaques", "destaques",
    "próximos passos", "proximos passos", "conclusão", "conclusao",
    "introdução", "introducao", "contexto", "sobre",
]

# Léxico verbal de IA pt-BR (warn — falso positivo possível)
AI_WORDLIST = [
    "robusto", "robusta", "alavancar", "alavanque", "seamless",
    "é importante ressaltar", "vale destacar", "nesse sentido",
    "cenário desafiador", "desbloquear todo o potencial", "mergulhar fundo",
    "panorama completo", "revolucione", "supercharge",
]


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    line: Optional[int] = None

    def fmt(self) -> str:
        loc = f"[line {self.line}]" if self.line is not None else "[--]"
        return f"{self._badge()} {self.code} {loc} {self.message}"

    def _badge(self) -> str:
        return {
            SEVERITY_ERROR: "ERROR",
            SEVERITY_WARN: "WARN ",
            SEVERITY_INFO: "INFO ",
        }[self.severity]


@dataclass
class Report:
    file: str
    model: Optional[str]
    theme: Optional[str]
    issues: List[Issue] = field(default_factory=list)

    @property
    def errors(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == SEVERITY_ERROR]

    @property
    def warnings(self) -> List[Issue]:
        return [i for i in self.issues if i.severity == SEVERITY_WARN]

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "model": self.model,
            "theme": self.theme,
            "issues": [asdict(i) for i in self.issues],
            "ok": len(self.errors) == 0,
        }


def _line_of(html: str, pos: int) -> int:
    return html.count("\n", 0, pos) + 1


def _find(html: str, pattern: str, flags: int = 0) -> Optional[re.Match]:
    return re.search(pattern, html, flags)


def identify_model(html: str) -> Optional[str]:
    """Detecta o modelo lendo classes/elementos raiz.

    Heurística tolerante: aceita variações de naming entre templates novos e
    exemplos legacy (e.g., 'class="scrolly"' vs 'class="scrollytelling"',
    'view is-active' vs 'view data-view').
    """
    # Deck — múltiplos slides em sequência com data-slide
    if re.search(r'<section\s+class="slide"[^>]*data-slide=', html):
        return "deck"
    if re.search(r'<div\s+class="deck"\b', html):
        return "deck"
    # Handbook — sidebar + (toc OU content__inner)
    if re.search(r'<aside\s+class="sidebar"', html):
        return "handbook"
    # Site — vários <article class="view"> + hash routing
    if re.search(r'<article\s+class="view\b', html) and re.search(r'(hashchange|topnav|topbar__nav)', html):
        return "site"
    # Hub — grid + filter chips
    if re.search(r'class="(?:filters|filter)\b', html) and re.search(r'class="grid"', html):
        return "hub"
    # Scrollytelling — várias seções com data-reveal + progress bar
    if re.search(r'class="progress"', html) or re.search(r'id="progress(?:-bar)?"', html):
        if re.search(r'data-reveal', html):
            return "scrollytelling"
    if re.search(r'class="scrolly"', html) or re.search(r'class="scene\b', html):
        return "scrollytelling"
    return None


def identify_theme(html: str) -> Optional[str]:
    if re.search(r'--itau-orange\s*:', html):
        return "itau"
    if re.search(r'#2563eb|#60a5fa', html) and re.search(r'--color-accent\s*:', html):
        return "neutro"
    return None


# ─── Checks ──────────────────────────────────────────────────────────────


def check_boot_script(html: str, report: Report) -> None:
    """B2: boot script de tema antes do CSS pintar."""
    head_m = _find(html, r"<head[^>]*>(.*?)</head>", re.DOTALL | re.IGNORECASE)
    if not head_m:
        report.issues.append(Issue(SEVERITY_ERROR, "B2-no-head", "<head> não encontrado"))
        return
    head = head_m.group(1)
    # Primeiro <script> dentro do <head>
    first_script = _find(head, r"<script[^>]*>([\s\S]*?)</script>", re.IGNORECASE)
    if not first_script:
        report.issues.append(Issue(SEVERITY_ERROR, "B2-boot-missing",
            "Boot script de tema ausente. Adicionar localStorage.getItem('theme') no primeiro <script> do <head>",
            _line_of(html, head_m.start())))
        return
    if "localStorage" not in first_script.group(1) or "data-theme" not in first_script.group(1):
        report.issues.append(Issue(SEVERITY_ERROR, "B2-boot-incomplete",
            "Boot script não chama localStorage.getItem('theme') ou não seta document.documentElement[data-theme]",
            _line_of(html, head_m.start() + first_script.start())))


def check_dark_overrides(html: str, report: Report) -> None:
    """B4: [data-theme="dark"] deve sobrescrever todos os tokens semânticos."""
    root_m = _find(html, r":root\s*\{([\s\S]*?)\}", re.MULTILINE)
    dark_m = _find(html, r'\[data-theme="dark"\]\s*\{([\s\S]*?)\}', re.MULTILINE)
    if not root_m:
        report.issues.append(Issue(SEVERITY_ERROR, "B4-no-root", ":root { ... } não encontrado"))
        return
    if not dark_m:
        report.issues.append(Issue(SEVERITY_ERROR, "B4-no-dark", '[data-theme="dark"] { ... } não encontrado'))
        return

    root_tokens = set(re.findall(r"(--[\w-]+)\s*:", root_m.group(1)))
    dark_tokens = set(re.findall(r"(--[\w-]+)\s*:", dark_m.group(1)))

    for tok in REQUIRED_DARK_OVERRIDES:
        if tok in root_tokens and tok not in dark_tokens:
            report.issues.append(Issue(SEVERITY_ERROR, "B4-missing-override",
                f'Token {tok} definido em :root mas sem override em [data-theme="dark"]',
                _line_of(html, dark_m.start())))


def check_reduced_motion(html: str, report: Report) -> None:
    """B5: presença de @media (prefers-reduced-motion: reduce)."""
    if not re.search(r"prefers-reduced-motion\s*:\s*reduce", html):
        report.issues.append(Issue(SEVERITY_ERROR, "B5-no-reduced-motion",
            "Sem @media (prefers-reduced-motion: reduce). Animações vão rodar mesmo para usuários que desativaram."))


def check_focus_visible(html: str, report: Report) -> None:
    """B6: foco visível."""
    if not re.search(r":focus-visible", html):
        report.issues.append(Issue(SEVERITY_WARN, "B6-no-focus-visible",
            "Sem regra :focus-visible no CSS. Foco de teclado pode estar invisível."))
    if re.search(r"\boutline\s*:\s*none\b(?!\s*[;)]?\s*(?:/\*|\}))", html):
        # Heurística — outline: none sem ser dentro de uma regra que define alternativa
        report.issues.append(Issue(SEVERITY_WARN, "B6-outline-none",
            "outline: none detectado. Garantir que :focus-visible reintroduz outline."))


def check_keyboard_deck(html: str, report: Report) -> None:
    """B7: deck precisa de keyboard handler."""
    if not re.search(r"addEventListener\(\s*['\"]keydown['\"]", html):
        report.issues.append(Issue(SEVERITY_ERROR, "B7-no-keydown",
            "Deck sem handler de 'keydown'. Setas/Space/Esc não vão funcionar."))
        return
    if not re.search(r"ArrowRight", html):
        report.issues.append(Issue(SEVERITY_ERROR, "B7-no-arrow",
            "Keyboard handler não trata 'ArrowRight' explicitamente."))


def check_single_file(html: str, report: Report) -> None:
    """B1: zero <link rel=stylesheet> ou <script src> para arquivos locais."""
    for m in re.finditer(r'<link[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']', html, re.IGNORECASE):
        href = m.group(1)
        if not href.startswith(("http://", "https://", "data:")):
            report.issues.append(Issue(SEVERITY_ERROR, "B1-external-css",
                f'<link rel=stylesheet> aponta para arquivo local: "{href}". Documento single-file não permite isso.',
                _line_of(html, m.start())))
    for m in re.finditer(r'<script[^>]*src=["\']([^"\']+)["\']', html, re.IGNORECASE):
        src = m.group(1)
        if not src.startswith(("http://", "https://", "data:")):
            report.issues.append(Issue(SEVERITY_ERROR, "B1-external-js",
                f'<script src> aponta para arquivo local: "{src}". Documento single-file não permite isso.',
                _line_of(html, m.start())))


def check_huge_typography_outside_deck(html: str, report: Report, model: Optional[str]) -> None:
    """A1: tipografia ≥ 4rem fora do deck."""
    if model == "deck":
        return  # OK no deck
    # Procurar font-size: Xrem onde X >= 4, mas IGNORAR dentro de clamp(...) e dentro de blocos não-CSS
    # Heurística: procurar em <style> blocks
    for style_m in re.finditer(r"<style[^>]*>([\s\S]*?)</style>", html, re.IGNORECASE):
        css = style_m.group(1)
        css_offset = style_m.start(1)
        # Remover ocorrências dentro de clamp() para não dar falso positivo
        css_no_clamp = re.sub(r"clamp\([^)]*\)", "CLAMP", css)
        for m in re.finditer(r"font-size\s*:\s*([\d.]+)rem", css_no_clamp):
            val = float(m.group(1))
            if val >= 4.0:
                # Achar posição original aproximada
                # Como removemos clamp(), offsets ficam imprecisos — usa o início do <style>
                report.issues.append(Issue(SEVERITY_ERROR, "A1-huge-typography",
                    f"font-size: {val}rem fora do modelo `deck` ({model or 'desconhecido'}). Tipografia gigante é proibida — só permitida em .slide do deck.",
                    _line_of(html, css_offset)))


def check_lang_attribute(html: str, report: Report) -> None:
    if not re.search(r'<html[^>]+lang\s*=\s*["\'][^"\']+["\']', html, re.IGNORECASE):
        report.issues.append(Issue(SEVERITY_WARN, "B8-no-lang",
            'Falta atributo `lang` no <html>. Recomendado lang="pt-BR".'))


def check_meta_viewport(html: str, report: Report) -> None:
    if not re.search(r'<meta[^>]+name=["\']viewport["\']', html, re.IGNORECASE):
        report.issues.append(Issue(SEVERITY_WARN, "B8-no-viewport",
            "Falta <meta name=\"viewport\">. Recomendado para responsividade."))


def check_handbook_sidebar(html: str, report: Report) -> None:
    if not re.search(r'<aside\s+class="sidebar"', html):
        report.issues.append(Issue(SEVERITY_ERROR, "D-handbook-no-sidebar",
            "Modelo handbook sem <aside class=\"sidebar\">. Sidebar é obrigatória."))
    if not re.search(r'IntersectionObserver', html):
        report.issues.append(Issue(SEVERITY_WARN, "D-handbook-no-spy",
            "Modelo handbook sem IntersectionObserver para scrollspy. Sidebar não atualizará ao rolar."))


def check_site_hash_routing(html: str, report: Report) -> None:
    if not re.search(r"hashchange", html):
        report.issues.append(Issue(SEVERITY_ERROR, "D-site-no-hash",
            "Modelo site sem listener de hashchange. Hash routing não funciona."))
    # Views não-ativas devem ter atributo hidden — checar fora de comentários HTML
    html_no_comments = re.sub(r"<!--[\s\S]*?-->", "", html)
    for m in re.finditer(r'<article\s+[^>]*class="view\b[^"]*"[^>]*>', html_no_comments):
        tag = m.group(0)
        if "is-active" in tag or "hidden" in tag:
            continue
        report.issues.append(Issue(SEVERITY_WARN, "D-site-view-no-hidden",
            "View não-ativa sem atributo `hidden`. Pode ser visível pra screen readers."))


def check_scrollytelling_progress(html: str, report: Report) -> None:
    if not re.search(r"progress(?:__bar|-bar)", html, re.IGNORECASE):
        report.issues.append(Issue(SEVERITY_WARN, "D-scrolly-no-progress",
            "Modelo scrollytelling sem progress bar. Característico do modelo."))


def check_hex_outside_root(html: str, report: Report) -> None:
    """B3: hex fora de :root / [data-theme] / --itau-*."""
    style_blocks = list(re.finditer(r"<style[^>]*>([\s\S]*?)</style>", html, re.IGNORECASE))
    if not style_blocks:
        return
    for sb in style_blocks:
        css = sb.group(1)
        # Remover :root { ... } e [data-theme=*] { ... }
        css_clean = re.sub(r":root\s*\{[^{}]*\}", "", css)
        css_clean = re.sub(r'\[data-theme="[^"]+"\]\s*\{[^{}]*\}', "", css_clean)
        # Remover comentários
        css_clean = re.sub(r"/\*[\s\S]*?\*/", "", css_clean)
        # Procurar hex
        for m in re.finditer(r"#[0-9a-fA-F]{3,8}\b", css_clean):
            hex_val = m.group(0)
            # Permitir alguns hex bem específicos (sombras com rgba, raros)
            if len(hex_val) in (4, 7, 9):  # #fff, #ffffff, #ffffff00
                report.issues.append(Issue(SEVERITY_WARN, "B3-hex-outside-root",
                    f"Cor hex `{hex_val}` fora de :root / [data-theme]. Use var(--color-*).",
                    _line_of(html, sb.start(1))))
                # Evitar spam: só reportar uma ocorrência por style block
                break


# ─── Categoria P — Pasteurização / AI-tells (v4) ─────────────────────────


PARTI_RE = re.compile(r"<!--\s*slideless:parti([\s\S]*?)-->", re.IGNORECASE)


def parse_parti(html: str) -> Optional[dict]:
    """Extrai o bloco <!-- slideless:parti --> como dict chave→valor."""
    m = PARTI_RE.search(html)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if ":" in line and not line.startswith(("http", "//")):
            k, _, v = line.partition(":")
            k = k.strip().lower()
            if re.fullmatch(r"[\w-]+", k):
                fields[k] = v.strip()
    return fields or None


def _strip_tags(html: str) -> str:
    body = re.sub(r"<(script|style)[^>]*>[\s\S]*?</\1>", " ", html, flags=re.IGNORECASE)
    body = re.sub(r"<!--[\s\S]*?-->", " ", body)
    return re.sub(r"<[^>]+>", " ", body)


def _scrub(html: str) -> str:
    """Remove comentários CSS e HTML antes dos checks de padrão. Um tell citado
    num comentário explicativo ('/* nunca transition:all */') não é o tell
    presente no documento — sem isso o validador gera falso positivo e perde
    credibilidade. O bloco parti é parseado à parte (parse_parti no html bruto)."""
    html = re.sub(r"/\*[\s\S]*?\*/", " ", html)
    html = re.sub(r"<!--[\s\S]*?-->", " ", html)
    return html


def check_parti_block(html: str, report: Report) -> None:
    """P0: bloco parti obrigatório, com as 7 decisões (incl. ambicao) + nao-vai-ter."""
    parti = parse_parti(html)
    if parti is None:
        report.issues.append(Issue(SEVERITY_ERROR, "P0-no-parti",
            "Bloco <!-- slideless:parti --> ausente no documento. Nenhum HTML antes do parti "
            "(references/direcao-de-arte.md). Documentos pré-v4 são legado — regenerar ou anotar."))
        return
    required = ["registro", "kit", "capa", "superficie", "motion", "ambicao", "assinatura", "nao-vai-ter"]
    missing = [f for f in required if f not in parti]
    if missing:
        report.issues.append(Issue(SEVERITY_ERROR, "P0-parti-incomplete",
            f"Bloco parti sem os campos: {', '.join(missing)}."))


def check_nao_vai_ter(html: str, report: Report) -> None:
    """P7: cada feature declarada em nao-vai-ter não pode aparecer no HTML."""
    parti = parse_parti(html)
    if not parti or "nao-vai-ter" not in parti:
        return
    declared = [t.strip().lower() for t in re.split(r"[;,]", parti["nao-vai-ter"]) if t.strip()]
    scrubbed = _scrub(html)
    for feat in declared:
        pattern = NAO_VAI_TER_REGEX.get(feat)
        if pattern is None:
            report.issues.append(Issue(SEVERITY_WARN, "P7-unknown-feature",
                f'nao-vai-ter declara "{feat}", que não está no vocabulário fechado '
                f"(direcao-de-arte.md §8) — inverificável."))
            continue
        m = re.search(pattern, scrubbed, re.IGNORECASE)
        if m:
            report.issues.append(Issue(SEVERITY_ERROR, "P7-nao-vai-ter-violated",
                f'Documento declara nao-vai-ter "{feat}" mas o padrão aparece no HTML.',
                _line_of(scrubbed, m.start())))


def check_banned_fonts(html: str, report: Report) -> None:
    """P-fontes: fontes-assinatura de IA + Inter como display."""
    for font in BANNED_FONTS:
        url_form = font.replace(" ", r"\+")
        if re.search(rf"{url_form}|font-family[^;]*['\"]{font}['\"]", html):
            report.issues.append(Issue(SEVERITY_ERROR, "P-banned-font",
                f'Fonte banida detectada: "{font}" (tell de IA — ver type-kits.md).'))
    m = re.search(r"--font-display\s*:[^;]*\bInter\b", html)
    if m:
        report.issues.append(Issue(SEVERITY_ERROR, "P-inter-display",
            "Inter como --font-display é proibido (tell nº 1 de tipografia de IA). "
            "Usar kit de type-kits.md.", _line_of(html, m.start())))


def check_transition_all(html: str, report: Report) -> None:
    """P-transition: transition: all é proibido (anti-pattern C7)."""
    scrubbed = _scrub(html)
    for m in re.finditer(r"transition\s*:\s*all\b", scrubbed):
        report.issues.append(Issue(SEVERITY_ERROR, "P-transition-all",
            "transition: all detectado — transições devem ser property-scoped.",
            _line_of(scrubbed, m.start())))


def check_single_easing(html: str, report: Report) -> None:
    """P4: easing único no arquivo inteiro (quando há motion)."""
    curves = set(re.findall(r"cubic-bezier\([^)]+\)", html))
    uses = len(re.findall(r"cubic-bezier\(", html))
    if uses >= 3 and len(curves) == 1:
        report.issues.append(Issue(SEVERITY_WARN, "P4-single-easing",
            f"Uma única curva de easing ({uses} usos) para todos os papéis de movimento. "
            "Declarar 2-3 curvas com papel comentado (entrada/micro/assinatura)."))


def check_chart_defaults(html: str, report: Report) -> None:
    """P5: Chart.js sem Chart.defaults.font.family = Helvetica default (tell)."""
    if re.search(r"new\s+Chart\s*\(", html) and not re.search(r"Chart\.defaults\.font\.family", html):
        report.issues.append(Issue(SEVERITY_ERROR, "P5-chart-default-font",
            "new Chart() sem Chart.defaults.font.family — gráfico renderiza na Helvetica "
            "default da lib (tell imediato). Colar o bloco §5.0 de css-patterns.md."))


def check_chart_guard(html: str, report: Report) -> None:
    """P5b: gráfico (new Chart) sem guard de CDN. Se cdn.jsdelivr.net for bloqueado
    (intranet), `Chart` fica undefined e Chart.defaults lança, matando o script inteiro.
    Aceita `typeof Chart` ou `window.Chart` como guard. Ver css-patterns §5.0b."""
    if re.search(r"new\s+Chart\s*\(", html) and not re.search(r"typeof\s+Chart\b|window\.Chart\b", html):
        report.issues.append(Issue(SEVERITY_WARN, "P5b-chart-no-guard",
            "new Chart() sem guard de CDN (`typeof Chart !== 'undefined'`) — se o Chart.js for "
            "bloqueado (intranet), o script inteiro morre e o documento não inicializa. Envolver "
            "defaults/renders no guard + fallback no lugar do canvas (css-patterns §5.0b)."))


def check_glow_wallpaper(html: str, report: Report) -> None:
    """P-glow: glow radial incondicional em body::before/after."""
    m = re.search(r"body::(?:before|after)\s*\{[^}]*radial-gradient", html)
    if m:
        report.issues.append(Issue(SEVERITY_WARN, "P-glow-wallpaper",
            "Glow radial em body::before/after incondicional — glow deve ser localizado "
            "atrás de UM elemento (anti-pattern C8).", _line_of(html, m.start())))


def check_hover_lift(html: str, report: Report) -> None:
    """P1: hover-lift (translateY negativo) — só em clicável + perfil cinemático."""
    matches = list(re.finditer(r":hover\s*\{[^}]*translateY\(\s*-", html))
    if not matches:
        return
    parti = parse_parti(html)
    motion = (parti or {}).get("motion", "")
    if "cinematico" not in motion and "cinemático" not in motion:
        report.issues.append(Issue(SEVERITY_WARN, "P1-hover-lift",
            f"translateY negativo em :hover ({len(matches)} ocorrência(s)) sem perfil de "
            "motion cinemático declarado. Lift só em card clicável + perfil cinemático.",
            _line_of(html, matches[0].start())))


def check_hairline_reveal(html: str, report: Report) -> None:
    """P-hairline: reveal por opacidade (data-fragment/data-anim) em CARDS de um grid de
    fios expõe o fundo pintado do grid como bloco cinza sólido. Em opacity:0 o fundo do
    card (que cobre o cinza) some. Ver slide-patterns.md → Pitfalls."""
    scrubbed = _scrub(html)
    hairline = set()
    for m in re.finditer(r'\.([A-Za-z0-9_-]+)\s*\{([^}]*)\}', scrubbed):
        cls, body = m.group(1), m.group(2)
        if (re.search(r'gap:\s*[1-3]px', body)
                and re.search(r'background:\s*(?!\s*(?:transparent|none|inherit)\b)\S', body)
                and 'grid' in body):
            hairline.add(cls)
    for cls in hairline:
        pat = (r'<[^>]*class="[^"]*\b' + re.escape(cls)
               + r'\b[^"]*"[^>]*>[\s\S]{0,2000}?<[^>]*class="[^"]*card[^"]*"[^>]*\sdata-(?:fragment|anim)\b')
        if re.search(pat, html):
            report.issues.append(Issue(SEVERITY_WARN, "P-hairline-reveal",
                f'Reveal por opacidade em cards do grid de fios ".{cls}" — em opacity:0 o fundo '
                "do grid vira bloco cinza sólido. Revele o CONTAINER (data-anim no grid), não cada "
                "card. Ver slide-patterns.md → Pitfalls."))
            return


def check_em_accent_ratio(html: str, report: Report) -> None:
    """P2: <em> em mais de 25% dos títulos (muleta tipográfica da casa)."""
    heads = re.findall(r"<h[1-3][^>]*>[\s\S]*?</h[1-3]>", html, re.IGNORECASE)
    heads += re.findall(r'<[^>]+class="[^"]*title-(?:mega|xl|lg)[^"]*"[^>]*>[\s\S]*?</', html)
    if len(heads) < 4:
        return
    com_em = [h for h in heads if "<em" in h]
    ratio = len(com_em) / len(heads)
    if ratio > 0.25:
        report.issues.append(Issue(SEVERITY_WARN, "P2-em-accent",
            f"<em> em {len(com_em)}/{len(heads)} títulos ({ratio:.0%}) — máximo 25%. "
            "Variar ênfase: contraste de peso, largura ou caixa."))


def check_banned_headlines(html: str, report: Report) -> None:
    """P-headline: h2 deve ser tese (verbo/número), não rótulo de categoria."""
    for m in re.finditer(r"<h2[^>]*>([\s\S]*?)</h2>", html, re.IGNORECASE):
        text = re.sub(r"<[^>]+>", "", m.group(1)).strip().lower()
        text = re.sub(r"^[\d.\s—–-]+", "", text)  # remove numeração "02 —"
        if text in BANNED_H2:
            report.issues.append(Issue(SEVERITY_WARN, "P-headline-categoria",
                f'h2 "{text}" é título-categoria — headline deve afirmar a tese da seção '
                "(conter verbo ou número da fonte).", _line_of(html, m.start())))


def check_ai_wordlist(html: str, report: Report) -> None:
    """P-copy: léxico verbal de IA em pt-BR (warn — revisar manualmente)."""
    text = _strip_tags(html).lower()
    found = sorted({w for w in AI_WORDLIST if w in text})
    if found:
        report.issues.append(Issue(SEVERITY_WARN, "P-ai-wordlist",
            f"Léxico de IA detectado no texto: {', '.join(found)}. Reescrever com "
            "vocabulário concreto da fonte."))


# Assinaturas de momento-wow SUBSTANTIVO (W1-W17). Cada par (rótulo, regex).
#
# REGRA: materialité (grain feTurbulence, aurora CSS, glass backdrop-filter) NÃO
# está aqui — é decisão de `superficie` do parti, não momento-wow. Antes, o grain
# (presente em quase todo template por padrão) quitava sozinho a obrigação de
# ambição A2/A3, então todo doc "passava" sem entregar nada impressionante. Aqui
# só entram técnicas que produzem o "uau" de fato, ligadas ao dado-tese.
#
# Nota histórica: o regex antigo do W3 (`@keyframes[^{]*\{[^}]*font-variation-settings`)
# estava MORTO — o `{ from {` aninhado das manchetes cinéticas reais quebra o
# `[^{]*`. Os decks-bandeira passavam só no grain. Corrigido com `[\s\S]{0,400}?`.
SUBSTANTIVE_WOW = [
    # ── W1-W9 (vocabulário existente) ──
    ("W1/W6-scroll-driven",  r"animation-timeline\s*:\s*(?:view|scroll|--)"),  # cena/reveal por timeline
    ("W2-counter-sync",      r"@property\s+--n\b|counter-reset\s*:\s*\w+\s+var\(\s*--n\b"),
    ("W3-kinetic-headline",  r"@keyframes[\s\S]{0,400}?font-variation-settings"),  # eixo animado (regex consertado)
    ("W3/W4-fvs-var",        r"font-variation-settings[^;]*var\("),  # eixo via var animável
    ("W4/W6-segmenter",      r"Intl\.Segmenter"),  # split grapheme/word
    ("W4/W8-pointer-raf",    r"requestAnimationFrame[\s\S]{0,400}getBoundingClientRect"),  # proximity/crosshair
    ("W5-view-transition",   r"\.startViewTransition\b|view-transition-name\s*:"),
    ("W8-live-annotation",   r"afterDatasetsDraw\b[\s\S]{0,800}?(?:fillRect|setLineDash|getPixelForValue|leader)"),
    ("W9-webgl",             r"getContext\(\s*['\"]webgl|new\s+Gradient\s*\("),  # hero minigl/shader
    # ── W10-W17 (camada de assinatura premium — inerte até os drop-ins existirem) ──
    ("W10-mask-reveal",      r"clip-path[\s\S]{0,220}?animation-timeline|animation-timeline[\s\S]{0,220}?clip-path"),
    ("W11-magnetic",         r"pointermove[\s\S]{0,400}?(?:translate3?d?\(|transform\s*=)"),
    ("W12-spotlight",        r"pointermove[\s\S]{0,300}?--m[xy]\b"),
    ("W13-horizontal-pin",   r"h-track|h-pin"),
    ("W15-odometer",         r"\.odometer\b|data-odometer\b"),
    ("W16-scroll-velocity",  r"--scroll-vel\b|data-scroll-vel\b"),
    ("W17-scramble",         r"\.scramble\b|data-scramble\b"),
    # ── W18-W31 (repertório expandido v7 — empilhamento de alto impacto) ──
    ("W18-sticky-stack",     r"\bstack-card\b"),
    ("W19-masked-type",      r"\bmasked-type\b"),
    ("W20-aurora-mesh",      r"\baurora-mesh\b"),
    ("W21-hue-drift",        r"--doc-hue\b"),
    ("W22-draw-on",          r"\bdraw-on\b|stroke-dashoffset"),
    ("W23-gooey",            r"url\(\s*#goo\b"),
    ("W24-tilt",             r"\bdata-tilt\b"),
    ("W25-data-choreo",      r"\bdata-choreo\b"),
    ("W26-spot-mask",        r"\bdata-spot-mask\b"),
    ("W27-marquee",          r"\bmarquee__track\b|\.marquee\b"),
    ("W28-chapter-divider",  r"\bchapter-divider\b"),
    ("W29-focus-reveal",     r"\bfocus-reveal\b"),
    ("W30-flip-in",          r"\bdata-flip-in\b"),
    ("W31-glitch",           r"\.glitch\b"),
]
SOBER_REGISTERS = ("institucional-impresso", "relatorio-de-bancada", "relatório-de-bancada")


def _ambicao_level(parti: Optional[dict]) -> Optional[str]:
    if not parti:
        return None
    raw = (parti.get("ambicao") or "").lower()
    if "a3" in raw or "extraordin" in raw:
        return "A3"
    if "a2" in raw or "elevado" in raw:
        return "A2"
    if "a1" in raw or "contido" in raw:
        return "A1"
    return None


# Mapa W# → assinatura de ENTREGA (para o cruzamento momento-wow declarado↔entregue, P8).
# Inclui W7 (materialité: grain/aurora/glass) que NÃO conta como substantivo (P8-floor) mas
# É uma entrega válida quando declarado explicitamente como momento-wow.
WOW_DELIVERY = {
    "W1":  r"animation-timeline\s*:\s*(?:view|scroll|--)",
    "W2":  r"@property\s+--n\b|counter-reset",
    "W3":  r"@keyframes[\s\S]{0,400}?font-variation-settings|font-variation-settings[^;]*var\(",
    "W4":  r"Intl\.Segmenter|pointermove[\s\S]{0,400}?fontVariationSettings",
    "W5":  r"\.startViewTransition\b|view-transition-name\s*:",
    "W6":  r"Intl\.Segmenter",
    "W7":  r"feTurbulence|\.aurora\b|backdrop-filter\s*:\s*blur",
    "W8":  r"afterDatasetsDraw\b",
    "W9":  r"getContext\(\s*['\"]webgl|new\s+Gradient\s*\(",
    "W10": r"clip-path[\s\S]{0,220}?animation-timeline|animation-timeline[\s\S]{0,220}?clip-path",
    "W11": r"data-magnetic\b",
    "W12": r"data-spotlight\b|--m[xy]\b",
    "W13": r"h-track|h-pin",
    "W14": r"parallax|--plx\b",
    "W15": r"\.odometer\b|data-odometer\b",
    "W16": r"--scroll-vel\b|data-scroll-vel\b",
    "W17": r"\.scramble\b|data-scramble\b",
    "W18": r"\bstack-card\b", "W19": r"\bmasked-type\b", "W20": r"\baurora-mesh\b",
    "W21": r"--doc-hue\b", "W22": r"\bdraw-on\b|stroke-dashoffset", "W23": r"url\(\s*#goo\b",
    "W24": r"\bdata-tilt\b", "W25": r"\bdata-choreo\b", "W26": r"\bdata-spot-mask\b",
    "W27": r"\bmarquee__track\b|\.marquee\b", "W28": r"\bchapter-divider\b",
    "W29": r"\bfocus-reveal\b", "W30": r"\bdata-flip-in\b", "W31": r"\.glitch\b",
}
# Famílias premium (camada de assinatura "agência premiada") — gateadas a registro expressivo.
# Os v7 ambientes/editoriais (W21 hue, W22 draw-on, W25 data-choreo, W29 blur-focus) NÃO são
# premium: são tasteful o bastante para registro sóbrio (report). O resto é gateado.
PREMIUM_FAMILIES = ("W10", "W11", "W12", "W13", "W15", "W16", "W17",
                    "W18", "W19", "W20", "W23", "W24", "W26", "W27", "W28", "W30", "W31")


def _wow_family(name: str) -> str:
    """'W3-kinetic-headline' → 'W3'; 'W1/W6-scroll-driven' → 'W1'."""
    return name.split("-")[0].split("/")[0]


def check_ambicao_delivered(html: str, report: Report) -> None:
    """P8 (músculo simétrico do nao-vai-ter): ambição A2/A3 declarada TEM que ser
    entregue — momento-wow SUBSTANTIVO no HTML. Cobra densidade (A1 1-2 calmos, A2 3-5,
    A3 6-8 com ≥4 famílias), zona (ligado ao dado) e coerência declarado↔entregue."""
    parti = parse_parti(html)
    level = _ambicao_level(parti)
    if level not in ("A1", "A2", "A3"):
        return
    scrubbed = _scrub(html)
    found = [(name, re.search(pat, scrubbed, re.IGNORECASE)) for name, pat in SUBSTANTIVE_WOW]
    found = [(name, m) for name, m in found if m]
    names = [name for name, _ in found]

    # A1 (sóbrio): agora pede 1-2 momentos CALMOS (não-premium) ligados ao dado. As famílias
    # loud seguem barradas pelo P-premium-sobrio — aqui só o piso calmo (WARN, não ERROR).
    if level == "A1":
        calm = [n for n in names if _wow_family(n) not in PREMIUM_FAMILIES]
        if not calm:
            report.issues.append(Issue(SEVERITY_WARN, "P8-a1-sem-momento-calmo",
                "ambicao A1 (sóbrio) pede 1-2 momentos CALMOS — text-reveal (W6), anotação viva no "
                "gráfico (W8), counter+barra (W2), draw-on (W22) ou máscara editorial (W10) — ligados "
                "ao dado. Nenhum encontrado. Sobriedade não é chapa: 1-2 gestos contidos elevam sem "
                "quebrar o registro (as famílias loud seguem proibidas no sóbrio)."))
        return

    if not names:
        report.issues.append(Issue(SEVERITY_ERROR, "P8-ambicao-nao-entregue",
            f"Parti declara ambicao {level} mas nenhum momento-wow SUBSTANTIVO aparece "
            "no HTML. Grain/aurora/glass são materialité (decisão `superficie`), NÃO quitam a "
            "ambição. Entregar técnicas de wow-components.md ligadas ao dado-tese."))
        if "momento-wow" not in (parti or {}):
            report.issues.append(Issue(SEVERITY_WARN, "P8-sem-campo-momento-wow",
                f"ambicao {level} sem campo `momento-wow:` no parti — declarar qual W# e onde."))
        return

    # P8-densidade (v7 — empilhamento): A2 alvo 3-5; A3 empilha 6-8 (≥4 famílias distintas).
    families = {_wow_family(n) for n in names}
    minimo = 4 if level == "A3" else 3
    if len(families) < minimo:
        alvo = "6-8 (A3 empilha: 1 herói + 2 sistemas ambientes + 3-4 momentos; ≥4 famílias)" if level == "A3" else "3-5 por dobra/seção"
        report.issues.append(Issue(SEVERITY_WARN, "P8-densidade-baixa",
            f"ambicao {level} com {len(families)} momento-wow substantivo ({', '.join(sorted(families))}). "
            f"Alvo: {alvo}, cada um ligado ao dado. Ver §STACKING em wow-components.md."))

    # P8-zone (lenient, WARN) — o wow precisa cair na zona herói/dado, não enterrado.
    zone_ok = False
    for _, m in found:
        ctx = scrubbed[max(0, m.start() - 800):m.start() + 800]
        if re.search(r"hero|capa|big-num|metric|kpi|fact|chart|title-(?:mega|xl)|story__chart", ctx, re.IGNORECASE):
            zone_ok = True
            break
        if m.start() < len(scrubbed) * 0.45:
            zone_ok = True
            break
    if not zone_ok:
        report.issues.append(Issue(SEVERITY_WARN, "P8-zone",
            "Momento-wow presente mas longe da zona herói/primeira-dobra/dado-tese. "
            "Ligar o wow ao elemento mais importante (capa, número-tese, gráfico)."))

    # momento-wow DECLARADO tem que ser ENTREGUE (gêmeo simétrico do nao-vai-ter).
    # SÓ para a camada premium (W10-W17): lá os marcadores são precisos (data-magnetic,
    # .odometer, data-scramble...). W1-W9 têm entrega variada demais (ex.: W2 pode ser
    # @property --n OU counter JS) — checá-los daria falso-positivo; o piso+densidade já cobrem.
    declared = sorted(set(re.findall(r"W\d+", (parti.get("momento-wow") or ""))))
    for w in declared:
        if w not in PREMIUM_FAMILIES:
            continue
        pat = WOW_DELIVERY.get(w)
        if pat and not re.search(pat, scrubbed, re.IGNORECASE):
            report.issues.append(Issue(SEVERITY_WARN, "P8-wow-declarado-nao-entregue",
                f"Parti declara momento-wow premium {w} mas a assinatura técnica não aparece no HTML. "
                "Colar o drop-in de wow-components.md ou corrigir o parti."))

    if "momento-wow" not in (parti or {}):
        report.issues.append(Issue(SEVERITY_WARN, "P8-sem-campo-momento-wow",
            f"ambicao {level} sem campo `momento-wow:` no parti — declarar qual W# e onde."))


def check_ambicao_fallback(html: str, report: Report) -> None:
    """P9 (protege a intranet): todo gesto de ponta precisa de rede (@supports/guard)."""
    scrubbed = _scrub(html)
    if re.search(r"animation-timeline\s*:", scrubbed) and not re.search(r"@supports\s*\([^)]*animation-timeline", scrubbed):
        report.issues.append(Issue(SEVERITY_ERROR, "P9-scroll-driven-sem-supports",
            "animation-timeline usado sem @supports (animation-timeline: ...). Num Chrome "
            "travado o conteúdo pode sumir — envolver em @supports com estado-final-base."))
    if re.search(r"\.startViewTransition", scrubbed) and not re.search(r"!\s*document\.startViewTransition|document\.startViewTransition\s*&&|if\s*\(\s*document\.startViewTransition", scrubbed):
        report.issues.append(Issue(SEVERITY_WARN, "P9-view-transition-sem-guard",
            "startViewTransition sem guard de feature-detect (if (!document.startViewTransition)...). "
            "Sem o guard, navegadores sem suporte podem não atualizar o DOM."))
    if re.search(r"backdrop-filter\s*:\s*blur", scrubbed) and not re.search(r"@supports[^{]*backdrop-filter", scrubbed):
        # fallback aceitável também via background translúcido NO MESMO bloco (topbar rgba 0.88
        # continua legível sem o blur) — só avisa se algum glass não tem nem @supports nem bg de base.
        sem_fallback = [m.group(0) for m in re.finditer(r"\{[^{}]*backdrop-filter\s*:\s*blur[^{}]*\}", scrubbed)
                        if not re.search(r"background[^;}]*(?:rgba|color-mix|var\(--color)", m.group(0))]
        if sem_fallback:
            report.issues.append(Issue(SEVERITY_WARN, "P9-glass-sem-fallback",
                "backdrop-filter sem @supports nem background de base sólido/translúcido. "
                "Em Chrome antigo o vidro vira invisível — adicionar @supports not ou um background."))
    # W9: hero WebGL TEM que ter fallback material (intranet/Chrome travado não pode regredir
    # em silêncio). O fallback canônico é a aurora CSS — seja a classe `.aurora-fallback`
    # (canvas), o irmão `.hero-aurora` + `.webgl-hero.is-empty` (canvas some, revela a aurora),
    # ou qualquer `aurora` material no hero. Aceita as duas convenções do corpus.
    if re.search(r"getContext\(\s*['\"](?:webgl|experimental-webgl)", scrubbed) and not re.search(r"aurora|is-(?:fallback|empty)\b", scrubbed, re.IGNORECASE):
        report.issues.append(Issue(SEVERITY_ERROR, "P9-webgl-sem-fallback",
            "Hero WebGL (getContext('webgl')) sem fallback material (aurora CSS / .aurora-fallback / "
            ".hero-aurora). Sem WebGL/reduced-motion o hero fica preto-morto — colar o fallback do W9 "
            "(wow-components.md)."))


def check_ambicao_coerente(html: str, report: Report) -> None:
    """P10: A3 é proibido em registro sóbrio (regulatório/RI) — coerência parti↔registro."""
    parti = parse_parti(html)
    if _ambicao_level(parti) != "A3":
        return
    registro = (parti.get("registro") or "").lower()
    if any(s in registro for s in SOBER_REGISTERS):
        # Exceção: /overdrive é opt-in DELIBERADO (marcado por data-overdrive). O P10
        # protege contra A3 acidental em documento sóbrio, não contra um showcase ao vivo
        # que o usuário pediu explicitamente (ex.: deck-overdrive de resultados ao vivo).
        if re.search(r"data-overdrive|data-showcase", html):
            return
        report.issues.append(Issue(SEVERITY_ERROR, "P10-a3-em-registro-sobrio",
            f"ambicao A3-extraordinário declarada em registro sóbrio ('{registro.split('(')[0].strip()}'). "
            "Documento sóbrio sobe via A2 (materialmente mais rico), nunca A3 — salvo /overdrive "
            "deliberado (data-overdrive). Ver ambicao.md."))


def check_premium_sobrio(html: str, report: Report) -> None:
    """P-premium-sobrio: a camada premium (W10-W17, 'agência premiada') é gateada a
    registros expressivos. Em registro sóbrio (regulatório/RI) é ERRO — salvo /overdrive."""
    parti = parse_parti(html)
    if not parti:
        return
    registro = (parti.get("registro") or "").lower()
    if not any(s in registro for s in SOBER_REGISTERS):
        return
    # data-overdrive = showcase ao vivo opt-in; data-showcase = peça de DEMONSTRAÇÃO da skill
    # (o corpus demos/ existe para exibir o palette inteiro, premium incluso, em todo registro).
    # Em geração real (sem esses flags) a regra continua: documento sóbrio não recebe premium.
    if re.search(r"data-overdrive|data-showcase", html):
        return
    scrubbed = _scrub(html)
    hits = [name for name, pat in SUBSTANTIVE_WOW
            if _wow_family(name) in PREMIUM_FAMILIES and re.search(pat, scrubbed, re.IGNORECASE)]
    if hits:
        report.issues.append(Issue(SEVERITY_ERROR, "P-premium-sobrio",
            f"Efeito premium ({', '.join(hits)}) em registro sóbrio ('{registro.split('(')[0].strip()}'). "
            "A camada premium (W10-W17) é gateada a registros expressivos (deck/site/hub/scrollytelling). "
            "Documento sóbrio sobe via materialidade/W6/W8 contidos. Ver wow-components.md."))


def check_premium_parcimonia(html: str, report: Report) -> None:
    """P-premium-*: parcimônia da camada premium — dose, não só presença (anti-slop)."""
    scrubbed = _scrub(html)
    # 1 spotlight por documento (luz que segue o cursor satura rápido).
    # Contar só ELEMENTOS HTML com o atributo — não o seletor CSS `[data-spotlight]`
    # nem o querySelectorAll do JS (senão um uso único legítimo já dispararia).
    n_spot = len(re.findall(r"<[^>]+\bdata-spotlight\b", html))
    if n_spot > 1:
        report.issues.append(Issue(SEVERITY_WARN, "P-premium-spotlight",
            f"{n_spot} spotlights (W12) — máx 1 por documento. A luz que segue o cursor satura "
            "se repetida; reservar ao bloco-herói/insight único."))
    # 1 scramble por documento (decode de número satura)
    n_scr = len(re.findall(r"<[^>]+\b(?:data-scramble\b|class=\"[^\"]*\bscramble\b)", html))
    if n_scr > 1:
        report.issues.append(Issue(SEVERITY_WARN, "P-premium-scramble",
            f"{n_scr} scrambles (W17) — máx 1 por documento, só no número-tese."))
    # magnetismo/spotlight/tilt/spot-mask exigem branch hover + reduced-motion no JS (só desktop, acessível)
    if re.search(r"data-(?:magnetic|spotlight|tilt|spot-mask)\b", html):
        if not re.search(r"hover\s*:\s*hover", scrubbed):
            report.issues.append(Issue(SEVERITY_WARN, "P-premium-sem-hover-guard",
                "Efeito cursor-reativo (W11/W12/W24/W26) sem guard @media (hover:hover) and (pointer:fine). "
                "Em touch vira comportamento errático — restringir a desktop+mouse. Ver wow-components.md."))
    # 1 glitch por documento (spice tonal satura)
    n_glitch = len(re.findall(r"<[^>]+\bclass=\"[^\"]*\bglitch\b", html))
    if n_glitch > 1:
        report.issues.append(Issue(SEVERITY_WARN, "P-premium-glitch",
            f"{n_glitch} glitches (W31) — máx 1 por documento, uma palavra, zonas escuras/tech."))
    # excesso de mecânicas PINNED (≥3) — fadiga de scroll/enjoo (regra de conflito §STACKING).
    # Só conta mecânicas que PRENDEM o scroll (sticky/scrub); o hue-drift (scroll(root) ambiente,
    # sem sticky) NÃO é pinned — por isso usa-se marcadores explícitos, não animation-timeline:scroll genérico.
    pinned = sum(1 for pat in (r"\bstack-card\b", r"\bchapter-divider\b",
                               r"\bh-pin\b|\bh-track\b", r"\bscrub-stage\b")
                 if re.search(pat, scrubbed, re.IGNORECASE))
    if pinned >= 3:
        report.issues.append(Issue(SEVERITY_WARN, "P-premium-pinned-excesso",
            f"{pinned} mecânicas pinned/scrub (sticky-stack/chapter-divider/horizontal/scrub) no doc. "
            "Regra de ouro: UM herói pinned por documento — duas+ disputam o scroll e enjoam (§STACKING)."))


# ─── Checks técnicos de FUNCIONAMENTO (bugs que quebram em silêncio) ──────
# Adicionados após a sessão de polish v7 que descobriu cada um na prática.

PLACEHOLDERS = [
    (r">BRAND\b|topbar__brand\">BRAND", "BRAND (marca não preenchida)"),
    (r"\{\{[A-Z_0-9]+\}\}", "{{...}} (placeholder mustache do template)"),
    (r"TÍTULO DO |TÍTULO —|>TÍTULO<|TÍTULO DA NARRATIVA", "TÍTULO (título não preenchido)"),
    (r">Card \d+<|class=\"card__title\">Card \d", "Card N (card de exemplo)"),
    (r">Cena \d+<", "Cena N (cena de exemplo)"),
    (r">Seção \d+<|>Seção</", "Seção N (seção de exemplo)"),
    (r">Coluna [AB]<|>Coluna A</|>Coluna B<", "Coluna A/B (coluna de exemplo)"),
    (r">Categoria [AB]<|data-filter=\"categoria-[ab]\"", "Categoria A/B (filtro de exemplo)"),
    (r"Lorem ipsum", "lorem ipsum"),
    (r"AAAA-MM-DD|AAAA\b(?!-)", "AAAA-MM-DD (data placeholder)"),
    (r"descrição da métrica|Conteúdo da cena|Conteúdo da seção|Subtítulo descrevendo|Detalhes do recurso|Conteúdo\.</p>", "texto placeholder do template"),
]


def check_placeholders(html: str, report: Report) -> None:
    """P0-placeholder: marcador do template não preenchido. Documento entregue
    com BRAND/TÍTULO/{{...}}/Card N = geração incompleta. Roda sobre _scrub (sem
    comentários): um placeholder em comentário-documentação não é bug renderizado."""
    scrubbed = _scrub(html)
    for pat, name in PLACEHOLDERS:
        m = re.search(pat, scrubbed)
        if m:
            report.issues.append(Issue(SEVERITY_ERROR, "P0-placeholder",
                f"Placeholder do template não preenchido: {name} ('{m.group(0)[:30]}'). "
                "Geração incompleta — substituir pelo conteúdo real.", _line_of(scrubbed, m.start())))


def check_invalid_calc(html: str, report: Report) -> None:
    """B-css-calc: `+`/`-` sem espaço dentro de calc/clamp/min/max é CSS INVÁLIDO —
    o navegador DESCARTA a declaração inteira em silêncio (a fonte/tamanho não aplica,
    cai pro default). Bug clássico: clamp(2rem,2rem+6vw,8rem) deixa o elemento minúsculo."""
    scrubbed = _scrub(html)
    m = re.search(r"(?:rem|em|px|vw|vh|ch|fr|vmin|vmax|%)[+\-]\d", scrubbed)
    if m:
        report.issues.append(Issue(SEVERITY_ERROR, "B-css-calc-invalido",
            f"Operador `+`/`-` sem espaço em volta dentro de calc/clamp (ex.: '{m.group(0)}'). "
            "É CSS inválido — o navegador descarta a regra inteira e o tamanho cai pro default. "
            "Sempre `2rem + 6vw`, nunca `2rem+6vw`.", _line_of(scrubbed, m.start())))


def check_canvas_autosize(html: str, report: Report) -> None:
    """B-canvas-autosize: regra CSS de <canvas> com width/height: auto. <canvas> é replaced
    element — width:auto usa o tamanho INTRÍNSECO (o buffer = css × devicePixelRatio); em telas
    HiDPI (2×/3×, muitos laptops) o gráfico Chart.js exibe no dobro/triplo e ESTOURA o container.
    Em DPR=1 (a tela do dev) parece ok. Usar tamanho explícito (100% / calc), nunca auto."""
    scrubbed = _scrub(html)
    m = re.search(r"canvas[^{}]*\{[^}]*\b(?:width|height)\s*:\s*auto", scrubbed)
    if m:
        report.issues.append(Issue(SEVERITY_ERROR, "B-canvas-autosize",
            "Regra de <canvas> com `width/height: auto`. Canvas é replaced element — `auto` usa o "
            "tamanho intrínseco (buffer = css × devicePixelRatio); em tela 2×/3× o gráfico exibe no "
            "dobro e estoura o box (some em DPR=1). Use tamanho explícito (`width:100% !important` ou "
            "`calc(...)`), nunca auto.", _line_of(scrubbed, m.start())))


def check_kit_vars(html: str, report: Report) -> None:
    """B-kit-undefined: <link> de fonte carregado mas `--kit-display:` não definido →
    o tema usa var(--kit-display, fallback) e cai pro Georgia/sistema; o kit fica inútil."""
    if re.search(r"fonts\.googleapis\.com|--font-display\s*:\s*[^;]*var\(\s*--kit-display", html):
        if not re.search(r"--kit-display\s*:", html):
            report.issues.append(Issue(SEVERITY_ERROR, "B-kit-undefined",
                "Fonte de kit referenciada (var(--kit-display)) mas `--kit-display:` nunca é "
                "DEFINIDO num :root. O tema cai pro fallback (Georgia/sistema) e o kit carregado "
                "via <link> fica inútil. Definir --kit-display/text/ui/mono ANTES do bloco do tema."))


def check_nested_script(html: str, report: Report) -> None:
    """B-nested-script: <script> dentro de outro <script> → 'Unexpected token <' em runtime,
    que MATA todo o JS do documento (navegação, animações, números). Catch estático do erro
    que só aparecia ao renderizar."""
    if re.search(r"<script\b[^>]*>(?:(?!</script>)[\s\S])*?<script\b", html, re.IGNORECASE):
        report.issues.append(Issue(SEVERITY_ERROR, "B-nested-script",
            "<script> aninhado dentro de outro <script> — gera SyntaxError 'Unexpected token <' "
            "em runtime e mata TODO o JavaScript do documento. Cada bloco <script> deve ser "
            "irmão (fechar um antes de abrir o próximo), nunca aninhado."))


def run_p_checks(html: str, report: Report) -> None:
    check_parti_block(html, report)
    check_nao_vai_ter(html, report)
    check_banned_fonts(html, report)
    check_transition_all(html, report)
    check_single_easing(html, report)
    check_chart_defaults(html, report)
    check_chart_guard(html, report)
    check_glow_wallpaper(html, report)
    check_hover_lift(html, report)
    check_hairline_reveal(html, report)
    check_em_accent_ratio(html, report)
    check_banned_headlines(html, report)
    check_ai_wordlist(html, report)
    check_ambicao_delivered(html, report)   # P8 (entrega + densidade + zona + declarado↔entregue)
    check_ambicao_fallback(html, report)    # P9
    check_ambicao_coerente(html, report)    # P10
    check_premium_sobrio(html, report)      # P-premium-sobrio (gateamento da estética híbrida)
    check_premium_parcimonia(html, report)  # P-premium-* (dose)


# ─── --stats: telemetria do pool (curadoria viva) ────────────────────────


def stats_mode(folder: Path) -> int:
    """Varre *.html de uma pasta, extrai blocos parti e tabula a distribuição
    de eixos. É o instrumento da revisão trimestral: eixo usado em >40% dos
    documentos vira candidato a aposentadoria/quota (slop de 3ª geração)."""
    from collections import Counter

    files = sorted(folder.rglob("*.html"))
    if not files:
        print(f"Nenhum .html em {folder}", file=sys.stderr)
        return 2

    axes = ["registro", "kit", "capa", "superficie", "motion", "ambicao", "assinatura"]
    counters = {a: Counter() for a in axes}
    wow_counter = Counter()     # famílias W# ENTREGUES (anti-uniformidade)
    wow_docs = 0                # docs A2/A3 considerados
    mono_wow = []               # docs com um único momento-wow (abaixo da régua 3-5)
    sem_parti = []
    total = 0

    for f in files:
        try:
            html = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        total += 1
        parti = parse_parti(html)
        if not parti:
            sem_parti.append(f.name)
            continue
        for a in axes:
            if a in parti:
                # normaliza: primeiro token antes de '(' ou '—'
                val = re.split(r"[(—–]", parti[a])[0].strip().lower()
                counters[a][val] += 1
        # anti-uniformidade: que famílias de momento-wow o doc A2/A3 realmente entrega?
        if _ambicao_level(parti) in ("A2", "A3"):
            wow_docs += 1
            scrubbed = _scrub(html)
            fams = sorted({_wow_family(name) for name, pat in SUBSTANTIVE_WOW
                           if re.search(pat, scrubbed, re.IGNORECASE)})
            for fam in fams:
                wow_counter[fam] += 1
            if len(fams) <= 1:
                mono_wow.append((f.name, fams[0] if fams else "—"))

    com_parti = total - len(sem_parti)
    print(f"Pasta    : {folder}")
    print(f"Arquivos : {total} html | {com_parti} com parti | {len(sem_parti)} legado sem parti")
    print("-" * 72)
    for a in axes:
        print(f"\n{a.upper()}")
        if not counters[a]:
            print("  (nenhum valor)")
            continue
        for val, n in counters[a].most_common():
            pct = n / com_parti * 100 if com_parti else 0
            flag = "  <-- >40%: candidato a quota/aposentadoria" if pct > 40 and com_parti >= 3 else ""
            print(f"  {n:3d}  {pct:5.1f}%  {val}{flag}")
    # ── Anti-uniformidade: distribuição de momento-wow ENTREGUE (não declarado).
    # Fingerprint visível: se >60% dos docs A2/A3 usam a MESMA família única, vira tell.
    if wow_docs:
        print(f"\nMOMENTO-WOW ENTREGUE  ({wow_docs} docs A2/A3)")
        for fam, n in wow_counter.most_common():
            pct = n / wow_docs * 100
            flag = "  <-- >60%: vira fingerprint da casa (variar o W#)" if pct > 60 and wow_docs >= 3 else ""
            print(f"  {n:3d}  {pct:5.1f}%  {fam}{flag}")
        if mono_wow:
            print(f"\n  Abaixo da régua (1 momento-wow; alvo 3-5 por dobra/seção):")
            for name, fam in mono_wow:
                print(f"    - {name}  ({fam})")

    if sem_parti:
        print("\nSEM PARTI (legado):")
        for name in sem_parti:
            print(f"  - {name}")
    return 0


# ─── Orquestração ────────────────────────────────────────────────────────


def validate(html_path: Path, strict: bool = False) -> Report:
    html = html_path.read_text(encoding="utf-8")
    # Blobs base64 de data-URI (logos, fontes, demos embutidas) são DADOS opacos —
    # neutraliza o conteúdo do blob para os checks não falsarem em "+digito" (calc),
    # "AAAA" (placeholder) etc. O blob é uma linha só, então os nº de linha não mudam.
    html = re.sub(r"(;base64,)[A-Za-z0-9+/=]{40,}", r"\1BASE64DATA", html)
    model = identify_model(html)
    theme = identify_theme(html)
    report = Report(file=str(html_path), model=model, theme=theme)

    # Checks universais
    check_boot_script(html, report)
    check_single_file(html, report)
    check_dark_overrides(html, report)
    check_reduced_motion(html, report)
    check_focus_visible(html, report)
    check_lang_attribute(html, report)
    check_meta_viewport(html, report)
    check_hex_outside_root(html, report)
    check_huge_typography_outside_deck(html, report, model)

    # Checks técnicos de FUNCIONAMENTO (bugs que quebram em silêncio — v7 polish)
    check_placeholders(html, report)
    check_invalid_calc(html, report)
    check_canvas_autosize(html, report)
    check_kit_vars(html, report)
    check_nested_script(html, report)

    # Categoria P — Pasteurização / AI-tells (v4)
    run_p_checks(html, report)

    # Checks específicos do modelo
    if model == "deck":
        check_keyboard_deck(html, report)
    elif model == "handbook":
        check_handbook_sidebar(html, report)
    elif model == "site":
        check_site_hash_routing(html, report)
    elif model == "scrollytelling":
        check_scrollytelling_progress(html, report)

    if strict:
        for issue in report.issues:
            if issue.severity == SEVERITY_WARN:
                issue.severity = SEVERITY_ERROR

    return report


def main() -> int:
    # Console Windows costuma ser cp1252 e quebra ao imprimir ≥, ×, → etc. das
    # mensagens. Forçar UTF-8 na saída evita UnicodeEncodeError em qualquer locale.
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(description="Valida documento slideless")
    parser.add_argument("file", help="Caminho do .html (ou pasta, com --stats)")
    parser.add_argument("--quick", action="store_true", help="Apenas identifica modelo/tema")
    parser.add_argument("--strict", action="store_true", help="Warnings viram erros")
    parser.add_argument("--json", action="store_true", help="Saída JSON")
    parser.add_argument("--stats", action="store_true",
        help="Telemetria do pool: varre a PASTA, extrai blocos parti e tabula eixos")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERRO: arquivo não existe: {path}", file=sys.stderr)
        return 2

    if args.stats:
        if not path.is_dir():
            print("ERRO: --stats espera uma pasta", file=sys.stderr)
            return 2
        return stats_mode(path)

    if args.quick:
        html = path.read_text(encoding="utf-8")
        print(json.dumps({
            "file": str(path),
            "model": identify_model(html),
            "theme": identify_theme(html),
        }, indent=2, ensure_ascii=False))
        return 0

    report = validate(path, strict=args.strict)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"Arquivo : {report.file}")
        print(f"Modelo  : {report.model or '(desconhecido)'}")
        print(f"Tema    : {report.theme or '(desconhecido)'}")
        print(f"Issues  : {len(report.errors)} erro(s), {len(report.warnings)} warning(s)")
        print("-" * 72)
        if report.issues:
            for i in report.issues:
                print(i.fmt())
        else:
            print("OK — nenhuma violação detectada.")

    return 0 if not report.errors else 1


if __name__ == "__main__":
    sys.exit(main())
