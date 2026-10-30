/* estudos/aiops: widget de quiz com feedback imediato.
   Uso: <div class="quiz" data-quiz="id-unico"></div> + <script type="application/json" id="id-unico">[...]</script>
   Cada pergunta: { "prompt": "...", "options": ["...", "..."], "answer": 0, "why": "explicação" }
   Regras de autoria (SKILL /teach): alternativas com o mesmo nº de palavras e caracteres parecidos;
   variar a posição da correta. O widget não embaralha: a ordem é responsabilidade de quem escreve. */
(function () {
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function mount(root) {
    var data = document.getElementById(root.dataset.quiz);
    if (!data) return;
    var questions = JSON.parse(data.textContent);
    var answered = 0, right = 0;
    var score = el("p", "quiz-score");
    score.setAttribute("aria-live", "polite");
    score.hidden = true;

    questions.forEach(function (q, i) {
      var box = el("div", "q");
      box.appendChild(el("span", "q-num", "Questão " + (i + 1) + " de " + questions.length));
      var prompt = el("p", "q-prompt");
      prompt.innerHTML = q.prompt; // conteúdo autoral, não vem do usuário
      box.appendChild(prompt);
      var opts = el("div", "q-options");
      opts.setAttribute("role", "group");
      var fb = el("p", "q-feedback");
      fb.setAttribute("aria-live", "polite");

      q.options.forEach(function (label, j) {
        var b = el("button", null, label);
        b.type = "button";
        b.addEventListener("click", function () {
          var ok = j === q.answer;
          answered++; if (ok) right++;
          Array.prototype.forEach.call(opts.children, function (btn, k) {
            btn.disabled = true;
            if (k === q.answer) btn.classList.add("correct");
          });
          if (!ok) b.classList.add("wrong");
          fb.innerHTML = (ok ? '<strong class="ok">Certo.</strong> ' : '<strong class="bad">Não.</strong> ') + q.why;
          if (answered === questions.length) {
            score.hidden = false;
            score.textContent = "Resultado: " + right + " de " + questions.length +
              (right === questions.length ? ". Domínio na primeira tentativa!" :
               ". Releia as explicações e refaça daqui a alguns dias: o espaçamento é o que fixa.");
          }
        });
        opts.appendChild(b);
      });

      box.appendChild(opts);
      box.appendChild(fb);
      root.appendChild(box);
    });
    root.appendChild(score);
  }

  document.querySelectorAll(".quiz[data-quiz]").forEach(mount);
})();
