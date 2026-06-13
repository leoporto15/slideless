---
description: Adiciona uma seção a handbook, scrollytelling ou site existente
argument-hint: <título da seção> [após-seção-id]
---

Você foi invocado para adicionar uma seção a um documento slideless existente.

## Procedimento

1. Identificar o modelo do arquivo (lendo classes raiz: `.layout`+`.sidebar`→handbook; `.scrolly`→scrollytelling; `.view`→site).
2. **Não modelo `hub` nem `deck`** — para hub, use `adicionar-callout`/`adicionar-grafico` dentro do painel; para deck, use [adicionar-slide](adicionar-slide.md).
3. Slug do título (kebab-case, ASCII) → `id` da seção.
4. Inserir (sem `data-reveal` por padrão — texto corrido não anima):
   ```html
   <section id="<slug>">
     <h2>Título</h2>
     <p>Conteúdo.</p>
   </section>
   ```
   **Ressalva sobre `data-reveal`:** só adicionar em figuras/dados (`.figure`/`.chart-wrap`/`.metric`) e apenas se o perfil de `motion` do parti for `editorial`/`cinematico` e o teto de ≤40% das sections com reveal ainda não foi atingido. Em seção de texto corrido, nunca.
5. **Handbook:** também adicionar link na sidebar (`<li><a href="#<slug>">Título</a></li>`). TOC é gerada automaticamente.
6. **Scrollytelling:** apenas inserir a `.scene` na ordem narrativa.
7. **Site:** sempre dentro de uma `<article class="view">` específica — perguntar ao usuário em qual.
8. Rodar validador.

## Anti-patterns críticos

- Esquecer link na sidebar (handbook) — sidebar fica desatualizada.
- Adicionar h2 sem `id` ou `scroll-margin-top` — scrollspy quebra.
