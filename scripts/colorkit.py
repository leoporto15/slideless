#!/usr/bin/env python3
"""
slideless - colorkit.py

Matematica de cor compartilhada (stdlib puro) para:
  - gerar paletas de tema/grafico em OKLCH (derivacao perceptual)
  - checar contraste WCAG e distinguibilidade sob daltonismo (validar.py)

OKLab/OKLCH: Bjorn Ottosson (https://bottosson.github.io/posts/oklab/).
Simulacao de CVD: matrizes Machado et al. (2009), severidade 1.0.
Sem dependencias externas — roda em harness restrito.
"""
import math

# ─── sRGB <-> hex ────────────────────────────────────────────────────────
def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c))):02X}" for c in rgb)

# ─── sRGB <-> linear ─────────────────────────────────────────────────────
def _s2l(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def _l2s(c):
    c = max(0.0, min(1.0, c))
    v = c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return v * 255.0

# ─── linear sRGB <-> OKLab ───────────────────────────────────────────────
def linrgb_to_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)

def oklab_to_linrgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (+4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)

def rgb_to_oklab(rgb):
    return linrgb_to_oklab(*(_s2l(c) for c in rgb))

def rgb_to_oklch(rgb):
    L, a, b = rgb_to_oklab(rgb)
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a)) % 360
    return (L, C, H)

def _in_gamut(lin, eps=1e-4):
    return all(-eps <= c <= 1 + eps for c in lin)

def oklch_to_rgb(L, C, H):
    """OKLCH -> sRGB 0-255, reduzindo croma ate caber no gamut sRGB."""
    h = math.radians(H)
    c = C
    for _ in range(40):
        a, b = c * math.cos(h), c * math.sin(h)
        lin = oklab_to_linrgb(L, a, b)
        if _in_gamut(lin):
            break
        c *= 0.94  # reduz croma, preserva L e H
    return tuple(_l2s(x) for x in lin)

def oklch_hex(L, C, H):
    return rgb_to_hex(oklch_to_rgb(L, C, H))

# ─── Contraste WCAG ──────────────────────────────────────────────────────
def luminance(rgb):
    r, g, b = (_s2l(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    """a, b = hex ou rgb-tuple."""
    if isinstance(a, str):
        a = hex_to_rgb(a)
    if isinstance(b, str):
        b = hex_to_rgb(b)
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

# ─── Distancia perceptual (OKLab) ────────────────────────────────────────
def delta_ok(a, b):
    if isinstance(a, str):
        a = hex_to_rgb(a)
    if isinstance(b, str):
        b = hex_to_rgb(b)
    la = rgb_to_oklab(a)
    lb = rgb_to_oklab(b)
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(la, lb)))

# ─── Simulacao de daltonismo (Machado 2009, sev 1.0, em linear RGB) ──────
_CVD = {
    "deuteranopia": ((0.367322, 0.860646, -0.227968),
                     (0.280085, 0.672501, 0.047413),
                     (-0.011820, 0.042940, 0.968881)),
    "protanopia": ((0.152286, 1.052583, -0.204868),
                   (0.114503, 0.786281, 0.099216),
                   (-0.003882, -0.048116, 1.051998)),
}

def simulate_cvd(rgb, kind="deuteranopia"):
    if isinstance(rgb, str):
        rgb = hex_to_rgb(rgb)
    lin = [_s2l(c) for c in rgb]
    M = _CVD[kind]
    out = [sum(M[i][j] * lin[j] for j in range(3)) for i in range(3)]
    return tuple(_l2s(c) for c in out)

def delta_ok_cvd(a, b, kind="deuteranopia"):
    return delta_ok(simulate_cvd(a, kind), simulate_cvd(b, kind))


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    # Validacao: a laranja da marca round-trip
    o = "#FF6200"
    L, C, H = rgb_to_oklch(hex_to_rgb(o))
    print(f"laranja {o} -> oklch({L:.3f} {C:.3f} {H:.1f})")
    print(f"  oklch->hex de volta: {oklch_hex(L, C, H)}  (esperado ~{o})")
    print(f"  contraste vs branco: {contrast(o, '#FFFFFF'):.2f}  vs preto: {contrast(o, '#000000'):.2f}")
    # info azul + verde semantico
    for nm, hx in [("blue", "#3B85FA"), ("teal", "#0f766e"), ("green", "#3f6f1f")]:
        Lc, Cc, Hc = rgb_to_oklch(hex_to_rgb(hx))
        print(f"{nm:5} {hx} -> oklch({Lc:.3f} {Cc:.3f} {Hc:.1f})")
    print(f"deltaOK laranja vs verde normal: {delta_ok('#FF6200', '#3f6f1f'):.3f}"
          f"  | sob deuteranopia: {delta_ok_cvd('#FF6200', '#3f6f1f'):.3f}")
