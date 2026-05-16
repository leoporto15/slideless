# Tema `itau`

Tema corporativo Itaú. Default da skill quando o usuário não especificar tema.

**CSS:** [../../assets/temas/itau.css](../../assets/temas/itau.css).

---

## Identidade

- **Accent primário:** laranja oficial `#FF6200` no light, laranja luminoso `#FA9F09` no dark.
- **Fontes:** Itaú Display (headings) + Itaú Text (corpo). Fallback Inter (Google Fonts) — nunca falhar por fonte.
- **Background light:** branco com warm cast (off-white `#faf8f5` para elementos elevados).
- **Background dark:** preto quente `#14110d` (NÃO preto puro `#000000`) — bege/marrom escuro, identidade Itaú.
- **Cores semânticas:** info usa azul Itaú (`#3B85FA`), warn usa amarelo Itaú (`#FBC305`).

---

## Tokens (resumo)

Definição completa em [../../assets/temas/itau.css](../../assets/temas/itau.css). Tokens-chave:

| Token | Light | Dark |
|---|---|---|
| `--color-accent` | `#FF6200` | `#FA9F09` |
| `--color-bg` | `#ffffff` | `#14110d` |
| `--color-bg-elevated` | `#faf8f5` | `#1c1814` |
| `--color-fg` | `#1a1a1a` | `#e8eaed` |
| `--color-fg-muted` | `#525252` | `#a8a39a` |
| `--color-border` | `#e8e4dd` | `#2f2a23` |
| `--font-display` | `'Itau Display', 'Inter', ...` | mesmo |
| `--font-text` | `'Itau Text', 'Inter', ...` | mesmo |

Tokens fixos (não mudam com tema):
- `--itau-orange: #FF6200`
- `--itau-orange-2: #F88104`
- `--itau-orange-3: #FA9F09`
- `--itau-blue-3: #3B85FA`
- `--itau-yellow: #FBC305`

---

## Aplicação

Toda geração com tema `itau` deve:

1. Incluir tokens inline no `<style>` do HTML (copiar `assets/temas/itau.css` inteiro).
2. Carregar Inter via Google Fonts (fallback obrigatório):
   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com">
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
   ```
   No `deck`, adicionar peso 800: `family=Inter:wght@400;500;600;700;800`.
3. Boot script de tema no `<head>` (ver [../design-system.md](../design-system.md#boot-script)).
4. Theme toggle no header.
5. Logo Itaú no `topbar__logo` (caminho `assets/logos/itau.png` — embarcar via base64 ou usar emoji `🟠` como fallback se logo indisponível).

---

## Anti-patterns do tema `itau`

- **Não use `#000000` como bg dark.** Use `#14110d` (preto quente).
- **Não use laranja em fundo amarelo** (contraste insuficiente).
- **Não use cor de marca para decoração estrutural** — laranja é accent (links, CTA, headings hover, número da seção). Bordas são `--color-border`, não laranja.
- **Não use fonte sem fallback.** Sempre `'Itau Display', 'Inter', system-ui` (não confiar que a fonte interna está disponível fora da rede Itaú).

---

## Quando usar `itau` vs `neutro`

| Cenário | Tema |
|---|---|
| Default — qualquer comunicação interna oficial | `itau` |
| Documento que vai para fora do Itaú (parceiros, fornecedores) | `neutro` |
| Documento institucional/regulatório (sem brand) | `neutro` |
| Material que será co-branded ou white-labeled | `neutro` |
| Documento experimental/draft | indiferente — `itau` por default |
