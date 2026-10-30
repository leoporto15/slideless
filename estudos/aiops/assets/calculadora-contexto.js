/* estudos/aiops: calculadora de contexto de um agente.
   Uso: <div class="calc" data-calc></div>. Valores padrão por data-atributos opcionais.
   Modelo simplificado: a cada turno o agente reenvia instruções + trechos da KB + todo o histórico. */
(function () {
  var campos = [
    ["instr", "Instruções do agente (tokens)", 800],
    ["chunks", "Trechos da KB por turno", 4],
    ["chunk", "Tamanho de cada trecho (tokens)", 400],
    ["q", "Pergunta do usuário (tokens)", 60],
    ["tool", "Resultado de ferramenta por turno (tokens)", 300],
    ["a", "Resposta do agente (tokens)", 250],
    ["turnos", "Turnos na conversa", 8],
    ["pin", "Preço de EXEMPLO, entrada (US$ por milhão)", 3],
    ["pout", "Preço de EXEMPLO, saída (US$ por milhão)", 15]
  ];
  function fmt(n) { return Math.round(n).toLocaleString("pt-BR"); }
  function mount(root) {
    var box = document.createElement("div"); box.className = "calc-inputs";
    var inputs = {};
    campos.forEach(function (c) {
      var id = "calc-" + c[0];
      var l = document.createElement("label"); l.setAttribute("for", id); l.textContent = c[1];
      var i = document.createElement("input"); i.type = "number"; i.min = "0"; i.step = "any"; i.id = id;
      i.value = root.dataset[c[0]] || c[2];
      i.addEventListener("input", render);
      l.appendChild(i); box.appendChild(l); inputs[c[0]] = i;
    });
    var out = document.createElement("div"); out.className = "calc-out"; out.setAttribute("aria-live", "polite");
    var total = document.createElement("p"); total.className = "calc-total";
    var legend = document.createElement("p"); legend.className = "calc-legend";
    legend.innerHTML = "<span><i></i>Entrada (o que o modelo lê)</span><span><i class=\"out\"></i>Saída (o que o modelo escreve)</span>";
    root.appendChild(box); root.appendChild(out); root.appendChild(legend); root.appendChild(total);

    function v(k) { var x = parseFloat(inputs[k].value); return isFinite(x) && x >= 0 ? x : 0; }
    function render() {
      var n = Math.min(Math.round(v("turnos")), 40), linhas = [], maxT = 1, tin = 0, tout = 0;
      var fixo = v("instr") + v("chunks") * v("chunk"), turno = v("q") + v("tool") + v("a");
      for (var t = 1; t <= n; t++) {
        var ein = fixo + v("q") + v("tool") + (t - 1) * turno, eout = v("a");
        linhas.push([t, ein, eout]); tin += ein; tout += eout; maxT = Math.max(maxT, ein + eout);
      }
      out.innerHTML = "";
      linhas.forEach(function (r) {
        var row = document.createElement("div"); row.className = "calc-row";
        var wIn = (r[1] / maxT) * 100, wOut = (r[2] / maxT) * 100;
        row.innerHTML = "<span>Turno " + r[0] + "</span><span class=\"calc-bar\"><span style=\"width:" + wIn + "%\"></span><span class=\"out\" style=\"left:" + wIn + "%;width:" + wOut + "%\"></span></span><span>" + fmt(r[1] + r[2]) + " tok</span>";
        out.appendChild(row);
      });
      var custo = tin / 1e6 * v("pin") + tout / 1e6 * v("pout");
      var pctIn = tin + tout ? Math.round(tin / (tin + tout) * 100) : 0;
      total.innerHTML = "Conversa inteira: <strong>" + fmt(tin) + "</strong> tokens de entrada + <strong>" + fmt(tout) +
        "</strong> de saída (" + pctIn + "% é entrada). Custo com os preços de exemplo: <strong>US$ " +
        custo.toLocaleString("pt-BR", { minimumFractionDigits: 4, maximumFractionDigits: 4 }) + "</strong> por conversa, ou US$ " +
        (custo * 10000).toLocaleString("pt-BR", { maximumFractionDigits: 0 }) + " a cada 10 mil conversas.";
    }
    render();
  }
  document.querySelectorAll(".calc[data-calc]").forEach(mount);
})();
