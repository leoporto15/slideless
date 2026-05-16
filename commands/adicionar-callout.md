---
description: Insere callout (info/tip/warn/danger) em um documento slideless
argument-hint: <tipo> [seção-id] [título]
---

Você foi invocado para adicionar callout.

## Tipos

| Tipo | Quando |
|---|---|
| `info` | Informação adicional, contexto |
| `tip` | Sugestão, atalho, boa prática |
| `warn` | Aviso — algo importante mas não destrutivo |
| `danger` | Algo crítico, erro comum grave, dado sigiloso |

## HTML

```html
<aside class="callout callout--<tipo>" role="note">
  <span class="callout__icon" aria-hidden="true"><símbolo></span>
  <div class="callout__content">
    <p class="callout__title">Título</p>
    <p>Corpo.</p>
  </div>
</aside>
```

Símbolos sugeridos:
- info: `i`
- tip: `★`
- warn: `!`
- danger: `✕`

Para `danger`, mudar `role="note"` para `role="alert"`.

## Procedimento

1. Identificar onde inserir (seção, slide, painel).
2. Não usar callout para decoração de cor — semântica é regra. Ver [../references/anti-patterns.md](../references/anti-patterns.md) A8.
3. Validar tipo (não inventar `callout--success` ou `callout--note`).
4. Validar.
