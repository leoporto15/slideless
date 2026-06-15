#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
smoke.py — teste de RENDER do documento gerado.

O validador determinístico (validar.py) checa a ESTRUTURA, mas não vê erro de
runtime (JS que não parseia) nem quebra visual. Esta sessão de polish provou que
um <script> aninhado matava TODO o JS em silêncio, e o validador passava.

Este script carrega o HTML num Chromium headless, captura console.error/pageerror,
e confere que o conteúdo aparece de fato. É a rede que faltava.

Requer:  pip install playwright  &&  python -m playwright install chromium
Uso:     python scripts/smoke.py outputs/meu-doc.html
Exit:    0 = PASS (ou playwright ausente → SKIP), 1 = FAIL.
"""
import sys
import pathlib


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if len(sys.argv) < 2:
        print("uso: python scripts/smoke.py <arquivo.html>", file=sys.stderr)
        return 2
    f = pathlib.Path(sys.argv[1])
    if not f.exists():
        print(f"não existe: {f}", file=sys.stderr)
        return 2

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("SKIP: playwright não instalado — `pip install playwright && python -m playwright install chromium`")
        return 0

    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 800})
        pg.on("pageerror", lambda e: errs.append(f"PAGEERROR: {e}"))
        pg.on("console", lambda m: errs.append(f"console.error: {m.text}") if m.type == "error" else None)
        try:
            pg.goto(f.resolve().as_uri(), wait_until="networkidle", timeout=15000)
        except Exception as e:
            errs.append(f"GOTO-FAIL: {e}")
        pg.wait_for_timeout(1200)
        info = pg.evaluate("""() => ({
            h: document.body.scrollHeight,
            txt: (document.body.innerText || '').trim().length,
            visHead: [...document.querySelectorAll('h1,h2,h3')].filter(e => e.offsetParent).length,
            ph: /\\{\\{[A-Z_]+\\}\\}|\\bBRAND\\b|TÍTULO DO/.test(document.body.innerText || '')
        })""")
        # ─── quebras VISUAIS que a estrutura não vê ───────────────────────────
        # sel curto pra um nó, p/ relatório legível
        pg.evaluate(r"""() => { window.__scan = () => {
            const W = innerWidth, H = innerHeight;
            const sel = el => {
              const c = (el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className) || '';
              const cls = String(c).trim().split(/\s+/).filter(Boolean).slice(0,2).map(x => '.'+x).join('');
              return el.tagName.toLowerCase() + cls;
            };
            // conteúdo clipado por algum ancestral não "sangra" de fato (slide-bg,
            // aurora-mesh, trilho de marquee vivem dentro de overflow:hidden/clip).
            const clipped = el => {
              for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
                const o = getComputedStyle(p).overflowX;
                if (o === 'hidden' || o === 'clip' || o === 'auto' || o === 'scroll') return true;
              }
              return false;
            };
            const cn = el => ' ' + (typeof el.className === 'string' ? el.className : '') + ' ';
            const seen = new Set(), out = {overflow: [], narrow: [], reel: [], dup: []};
            // colunas laterais (handbook/site): conteúdo que as invade = bug de bleed
            // só RAILS laterais (altos + ao lado) contam — exclui índice de topo do report
            const colR = [...document.querySelectorAll('.toc, aside.toc')]
              .map(e => e.getBoundingClientRect())
              .filter(r => r.width > 40 && r.height > innerHeight*0.5 && r.left > innerWidth*0.45);
            const colL = [...document.querySelectorAll('.sidebar, aside.sidebar')]
              .map(e => e.getBoundingClientRect())
              .filter(r => r.width > 40 && r.height > innerHeight*0.5 && r.right < innerWidth*0.55);
            for (const el of document.querySelectorAll('body *')) {
              if (!el.offsetParent && el.tagName !== 'TABLE') continue;
              const cs = getComputedStyle(el);
              if (cs.visibility === 'hidden' || cs.display === 'none' || cs.position === 'fixed') continue;
              const r = el.getBoundingClientRect();
              if (r.width < 1 || r.height < 1) continue;
              // (1) conteúdo invade a coluna do TOC/sidebar (bleed overshoot)
              const inContent = el.closest('.content, .content__inner, .report-body, main');
              const isCol = el.closest('.toc, .sidebar');
              if (inContent && !isCol && r.width > 80 && !clipped(el)) {
                for (const c of colR) if (r.right > c.left + 6 && r.left < c.left) {
                  const k = sel(el);
                  if (!seen.has('x'+k)) { seen.add('x'+k);
                    out.overflow.push(`${k} invade o TOC (right=${Math.round(r.right)} > toc=${Math.round(c.left)})`); }
                }
                for (const c of colL) if (r.left < c.right - 6 && r.right > c.right) {
                  const k = sel(el);
                  if (!seen.has('xl'+k)) { seen.add('xl'+k);
                    out.overflow.push(`${k} invade a sidebar (left=${Math.round(r.left)} < ${Math.round(c.right)})`); }
                }
              }
              // (2) sangra a viewport pela direita (só se não for clipado)
              if (r.right > W + 12 && r.width > 40 && r.width < W*1.5 && !clipped(el)) {
                const k = sel(el);
                if (!seen.has('v'+k)) { seen.add('v'+k);
                  out.overflow.push(`${k} sangra→ (right=${Math.round(r.right)}>${W})`); }
              }
              // (2b) tabela mais larga que a viewport = cortada no slide / vaza no doc
              if (el.tagName === 'TABLE' && r.width > W + 12) {
                const k = sel(el);
                if (!seen.has('t'+k)) { seen.add('t'+k);
                  out.overflow.push(`${k} maior que a viewport (${Math.round(r.width)}>${W}px)`); }
              }
              // (3) coluna de texto estreita demais => quebra por-caractere
              const txt = (el.childNodes.length && [...el.childNodes].some(n => n.nodeType===3 && n.textContent.trim().length>20));
              if (txt && r.width < 60 && el.scrollHeight > r.width * 3) {
                const k = sel(el);
                if (!seen.has('n'+k)) { seen.add('n'+k);
                  out.narrow.push(`${k} (w=${Math.round(r.width)}px, texto vertical?)`); }
              }
              // (4) odômetro/reel não-clipado: caixa muito mais alta que 1 linha
              //     (NÃO inclui .choreo — é bloco multi-linha legítimo)
              if (/\bodometer\b|\bod-digit\b/.test(cn(el))) {
                const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize)*1.2 || 16;
                if (r.height > lh * 2.2) {
                  const k = sel(el);
                  if (!seen.has('r'+k)) { seen.add('r'+k);
                    out.reel.push(`${k} (h=${Math.round(r.height)}px vs linha≈${Math.round(lh)}px — coluna 0-9?)`); }
                }
              }
              // (5) número duplicado: ::after usa counter() E o elemento JÁ tem
              //     nó de texto com dígitos => render "7070" (W25/choreo duplicado).
              //     (Chromium devolve 'counter(n)' literal, daí o teste estrutural.)
              const csA = getComputedStyle(el, '::after');
              const aft = csA.content || '';
              // overlay legítimo: texto transparente OU ::after absoluto (sobreposto)
              // não duplica visualmente — só flag quando AMBOS rolam no fluxo normal.
              const overlay = csA.position === 'absolute'
                || /rgba?\([^)]*,\s*0(\.0+)?\)/.test(cs.color)
                || cs.color === 'transparent';
              if (/counter\(/.test(aft) && !overlay) {
                const t0 = [...el.childNodes].filter(n => n.nodeType === 3)
                  .map(n => n.textContent).join('').replace(/\D/g, '');
                if (t0.length) {
                  const k = sel(el);
                  if (!seen.has('d'+k)) { seen.add('d'+k);
                    out.dup.push(`${k} (texto "${t0}" + ::after counter = duplicado)`); }
                }
              }
            }
            // (6) página rola horizontalmente = algo vaza a tela de fato
            const de = document.scrollingElement || document.documentElement;
            if (de.scrollWidth - innerWidth > 4) {
              out.overflow.push(`PÁGINA rola horizontal (${de.scrollWidth}>${innerWidth}px)`);
            }
            return out;
        }; }""")
        visual = pg.evaluate("window.__scan()")
        visual.setdefault("short", [])
        # slide que não preenche a viewport (capa de overdrive colapsada etc.)
        short_js = """() => { const s=document.querySelector('.slide.is-active');
            if(!s) return null; const r=s.getBoundingClientRect();
            return r.height < innerHeight*0.85 && r.width>200
              ? `slide ${s.dataset.slide||'?'} só ${Math.round(r.height)}px de ${innerHeight}px` : null; }"""
        # deck: percorre os slides, escaneando CADA slide ativo (os bugs reais
        # — odômetro, tabela vazando — vivem em slides depois da capa)
        is_deck = pg.evaluate("!!document.querySelector('.slide[data-slide]')")
        if is_deck:
            sh = pg.evaluate(short_js)
            if sh and sh not in visual["short"]:
                visual["short"].append(sh)
            n_slides = pg.evaluate("document.querySelectorAll('.slide[data-slide]').length")
            for _ in range(min(max(n_slides - 1, 1), 40)):
                pg.keyboard.press("ArrowRight")
                pg.wait_for_timeout(160)
                more = pg.evaluate("window.__scan()")
                for k in ("overflow", "narrow", "reel", "dup"):
                    for item in more.get(k, []):
                        if item not in visual[k]:
                            visual[k].append(item)
                sh = pg.evaluate(short_js)
                if sh and sh not in visual["short"]:
                    visual["short"].append(sh)
        b.close()

    fails = []
    if any("PAGEERROR" in e or "GOTO-FAIL" in e for e in errs):
        fails.append("erro de runtime — JS do documento quebrado")
    if info["txt"] < 50:
        fails.append(f"quase sem texto visível ({info['txt']} chars)")
    if info["visHead"] == 0:
        fails.append("nenhum heading visível (h1/h2/h3)")
    if info["ph"]:
        fails.append("placeholder renderizado ({{...}}/BRAND/TÍTULO)")
    if visual["reel"]:
        fails.append("odômetro não-clipado — coluna de dígitos visível: " + "; ".join(visual["reel"][:4]))
    if visual["dup"]:
        fails.append("número duplicado (counter + texto?): " + "; ".join(visual["dup"][:4]))
    if visual["narrow"]:
        fails.append("texto quebrando por-caractere (coluna estreita): " + "; ".join(visual["narrow"][:4]))
    if visual["overflow"]:
        fails.append("overflow/sangramento horizontal: " + "; ".join(visual["overflow"][:5]))
    if visual.get("short"):
        fails.append("slide não preenche a viewport: " + "; ".join(visual["short"][:4]))

    print(f"render: bodyH={info['h']}px  texto={info['txt']}ch  headings_visíveis={info['visHead']}")
    for e in errs[:10]:
        print("  " + e)
    if fails:
        print("SMOKE FAIL: " + "; ".join(fails))
        return 1
    print("SMOKE PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
