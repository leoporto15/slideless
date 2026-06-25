#!/usr/bin/env python3
"""
slideless - scaffold.py

Monta o ESQUELETO de um documento slideless FORA do modelo de linguagem:
copia o template do modelo e injeta o tema no marker SLIDELESS:THEME.

Por que existe: o engine, o CSS de layout e o tema somam ~80% dos bytes de um
documento. Quando o LLM os REGURGITA na resposta (geracao monolitica), o gateway
do GitHub Copilot Chat estoura com 502/timeout. Com o scaffold, esses bytes sao
montados deterministicamente em disco e NUNCA passam pelo output do modelo.

Uso:
    python scripts/scaffold.py <modelo> <tema> <saida.html> [--force]

Ex.:
    python scripts/scaffold.py deck itau outputs/pitch-1t26.html

Depois do scaffold, o LLM SO preenche - com EDITS PEQUENOS, nunca o doc inteiro
numa unica resposta:
    1) kit tipografico no slot SLIDELESS:TYPE-KIT (<link> de references/type-kits.md)
       + bloco :root com os slots --kit-* ANTES do tema
    2) o bloco <!-- slideless:parti --> no <head>
    3) o conteudo, secao-a-secao / slide-a-slide
    4) validar:  python scripts/validar.py <saida.html>
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODELOS = ["deck", "handbook", "hub", "scrollytelling", "site", "report"]
TEMAS = ["itau", "neutro"]


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    ap = argparse.ArgumentParser(
        description="Monta o esqueleto slideless (template + tema) fora do LLM."
    )
    ap.add_argument("modelo", choices=MODELOS, help="modelo do documento")
    ap.add_argument("tema", choices=TEMAS, help="tema (itau ou neutro)")
    ap.add_argument("saida", help="caminho do HTML de saida (ex.: outputs/pitch.html)")
    ap.add_argument("--force", action="store_true", help="sobrescrever se ja existir")
    args = ap.parse_args()

    tpl = ROOT / "assets" / "templates" / f"template-{args.modelo}.html"
    css = ROOT / "assets" / "temas" / f"{args.tema}.css"
    out = pathlib.Path(args.saida)

    if not tpl.exists():
        sys.exit(f"ERRO: template nao encontrado: {tpl}")
    if not css.exists():
        sys.exit(f"ERRO: tema nao encontrado: {css}")
    if out.exists() and not args.force:
        sys.exit(f"ERRO: {out} ja existe (use --force para sobrescrever).")

    html = tpl.read_text(encoding="utf-8")
    theme = css.read_text(encoding="utf-8")

    # 1) remove PRIMEIRO o comentario-doc do topo (instrucoes de dev; nao vao pro
    #    produto) -- ele tambem MENCIONA "/* SLIDELESS:THEME */", entao tem que sair
    #    antes da injecao, senao o regex casaria a mencao em vez do marker real.
    html = re.sub(
        r"(<!DOCTYPE html>\s*)<!--\s*Template:[\s\S]*?-->\s*", r"\1", html, count=1
    )

    # 2) injeta o tema no marker real SLIDELESS:THEME (comentario CSS auto-contido no <style>)
    marker = re.compile(r"/\*\s*SLIDELESS:THEME[\s\S]*?\*/")
    if not marker.search(html):
        sys.exit(f"ERRO: marker SLIDELESS:THEME ausente em {tpl.name} (template malformado).")
    banner = (
        f"/* === TEMA {args.tema}: injetado por scaffold.py. "
        f"NAO regurgitar; editar so a camada [DIRECAO] se o parti pedir. === */"
    )
    html = marker.sub(lambda _m: banner + "\n" + theme, html, count=1)

    # 3) sanity: o marker tem que ter sido consumido (tema realmente entrou no <style>)
    if "SLIDELESS:THEME" in html:
        sys.exit("ERRO: marker SLIDELESS:THEME nao foi consumido (injecao do tema falhou).")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

    kb = len(html.encode("utf-8")) // 1024
    print(f"OK  esqueleto montado: {out}  (~{kb} KB ja prontos -- NAO passaram pelo LLM)")
    print(f"    tema '{args.tema}' injetado no <style>; engine+layout de '{args.modelo}' ja vem do template.")
    print("    Agora preencha com EDITS PEQUENOS (NUNCA o documento inteiro numa resposta):")
    print("      1) kit no slot SLIDELESS:TYPE-KIT (<link> de references/type-kits.md) + :root --kit-* antes do tema")
    print("      2) bloco <!-- slideless:parti --> no <head>")
    print("      3) conteudo secao-a-secao / slide-a-slide (um chunk por edit)")
    print(f"      4) python scripts/validar.py {out}")


if __name__ == "__main__":
    main()
