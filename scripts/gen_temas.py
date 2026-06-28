#!/usr/bin/env python3
"""
slideless - gen_temas.py

Gera os 6 temas itau a partir de itau-base.css (base estrutural provada),
trocando o canvas aprovado e ANEXANDO as camadas de cor novas, todas
derivadas em OKLCH (colorkit.py):

  - accent-text   : laranja escurecida p/ TEXTO pequeno em canvas claro (AA 4.5);
                    = laranja da marca em canvas escuro (ja passa).
  - secondary(+dim): par cromatico de SUPORTE por tema (papel = dado/realce
                    secundario, subordinado ao laranja).
  - cat-1..6      : paleta CATEGORICA de grafico, contraste garantido vs o
                    canvas do tema; 1=laranja(tese). 1-3 CVD-safe por cor.
  - seq-1..5      : escala SEQUENCIAL (magnitude), 1 matiz (laranja).
  - div-1..5      : escala DIVERGENTE laranja<->azul (CVD-safe), 3=neutro.

Canvas invertido (navy/grafite/aco: :root ja e escuro) recebe a paleta
SEMANTICA dark no :root (senao success/teal/plum ficam ilegiveis — medido).

Uso:  python scripts/gen_temas.py [--check]   (--check: so relatorio, nao escreve)
"""
import re
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import colorkit as ck

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "assets" / "temas" / "itau-base.css"
O, OH = "var(--itau-orange)", "var(--itau-orange-2)"

# ─── Canvas aprovado + fixes (accent-fg escuro nos light; fg-subtle ≥3) ───
def Ld(bg, el, su, fg, fm, fs, bd, bds, ad, afg):
    return dict(zip(["color-bg","color-bg-elevated","color-bg-sunken","color-fg",
        "color-fg-muted","color-fg-subtle","color-border","color-border-strong",
        "color-accent","color-accent-dim","color-accent-fg","color-accent-hover"],
        [bg,el,su,fg,fm,fs,bd,bds,O,ad,afg,OH]))
def Dd(bg, el, su, fg, fm, fs, bd, bds, afg, ad):
    return dict(zip(["color-bg","color-bg-elevated","color-bg-sunken","color-fg",
        "color-fg-muted","color-fg-subtle","color-border","color-border-strong",
        "color-accent","color-accent-hover","color-accent-fg","color-accent-dim"],
        [bg,el,su,fg,fm,fs,bd,bds,O,OH,afg,ad]))

