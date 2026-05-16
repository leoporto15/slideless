# Tema `neutro`

Tema neutro com accent azul. Para documentos que vão para fora do Itaú, materiais sem brand, ou contextos onde a cor laranja não cabe.

**CSS:** [../../assets/temas/neutro.css](../../assets/temas/neutro.css).

---

## Identidade

- **Accent primário:** azul `#2563eb` no light, azul luminoso `#60a5fa` no dark.
- **Fontes:** Inter (Google Fonts) para corpo e headings. JetBrains Mono para código.
- **Background light:** branco puro `#ffffff`, elevado `#f8fafc` (frio, não warm).
- **Background dark:** azul-escuro `#0f172a` (slate), elevado `#1e293b`.
- **Cores semânticas:** info azul, tip verde, warn amarelo, danger vermelho — paleta neutra Tailwind-like.

---

## Tokens (resumo)

Definição completa em [../../assets/temas/neutro.css](../../assets/temas/neutro.css). Tokens-chave:

| Token | Light | Dark |
|---|---|---|
| `--color-accent` | `#2563eb` | `#60a5fa` |
| `--color-bg` | `#ffffff` | `#0f172a` |
| `--color-bg-elevated` | `#f8fafc` | `#1e293b` |
| `--color-fg` | `#0f172a` | `#e2e8f0` |
| `--color-fg-muted` | `#475569` | `#94a3b8` |
| `--color-border` | `#e2e8f0` | `#334155` |
| `--font-display` | `'Inter', ...` | mesmo |
| `--font-text` | `'Inter', ...` | mesmo |

Sem tokens `--itau-*`.

---

## Aplicação

1. Incluir tokens inline no `<style>` do HTML (copiar `assets/temas/neutro.css` inteiro).
2. Carregar Inter:
   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com">
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
   ```
3. Boot script de tema (mesmo que `itau`).
4. Theme toggle no header.
5. Sem logo Itaú no topbar. Pode usar marca neutra ("Squad X", "Equipe Y") ou nada.

---

## Anti-patterns do tema `neutro`

- **Não use laranja Itaú nem `--itau-*` tokens.** O tema é deliberadamente neutro.
- **Não use bege/warm tones no light.** Mantenha frio (slate/gray).
- **Não use preto puro** — `#0f172a` (slate-900) é mais sofisticado.

---

## Quando `neutro` faz mais sentido que `itau`

- Documento entregue a fornecedor / parceiro externo
- Material co-branded
- Tom técnico-neutro (release notes, postmortem público)
- Conteúdo experimental que vai virar produto separado
- Treinamento aberto / curso público
