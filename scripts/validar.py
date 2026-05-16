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
    parser.add_argument("file", help="Caminho do .html")
    parser.add_argument("--quick", action="store_true", help="Apenas identifica modelo/tema")
    parser.add_argument("--strict", action="store_true", help="Warnings viram erros")
    parser.add_argument("--json", action="store_true", help="Saída JSON")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERRO: arquivo não existe: {path}", file=sys.stderr)
        return 2

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