THEMES = {
 "itau-padrao": dict(sec=255, light=Ld("#F1F2F4","#FFFFFF","#E3E5E8","#1A1D21","#4C4C4C","#6E6E6E","rgba(26,29,33,0.10)","rgba(26,29,33,0.18)","rgba(255,98,0,0.08)","#15181C"),
                     dark=Dd("#15181C","#1D2127","#101317","#E6E7E4","#A3A8AD","#70767D","rgba(230,231,228,0.12)","rgba(230,231,228,0.22)","#15181C","rgba(255,98,0,0.12)")),
 "itau-navy":   dict(sec=85,  light=Ld("#000D3C","#0A1A52","#00081F","#EAEEF6","#A9B4CC","#6E7A96","rgba(234,238,246,0.12)","rgba(234,238,246,0.22)","rgba(255,98,0,0.14)","#000D3C"),
                     dark=Dd("#00081F","#000D3C","#00040F","#EAEEF6","#A9B4CC","#6E7A96","rgba(234,238,246,0.14)","rgba(234,238,246,0.24)","#00081F","rgba(255,98,0,0.16)")),
 "itau-grafite":dict(sec=70,  light=Ld("#1E1C1A","#28241F","#161412","#ECE6DD","#B0A79B","#7F7669","rgba(236,230,221,0.12)","rgba(236,230,221,0.22)","rgba(255,98,0,0.12)","#1E1C1A"),
                     dark=Dd("#161412","#1F1C18","#100E0C","#ECE6DD","#B0A79B","#7F7669","rgba(236,230,221,0.14)","rgba(236,230,221,0.24)","#161412","rgba(255,98,0,0.14)")),
 "itau-aco":    dict(sec=200, light=Ld("#1E242C","#28303A","#161B21","#E8ECF1","#A3ADB9","#6E7782","rgba(232,236,241,0.12)","rgba(232,236,241,0.22)","rgba(255,98,0,0.12)","#1E242C"),
                     dark=Dd("#161B21","#1E242C","#0F1318","#E8ECF1","#A3ADB9","#6E7782","rgba(232,236,241,0.14)","rgba(232,236,241,0.24)","#161B21","rgba(255,98,0,0.14)")),
 "itau-areia":  dict(sec=248, light=Ld("#ECE4D5","#F6F1E7","#E0D6C4","#2A2620","#6E6356","#7C7163","rgba(42,38,32,0.12)","rgba(42,38,32,0.20)","rgba(255,98,0,0.08)","#1F1B16"),
                     dark=Dd("#1F1B16","#2A2419","#15120D","#EFE7D8","#C0B4A0","#8A7E6C","rgba(239,231,216,0.12)","rgba(239,231,216,0.22)","#1F1B16","rgba(255,98,0,0.12)")),
 "itau-bruma":  dict(sec=210, light=Ld("#E7ECF2","#FFFFFF","#D8DFE8","#1B2430","#566270","#69748A","rgba(27,36,48,0.10)","rgba(27,36,48,0.18)","rgba(255,98,0,0.08)","#141A22"),
                     dark=Dd("#141A22","#1C232D","#0E1218","#E7ECF2","#A3AEBC","#6E7884","rgba(231,236,242,0.12)","rgba(231,236,242,0.22)","#141A22","rgba(255,98,0,0.12)")),
}

# ─── Paleta categorica (locked): nome,H,C, L_claro, L_escuro ─────────────
CAT = [("orange",42,0.17,0.60,0.74),("blue",255,0.15,0.50,0.71),("teal",190,0.11,0.63,0.86),
       ("gold",88,0.14,0.45,0.84),("green",140,0.125,0.53,0.66),("indigo",268,0.12,0.40,0.62)]

def is_dark(bg):
    return ck.luminance(ck.hex_to_rgb(bg)) < 0.35

def fit(H, C, L, bg, target):
    dark = is_dark(bg)
    last = ck.oklch_hex(L, C, H)
    for _ in range(70):
        last = ck.oklch_hex(L, C, H)
        if ck.contrast(last, bg) >= target:
            return last
        L = min(0.93, L + 0.012) if dark else max(0.30, L - 0.012)
    return last

def rgba_of(hexc, a):
    r, g, b = ck.hex_to_rgb(hexc)
    return f"rgba({r},{g},{b},{a})"

def cat_palette(bg):
    d = is_dark(bg)
    return [fit(H, C, (Ld_ if d else Ll), bg, 3.0) for _, H, C, Ll, Ld_ in CAT]

def seq_palette(bg):
    # sequencial laranja (magnitude). fills — rampa perceptual.
    d = is_dark(bg)
    Ls = [0.34,0.46,0.58,0.70,0.82] if d else [0.90,0.78,0.66,0.55,0.45]
    Cs = [0.07,0.11,0.15,0.18,0.19] if d else [0.05,0.10,0.15,0.18,0.19]
    return [ck.oklch_hex(Ls[i], Cs[i], 42) for i in range(5)]

def div_palette(bg):
    # divergente laranja(1-2) <-> neutro(3) <-> azul(4-5). CVD-safe.
    d = is_dark(bg)
    if d:
        specs = [(0.70,0.17,42),(0.56,0.10,42),(0.52,0.012,250),(0.60,0.09,255),(0.74,0.15,255)]
    else:
        specs = [(0.56,0.18,42),(0.75,0.10,42),(0.72,0.012,250),(0.72,0.09,255),(0.52,0.16,255)]
    return [ck.oklch_hex(L, C, H) for L, C, H in specs]

