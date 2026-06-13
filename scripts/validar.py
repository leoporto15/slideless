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


# Assinaturas técnicas de "ambição entregue" (momentos-wow W1-W9)
AMBICAO_SIGNATURES = [
    r"animation-timeline\s*:",          # W1/W2/W3/W6 scroll-driven
    r"startViewTransition",             # W5 view transitions
    r"view-transition-name\s*:",        # W5
    r"font-variation-settings[^;]*var\(", # W3/W4 kinetic type (eixo via var animável)
    r"@keyframes[^{]*\{[^}]*font-variation-settings",  # W3 eixo animado
    r"Intl\.Segmenter",                 # W4/W6 split/proximity
    r"\.aurora\b",                      # W7 aurora
    r"feTurbulence",                    # W7 grain
    r"backdrop-filter\s*:\s*blur",      # W7 glass
    r"@property\s+--ang",               # conic glow
    r"new\s+Gradient\s*\(",             # W9 minigl
    r"requestAnimationFrame[\s\S]{0,400}getBoundingClientRect",  # W4 cursor-proximity / W8 crosshair
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


def check_ambicao_delivered(html: str, report: Report) -> None:
    """P8 (músculo simétrico do nao-vai-ter): ambição A2/A3 declarada TEM que ser
    entregue — ao menos um momento-wow tem que existir no HTML."""
    parti = parse_parti(html)
    level = _ambicao_level(parti)
    if level not in ("A2", "A3"):
        return
    scrubbed = _scrub(html)
    if not any(re.search(p, scrubbed, re.IGNORECASE) for p in AMBICAO_SIGNATURES):
        report.issues.append(Issue(SEVERITY_ERROR, "P8-ambicao-nao-entregue",
            f"Parti declara ambicao {level} mas nenhum momento-wow (W1-W9) aparece no HTML. "
            "Ambição declarada e não entregue = falha. Ver ambicao.md."))
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
        if re.search(r"data-overdrive", html):
            return
        report.issues.append(Issue(SEVERITY_ERROR, "P10-a3-em-registro-sobrio",
            f"ambicao A3-extraordinário declarada em registro sóbrio ('{registro.split('(')[0].strip()}'). "
            "Documento sóbrio sobe via A2 (materialmente mais rico), nunca A3 — salvo /overdrive "
            "deliberado (data-overdrive). Ver ambicao.md."))


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
    check_ambicao_delivered(html, report)   # P8
    check_ambicao_fallback(html, report)    # P9
    check_ambicao_coerente(html, report)    # P10


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
    if sem_parti:
        print("\nSEM PARTI (legado):")
        for name in sem_parti:
            print(f"  - {name}")
    return 0


# ─── Orquestração ────────────────────────────────────────────────────────


def validate(html_path: Path, strict: bool = False) -> Report:
    html = html_path.read_text(encoding="utf-8")
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
