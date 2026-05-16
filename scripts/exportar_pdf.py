"""
slideless — exportador PDF + screenshots via Playwright (async)

Renderiza um documento slideless em PDF (deck = A4 landscape; demais = A4
retrato), ou em PNGs (1 por slide no deck; 1 por h2 nos demais).

Detecta o modelo automaticamente usando o mesmo método de validar.py.

Dependências:
    pip install playwright
    playwright install chromium

Uso:
    python exportar_pdf.py <arquivo.html>
    python exportar_pdf.py <arquivo.html> --output /tmp/saida.pdf
    python exportar_pdf.py <arquivo.html> --mode screenshots --output /tmp/png/
    python exportar_pdf.py <arquivo.html> --theme dark   # força tema antes do render

Exit code: 0 OK, 1 falha de render, 2 args inválidos.
"""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from pathlib import Path
from typing import Optional


# Importa em escopo de função para não exigir playwright apenas para --help
def _import_playwright():
    try:
        from playwright.async_api import async_playwright
        return async_playwright
    except ImportError:
        print("ERRO: pacote `playwright` não instalado.", file=sys.stderr)
        print("Instale com: pip install playwright && playwright install chromium", file=sys.stderr)
        sys.exit(2)


def identify_model(html: str) -> Optional[str]:
    """Espelho de scripts/validar.py:identify_model — manter em sincronia."""
    if re.search(r'<section\s+class="slide"[^>]*data-slide=', html):
        return "deck"
    if re.search(r'<div\s+class="deck"\b', html):
        return "deck"
    if re.search(r'<aside\s+class="sidebar"', html):
        return "handbook"
    if re.search(r'<article\s+class="view\b', html) and re.search(r'(hashchange|topnav|topbar__nav)', html):
        return "site"
    if re.search(r'class="(?:filters|filter)\b', html) and re.search(r'class="grid"', html):
        return "hub"
    if re.search(r'class="progress"', html) or re.search(r'id="progress(?:-bar)?"', html):
        if re.search(r'data-reveal', html):
            return "scrollytelling"
    if re.search(r'class="scrolly"', html) or re.search(r'class="scene\b', html):
        return "scrollytelling"
    return None


async def export_pdf(
    html_path: Path,
    output: Path,
    model: str,
    theme: Optional[str] = None,
) -> None:
    async_playwright = _import_playwright()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
        )
        page = await context.new_page()

        # Forçar tema via localStorage ANTES de navegar
        if theme:
            await page.add_init_script(
                f"localStorage.setItem('theme', {theme!r});"
            )

        url = html_path.absolute().as_uri()
        await page.goto(url, wait_until="networkidle")

        # Para o deck: revelar todos os fragments e aguardar transições
        if model == "deck":
            await page.evaluate(
                """() => {
                    document.querySelectorAll('[data-fragment]').forEach(el => el.classList.add('is-visible'));
                    document.querySelectorAll('[data-anim]').forEach(el => {
                        el.style.opacity = '1';
                        el.style.transform = 'none';
                    });
                }"""
            )
            await page.wait_for_timeout(500)
            await page.pdf(
                path=str(output),
                format="A4",
                landscape=True,
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
        else:
            # No site, expandir todas as views para o PDF
            if model == "site":
                await page.evaluate(
                    """() => {
                        document.querySelectorAll('.view').forEach(v => {
                            v.classList.add('is-active');
                            v.hidden = false;
                            v.style.opacity = '1';
                        });
                    }"""
                )
            # No hub, abrir todos os painéis
            elif model == "hub":
                await page.evaluate(
                    """() => {
                        document.querySelectorAll('.panel').forEach(p => p.classList.add('is-open'));
                    }"""
                )
            # Forçar reveals
            await page.evaluate(
                """() => {
                    document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('is-visible'));
                }"""
            )
            await page.wait_for_timeout(300)
            await page.pdf(
                path=str(output),
                format="A4",
                landscape=False,
                print_background=True,
                margin={"top": "20mm", "right": "15mm", "bottom": "20mm", "left": "15mm"},
            )

        await browser.close()


async def export_screenshots(
    html_path: Path,
    output_dir: Path,
    model: str,
    theme: Optional[str] = None,
) -> None:
    async_playwright = _import_playwright()
    output_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        viewport = (
            {"width": 1920, "height": 1080}
            if model == "deck"
            else {"width": 1440, "height": 900}
        )
        context = await browser.new_context(viewport=viewport)
        page = await context.new_page()

        if theme:
            await page.add_init_script(f"localStorage.setItem('theme', {theme!r});")

        url = html_path.absolute().as_uri()
        await page.goto(url, wait_until="networkidle")

        if model == "deck":
            slides = await page.locator(".slide").count()
            for i in range(slides):
                await page.evaluate(f"() => goto({i})")
                # Revelar fragments
                await page.evaluate(
                    """() => {
                        document.querySelectorAll('.slide.is-active [data-fragment]').forEach(el => el.classList.add('is-visible'));
                    }"""
                )
                await page.wait_for_timeout(800)
                await page.screenshot(
                    path=str(output_dir / f"s{i+1:02d}.png"),
                    full_page=False,
                )
        else:
            # Para os demais: 1 PNG por h2 (full-page com scroll)
            await page.evaluate(
                """() => {
                    document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('is-visible'));
                }"""
            )
            h2s = await page.locator("h2[id]").all()
            for i, h in enumerate(h2s):
                await h.scroll_into_view_if_needed()
                await page.wait_for_timeout(300)
                hid = await h.get_attribute("id")
                await page.screenshot(
                    path=str(output_dir / f"{i+1:02d}-{hid}.png"),
                    full_page=False,
                )
            # E um PNG full-page geral
            await page.screenshot(path=str(output_dir / "00-full.png"), full_page=True)

        await browser.close()


async def amain(args) -> int:
    html_path = Path(args.file)
    if not html_path.exists():
        print(f"ERRO: arquivo não existe: {html_path}", file=sys.stderr)
        return 2

    html = html_path.read_text(encoding="utf-8")
    model = identify_model(html)
    if not model:
        print("ERRO: não foi possível identificar o modelo. O arquivo é slideless?", file=sys.stderr)
        return 2

    if args.mode == "pdf":
        out = Path(args.output) if args.output else html_path.with_suffix(".pdf")
        await export_pdf(html_path, out, model, theme=args.theme)
        print(f"PDF gerado: {out}")
    else:
        out = Path(args.output) if args.output else html_path.with_suffix("")
        await export_screenshots(html_path, out, model, theme=args.theme)
        print(f"Screenshots gerados em: {out}")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Exporta documento slideless para PDF ou PNGs")
    parser.add_argument("file", help="Caminho do .html")
    parser.add_argument("--mode", choices=["pdf", "screenshots"], default="pdf")
    parser.add_argument("--output", help="Caminho do PDF ou diretório de screenshots")
    parser.add_argument("--theme", choices=["light", "dark"], help="Força tema antes de renderizar")
    args = parser.parse_args()

    try:
        return asyncio.run(amain(args))
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