def accent_text(bg):
    if is_dark(bg):
        return O                      # laranja da marca ja passa (>5) no escuro
    return fit(42.3, 0.19, 0.55, bg, 4.6)   # laranja escurecida p/ texto pequeno

def secondary(bg, H):
    return fit(H, 0.13, 0.72 if is_dark(bg) else 0.52, bg, 4.5)

def new_tokens(bg, secH):
    sec = secondary(bg, secH)
    cat = cat_palette(bg); seq = seq_palette(bg); div = div_palette(bg)
    t = {
        "color-accent-text": accent_text(bg),
        "color-secondary": sec,
        "color-secondary-dim": rgba_of(sec, 0.12),
    }
    for i, c in enumerate(cat, 1): t[f"cat-{i}"] = c
    for i, c in enumerate(seq, 1): t[f"seq-{i}"] = c
    for i, c in enumerate(div, 1): t[f"div-{i}"] = c
    return t

# ─── Semantica dark p/ canvas invertido (:root vira dark) ────────────────
SEM_DARK = {  # light_value -> dark_value (hex/rgba/oklch)
 "#3f6f1f":"#8fcc5a", "#0f766e":"#6fd0c0", "#9f1239":"#e8889c", "#b91c1c":"#f87171",
 "#16a34a":"#4ade80",
 "rgba(63, 111, 31, 0.08)":"rgba(143, 204, 90, 0.10)",
 "rgba(15, 118, 110, 0.08)":"rgba(111, 208, 192, 0.10)",
 "rgba(159, 18, 57, 0.08)":"rgba(232, 136, 156, 0.10)",
 "rgba(185, 28, 28, 0.08)":"rgba(248, 113, 113, 0.10)",
 "rgba(59, 133, 250, 0.08)":"rgba(59, 133, 250, 0.12)",
 "oklch(52% 0.11 140)":"oklch(76% 0.13 140)",
 "oklch(52% 0.08 200)":"oklch(78% 0.09 195)",
 "oklch(46% 0.12 355)":"oklch(74% 0.11 0)",
 "oklch(50% 0.16 27)":"oklch(70% 0.15 25)",
 "oklch(52% 0.11 140 / 0.08)":"oklch(76% 0.13 140 / 0.10)",
 "oklch(52% 0.08 200 / 0.08)":"oklch(78% 0.09 195 / 0.10)",
 "oklch(46% 0.12 355 / 0.08)":"oklch(74% 0.11 0 / 0.10)",
 "oklch(50% 0.16 27 / 0.08)":"oklch(70% 0.15 25 / 0.10)",
}

def scope_bounds(css, marker):
    i = css.index(marker); j = css.index('{', i); d = 0; k = j
    while k < len(css):
        if css[k] == '{': d += 1
        elif css[k] == '}':
            d -= 1
            if d == 0: break
        k += 1
    return j, k  # indices da abertura { e do fechamento }

def repl_scope(css, marker, tokens, append):
    j, k = scope_bounds(css, marker)
    block = css[j:k + 1]
    for tok, val in tokens.items():
        block, n = re.subn(r'(--' + re.escape(tok) + r'\s*:\s*)[^;]+;', r'\g<1>' + val + ';', block, count=1)
        if n == 0:
            block = block[:-1] + f"  --{tok}: {val};\n}}"  # define se ausente
    if append:
        ins = "\n  /* ─── camada de cor gerada (gen_temas.py) ─── */\n" + \
              "".join(f"  --{t}: {v};\n" for t, v in append.items())
        block = block[:-1] + ins + "}"
    return css[:j] + block + css[k + 1:]

def generate(name, spec, base):
    css = base
    css = repl_scope(css, ":root {", spec["light"], new_tokens(spec["light"]["color-bg"], spec["sec"]))
    css = repl_scope(css, '[data-theme="dark"]', spec["dark"], new_tokens(spec["dark"]["color-bg"], spec["sec"]))
    # Canvas invertido (navy/grafite/aco: :root ja e escuro): troca a paleta
    # SEMANTICA para a versao dark. Cada valor light so existe no :root e no
    # @supports :root — o bloco [data-theme=dark] ja usa os valores dark —,
    # entao um replace global flipa exatamente :root + @supports:root, intacto o dark.
    if is_dark(spec["light"]["color-bg"]):
        for a, b in SEM_DARK.items():
            css = css.replace(a, b)
    return (f"/* slideless — tema {name}. Gerado por gen_temas.py de itau-base.css.\n"
            f"   NAO editar a mao: rode `python scripts/gen_temas.py`. */\n") + css

def _scope_tokens(css, marker):
    j, k = scope_bounds(css, marker)
    return {a: b.strip() for a, b in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", css[j:k + 1])}

def verify():
    """Gate DURO sobre os arquivos de tema em disco: contraste AA dos tokens de
    texto/serie vs canvas + CVD do par cat-1/cat-2. Exit 1 se algo falhar."""
    import json
    HEXP = re.compile(r"^#[0-9a-fA-F]{6}$")
    reg = json.loads((ROOT / "assets" / "temas" / "temas.json").read_text(encoding="utf-8"))
    fails = 0
    for name in reg["temas"]:
        css = (ROOT / "assets" / "temas" / f"{name}.css").read_text(encoding="utf-8")
        for label, marker in (("light", ":root {"), ("dark", '[data-theme="dark"]')):
            t = _scope_tokens(css, marker)
            bg = t.get("--color-bg", "")
            if not HEXP.match(bg):
                continue
            checks = [("--color-fg", 4.5), ("--color-fg-muted", 4.5), ("--color-fg-subtle", 3.0),
                      ("--color-accent-text", 4.5)] + [(f"--cat-{i}", 3.0) for i in range(1, 7)]
            for tok, thr in checks:
                v = t.get(tok, "")
                if not HEXP.match(v):
                    continue
                cr = ck.contrast(v, bg)
                if cr < thr:
                    print(f"  XX {name:13} {label:5} {tok}={v} / {bg} = {cr:.2f} < {thr}")
                    fails += 1
            c1, c2 = t.get("--cat-1", ""), t.get("--cat-2", "")
            if HEXP.match(c1) and HEXP.match(c2):
                d = ck.delta_ok_cvd(c1, c2)
                if d < 0.15:
                    print(f"  XX {name:13} {label:5} cat-1/cat-2 CVD Δok={d:.3f} < 0.15")
                    fails += 1
    print("VERIFY:", "PASS — todos os temas passam AA + CVD do par primario" if fails == 0 else f"FAIL ({fails})")
    return 0 if fails == 0 else 1

def main():
    if "--verify" in sys.argv:
        sys.exit(verify())
    check = "--check" in sys.argv
    base = BASE.read_text(encoding="utf-8")
    if check:
        for name, spec in THEMES.items():
            for sc in ("light", "dark"):
                bg = spec[sc]["color-bg"]
                at = accent_text(bg); cat = cat_palette(bg)
                atc = ck.contrast(at if at != O else "#FF6200", bg)
                print(f"{name:13} {sc:5} bg={bg:8} accent-text={('marca' if at==O else at)}({atc:.2f}) "
                      f"sec={secondary(bg,spec['sec'])}({ck.contrast(secondary(bg,spec['sec']),bg):.2f}) "
                      f"cat1={cat[0]} catMinC={min(ck.contrast(c,bg) for c in cat):.2f}")
        return
    for name, spec in THEMES.items():
        out = ROOT / "assets" / "temas" / f"{name}.css"
        out.write_text(generate(name, spec, base), encoding="utf-8")
        print(f"OK {name}.css")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
