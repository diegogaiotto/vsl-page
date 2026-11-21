# Gera /c, /d e /e (VSL 1, 2, 3) a partir do visual "cédula" de e/index.html
import re, sys, json
ROOT = "/Users/diegoferreiragaioto/vsl-page/"
tpl = open(sys.argv[1]).read()
head_css = tpl[tpl.index("<style>"):tpl.index("</style>") + len("</style>")]
cfg = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}

EXTRA_CSS = """
    .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 24px 0 4px; }
    .stat { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 12px 4px; border-top: 2px solid var(--nota); border-bottom: 2px solid var(--nota); }
    .stat-num { font-stretch: 70%; font-weight: 900; font-size: clamp(26px, 7vw, 38px); line-height: 1; color: var(--nota); white-space: nowrap; }
    .stat .one-label { font-size: 13px; }
    .tool-grid { list-style: none; margin-top: 22px; display: grid; gap: 12px; }
    .tool-grid li { border: 2px solid var(--nota); border-radius: 4px; padding: 16px 18px; background: var(--papel); }
    .tool-grid .tag { display: inline-block; font-stretch: 125%; font-weight: 800; font-size: 11px; letter-spacing: .08em; color: var(--papel); background: var(--nota); padding: 2px 8px; border-radius: 2px; margin-bottom: 8px; }
    .tool-grid p { color: var(--muted); }
    .ladder { list-style: none; margin: 4px 0 6px; }
    .ladder li { color: var(--muted); text-decoration: line-through; font-size: 15px; }
    .free { display: inline-block; margin-top: 10px; font-weight: 800; color: var(--selo); }
"""

def player(vid):
    if not vid:
        return '<div style="aspect-ratio:9/16;max-width:400px;margin:0 auto;background:#000;color:#fff;display:grid;place-items:center">VÍDEO</div>'
    acc, pid = vid
    return ('<vturb-smartplayer id="vid-%s" style="display: block; margin: 0 auto; width: 100%%; max-width: 400px;"><div class="vturb-player-placeholder" style="position: relative; width: 100%%; padding: 177.77777777777777%% 0 0; z-index: 0; background-color: black;"></div></vturb-smartplayer>\n'
            '        <script type="text/javascript">\n'
            '          var s=document.createElement("script");\n'
            '          s.src="https://scripts.converteai.net/%s/players/%s/v4/player.js", s.async=!0,document.head.appendChild(s);\n'
            '        </script>') % (pid, acc, pid)

MENTOR = """
          <h2>Prazer, eu sou o Diego Ferreira</h2>
          <p class="lead">Fui CLT no interior de São Paulo ganhando R$ 1.600, depois R$ 2.900 por mês. Fui demitido, peguei o acerto e me mudei pra Florianópolis pra fazer acontecer no digital, morando numa casa bem humilde.</p>

          <ul class="path">
            <li><span class="path-when">De onde vim</span><div><h3>CLT, interior de SP</h3><p>Salário curto, sem liberdade nem pra viajar sem pedir pro chefe.</p></div></li>
            <li><span class="path-when">A virada</span><div><h3>Com a água batendo, testei até achar o que funciona</h3><p>Vender produto digital em dólar e euro, no automático, pra quem já quer comprar.</p></div></li>
            <li><span class="path-when">Hoje</span><div><h3>Vivo do digital em Floripa</h3><p>Trabalho de casa com vista pro mar, e a operação roda mesmo quando eu viajo.</p></div></li>
          </ul>

          <div class="figures">
            <div class="figure"><strong>R$ 176 mil</strong><span>de faturamento em 3 meses</span></div>
            <div class="figure"><strong>R$ 4.300</strong><span>de lucro em um único dia (recorde)</span></div>
          </div>

          <p class="lead">Mais de 5 mil alunos já passaram pelos meus cursos. Hoje a minha mentoria individual custa R$ 10.000.</p>

          <p class="photo-cap">Antes</p>
          <div class="photos photos--2">
            <img src="../images/antes-1.jpg" alt="Diego antes, no interior de SP" />
            <img src="../images/antes-2.jpg" alt="Diego antes, no interior de SP" />
          </div>
          <p class="photo-cap">Hoje, em Florianópolis</p>
          <div class="photos">
            <img src="../images/depois-1.jpg" alt="Diego hoje, em Florianópolis" />
            <img src="../images/depois-2.jpg" alt="Diego hoje, em Florianópolis" />
            <img src="../images/depois-3.jpg" alt="Diego hoje, em Florianópolis" />
          </div>
"""

QUOTES = """
          <section class="block">
            <h2>Quem já está fazendo</h2>
            <div class="quotes">
              <blockquote class="quote">
                <p>Recebeu a estrutura validada, ajustou as campanhas e estava vendendo desde o segundo dia de operação.</p>
                <footer><strong>Lucas</strong>, aluno do Dólar Automático</footer>
              </blockquote>
              <blockquote class="quote">
                <p>Começou a rodar em 28 de julho e em menos de uma semana já tinha vendas no Pix, Stripe, PayPal e Hotmart, incluindo um Pix de R$ 500 no segundo dia.</p>
                <footer><strong>Patrick</strong>, aluno da mentoria</footer>
              </blockquote>
              <blockquote class="quote">
                <p>Faturou os primeiros R$ 10 mil em 17 dias e recebeu a premiação da Hotmart.</p>
                <footer><strong>David</strong>, premiado pela Hotmart</footer>
              </blockquote>
            </div>
          </section>
"""

COUNTRIES = """
          <section class="block">
            <h2>Alguns dos países que mais compram</h2>
            <div class="countries"><span>Estados Unidos</span><span>Portugal</span><span>Reino Unido</span><span>França</span><span>Itália</span><span>Paraguai</span></div>
            <p class="note-small">Vendas em dólar e euro todos os dias, mostradas ao vivo no vídeo.</p>
          </section>
"""

RATE = """
            <div class="rate">
              <div class="rate-side rate-side--usd"><span class="rate-num">US$ 1</span><span class="rate-cap">pago lá fora</span></div>
              <span class="rate-eq" aria-hidden="true">≈</span>
              <div class="rate-side rate-side--brl"><span class="rate-num">R$ 5</span><span class="rate-cap">no seu bolso</span></div>
            </div>
"""

COURSE_STEPS = """
          <section class="block">
            <h2>Como a venda automática acontece</h2>
            <ol class="steps">
              <li><h3>Você encontra uma demanda reprimida</h3><p>Produtos que já vendem muito lá fora, achados com ferramentas de mineração. Nada de achismo.</p></li>
              <li><h3>Adapta o produto pro idioma e a moeda</h3><p>Mesmo produto, novo público, pagando em dólar ou euro.</p></li>
              <li><h3>Testa com R$ 50 a R$ 100</h3><p>Uns 5 criativos. Pausa o que não deu certo e coloca mais dinheiro no que vendeu.</p></li>
              <li><h3>O robô atende e vende</h3><p>O funil automático conversa com o cliente e entrega o produto. Você só acompanha.</p></li>
            </ol>
          </section>
"""

PAGES = {
  "c": dict(
    title="Dólar Automático com IA — Diego Ferreira",
    desc="Como eu vendo em dólar pra fora do Brasil, no automático, da minha casa.",
    top="Dólar Automático com IA",
    headline="Como eu vendo em dólar pra fora do Brasil, no automático, de casa",
    sub="Sem aparecer, sem falar com cliente e começando com pouco. No vídeo eu abro a minha tela, mostro as vendas caindo em dólar na Hotmart e os resultados dos alunos. Assista até o fim.",
    ones=[("US$ · €", "moedas que você recebe"), ("24h", "o robô atende por você"), ("0", "vezes que você aparece")],
    metodo="""
          <h2>Por que vender em dólar</h2>
          <p class="lead">O Brasil está saturado e o real é fraco. Lá fora tem gente querendo comprar e cada venda vale 5 a 6 vezes mais no seu bolso.</p>
""" + RATE + """
""" + COURSE_STEPS + COUNTRIES + QUOTES,
    bonus_title="O que vem junto com o curso",
    bonus=[
      ("Método de análise das ofertas mais escaladas", "Como encontrar as ofertas boas antes de gastar um real em anúncio.", None),
      ("Criativos prontos de uma oferta de R$ 100 mil", "Os criativos de uma oferta que já vendeu mais de US$ 20 mil.", None),
      ("Funil pronto, copia e cola", "O mesmo funil automático que eu uso. Você cola, coloca pra rodar e já pode vender no segundo dia.", None),
      ("Grupo de networking com os alunos", "Contato com quem já vende todo dia em dólar: estratégias, criativos e parcerias novas.", None),
    ],
    offer_title="Dólar Automático com IA: curso gravado e 4 bônus",
    ladder=["Mentoria individual: R$ 10.000", "Preço justo do curso: R$ 5.000", "Nem a metade: R$ 2.500"],
    price_big="12x R$ 9,90", price_small="ou R$ 97 à vista",
    seal="PREÇO DE<br/>LANÇA-<br/>MENTO",
    buy_text="Quero entrar por R$ 97", buy_small="Acesso liberado logo após o pagamento",
    checkout="https://pay.kirvano.com/c48e32d5-9527-49c5-bbaa-27e4a9c68970",
    guarantee="Garantia incondicional de 7 dias. Se não gostar, você pede o reembolso e recebe cada centavo de volta.",
  ),
  "d": dict(
    title="Do escravo do digital ao automático — Diego Ferreira",
    desc="Eu parei de vender o meu tempo e passei a vender em dólar, no automático.",
    top="Do escravo do digital ao automático",
    headline="Eu parei de vender o meu tempo e passei a vender em dólar, no automático",
    sub="Antes eu fazia fotos com IA e passava o dia todo no celular atendendo. Hoje eu vendo produto digital pra fora, sem mostrar o rosto. No vídeo eu mostro como. Assista até o fim.",
    ones=[("R$ 1 mil", "recorde por dia nas fotos"), ("R$ 4.300", "de lucro em 1 dia"), ("R$ 17 mil", "de lucro numa semana")],
    metodo="""
          <h2>Serviço prende. Produto liberta.</h2>
          <p class="lead">Quando você vende um serviço, paga com as suas horas. Quando vende um produto digital, vende vários sem trabalho a mais.</p>
          <ul class="wrong">
            <li><h3>Fazer cada foto na mão</h3><p>Pegar o mouse, refazer quando o cliente não gosta, entregar depois.</p></li>
            <li><h3>Atender o dia inteiro no celular</h3><p>O teto era R$ 1 mil de lucro por dia, trabalhando muito.</p></li>
            <li><h3>Ficar preso no Brasil e no real</h3><p>Mercado saturado, moeda fraca.</p></li>
          </ul>

          <section class="block" style="margin-top:40px">
            <h2>A estratégia nova: produto que já vende, em moeda forte</h2>
            <p class="lead">Achar produtos que vendem muito e adaptar pra vender lá fora, onde cada venda vale 5 a 6 vezes mais. E a ferramenta não só vende no automático: ela entrega o produto pro cliente.</p>
""" + RATE + """
          </section>
""" + COURSE_STEPS + COUNTRIES + QUOTES,
    bonus_title="O que vem junto com o curso",
    bonus=[
      ("Criativo pronto", "Pra você subir o anúncio sem começar do zero.", None),
      ("Funil pronto, copia e cola", "O funil é quem fala com os clientes e faz a venda por você.", None),
      ("Grupo exclusivo com alunos que vendem", "Gente que já vende em outras moedas. Diga-me com quem andas.", None),
    ],
    offer_title="O método completo na tela do computador, com 3 bônus",
    ladder=["Mentoria individual: R$ 10.000", "Metade: R$ 5.000", "Um décimo: R$ 500"],
    price_big="12x R$ 9,90", price_small="ou R$ 97 à vista",
    seal="PREÇO DE<br/>LANÇA-<br/>MENTO",
    buy_text="Quero entrar por R$ 97", buy_small="O mesmo preço com que lancei o curso de fotos, que hoje custa R$ 997",
    checkout="https://pay.kirvano.com/c48e32d5-9527-49c5-bbaa-27e4a9c68970",
    guarantee="Garantia de 7 dias. A outra garantia depende de você: sentar, aplicar e subir os anúncios.",
  ),
  "e": dict(
    title="Do CLT ao dólar no automático — Diego Ferreira",
    desc="Do CLT de R$ 1.600 a vender em dólar no automático, com uma ferramenta que minera, cria o produto e vende por você.",
    top="Do CLT ao dólar no automático",
    headline="Do CLT de R$ 1.600 a vender em dólar no automático, morando na praia",
    sub="Com pouco dinheiro em anúncio e sem depender de técnica de venda. No vídeo eu mostro a ferramenta, o país que mais compra e o produto que eu mais vendo. Assista até o fim.",
    ones=[("R$ 50", "pra começar um teste"), ("5", "criativos por teste"), ("0", "mensagens manuais")],
    metodo="""
          <h2>Uma ferramenta, três trabalhos</h2>
          <p class="lead">O que antes exigia três pessoas e semanas de teste agora é um só lugar. Você não tenta acertar o produto: pega o que já tem demanda e coloca pra vender.</p>
          <ul class="tool-grid">
            <li><span class="tag">1 · MINERA</span><h3>Acha as ofertas que mais vendem no mundo</h3><p>Espiona os anúncios que estão escalando em outros países e mostra a demanda reprimida pronta pra você.</p></li>
            <li><span class="tag">2 · CRIA</span><h3>Monta o produto inteiro com IA</h3><p>A IA constrói o produto com base no que já vende, já adaptado pro idioma e pra moeda do país. Você não precisa fazer nada na mão.</p></li>
            <li><span class="tag">3 · VENDE</span><h3>Automatiza as mensagens de venda</h3><p>O funil validado conversa com o cliente, convence e entrega. Você só acompanha e escala no gerenciador.</p></li>
          </ul>

          <section class="block" style="margin-top:40px">
            <h2>Por que em dólar e euro</h2>
            <p class="lead">Mesmo produto, novo público, moeda até 6 vezes mais forte. Por isso dá pra testar com pouco e ter lucro no dia seguinte.</p>
""" + RATE + """
          </section>
""" + COURSE_STEPS + COUNTRIES + QUOTES,
    bonus_title="Pegando a ferramenta hoje, você leva de graça",
    bonus=[
      ("O curso completo Do CLT ao Dólar", "O método inteiro na tela do computador, clique a clique: achar, validar e escalar produtos.", "Seria R$ 500, sai de graça com a ferramenta"),
      ("Protocolo de IA pra subir e analisar campanhas", "A mesma IA que sobe e analisa os anúncios da minha operação.", None),
      ("Meu funil validado + criativos prontos", "Um código que você cola na ferramenta e cria o meu fluxo de vendas inteiro com um clique.", None),
      ("Grupo de networking", "Contato com quem já vende todo dia em dólar e euro.", None),
    ],
    offer_title="A ferramenta que minera, cria o produto e vende por você",
    ladder=[],
    price_big="50% OFF", price_small="Black Friday: metade do preço",
    seal="BLACK<br/>FRIDAY<br/>50% OFF",
    buy_text="Quero a ferramenta pela metade do preço", buy_small="E receber o curso completo de graça",
    checkout="LINK_FERRAMENTA",
    guarantee="Garantia de 7 dias. Se não gostar, você pede o reembolso e recebe cada centavo de volta.",
  ),
}

def pixel(pid):
    if not pid:
        return ""
    return """<!-- Meta Pixel -->
  <script>
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
    document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '%s');
    fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=%s&ev=PageView&noscript=1" /></noscript>
  """ % (pid, pid)

def build(key, p, vid, delay, px=None):
    ones = "\n".join('          <div class="stat"><span class="stat-num">%s</span><span class="one-label">%s</span></div>' % (n, l) for n, l in p["ones"])
    bonus = "\n".join('          <li><div><h3>%s</h3><p>%s</p>%s</div></li>' % (h, d, '<span class="value">%s</span>' % v if v else "") for h, d, v in p["bonus"])
    ladder = ('<ul class="ladder">%s</ul>' % "".join("<li>%s</li>" % x for x in p["ladder"])) if p["ladder"] else ""
    css = head_css.replace("</style>", EXTRA_CSS + "  </style>")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{p['desc']}" />
  <title>{p['title']}</title>
  <link rel="icon" type="image/png" href="../favicon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap" rel="stylesheet" />
  {pixel(px)}{css}
</head>
<body>

  <!-- Hero: headline + números + vídeo (sempre visível) -->
  <header class="hero">
    <div class="wrap">
      <div class="note">
        <p class="note-top">{p['top']}</p>
        <h1 class="headline">{p['headline']}</h1>
        <div class="stats">
{ones}
        </div>
      </div>

      <p class="sub">{p['sub']}</p>

      <div class="video">
        {player(vid)}
      </div>

      <a href="#oferta" class="jump esconder">Ver a oferta</a>
    </div>
  </header>

  <!-- Tudo abaixo só aparece no segundo em que o preço é falado no vídeo ({delay}s) -->
  <main class="esconder">
    <section class="block">
      <div class="wrap">

        <div class="tabs" role="tablist">
          <button class="tab" role="tab" id="tab-metodo" aria-controls="painel-metodo" aria-selected="true">O método</button>
          <button class="tab" role="tab" id="tab-mentor" aria-controls="painel-mentor" aria-selected="false">Quem é seu mentor</button>
        </div>

        <div class="panel" id="painel-metodo" role="tabpanel" aria-labelledby="tab-metodo">
{p['metodo']}
        </div>

        <div class="panel" id="painel-mentor" role="tabpanel" aria-labelledby="tab-mentor" hidden>
{MENTOR}
        </div>
      </div>
    </section>

    <section class="block">
      <div class="wrap">
        <h2>{p['bonus_title']}</h2>
        <ul class="inside">
{bonus}
        </ul>
      </div>
    </section>

    <section class="offer" id="oferta">
      <div class="wrap">
        <div class="note">
          <span class="seal" aria-hidden="true">{p['seal']}</span>
          <p class="offer-title">{p['offer_title']}</p>
          {ladder}
          <p class="price"><span class="price-big">{p['price_big']}</span><span class="price-small">{p['price_small']}</span></p>
          <a href="{p['checkout']}" class="buy">
            {p['buy_text']}
            <small>{p['buy_small']}</small>
          </a>
          <p class="guarantee">{p['guarantee']}</p>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <p>© 2026 Diego Ferreira. Todos os direitos reservados.</p>
      <p>Este site não é afiliado ao Facebook, Instagram ou Google.</p>
    </div>
  </footer>

  <script>
    /* Libera a página de vendas aos {delay}s do vídeo, quando o preço é falado */
    (function () {{
      var delaySeconds = {delay};
      var revealed = false;

      function markOffer() {{
        var offer = document.getElementById("oferta");
        if (!offer || !("IntersectionObserver" in window)) return;
        var io = new IntersectionObserver(function (entries) {{
          if (entries[0].isIntersecting) {{ offer.classList.add("is-in"); io.disconnect(); }}
        }}, {{ threshold: .4 }});
        io.observe(offer);
      }}

      function reveal() {{
        if (revealed) return;
        revealed = true;
        document.querySelectorAll(".esconder").forEach(function (el) {{ el.classList.remove("esconder"); }});
        markOffer();
      }}

      /* Prévia local: mostra tudo de uma vez */
      if (location.hostname === "localhost" || location.hostname === "127.0.0.1" || location.protocol === "file:") {{ reveal(); return; }}

      var player = document.querySelector("vturb-smartplayer");
      if (player) {{
        player.addEventListener("player:ready", function () {{
          revealed = true;
          player.displayHiddenElements(delaySeconds, [".esconder"], {{ persist: true }});
          markOffer();
        }});
      }}

      /* Plano B: se o player não avisar que está pronto, libera pelo relógio */
      setTimeout(reveal, (delaySeconds + 5) * 1000);
    }})();

    /* Abas */
    (function () {{
      var tabs = document.querySelectorAll(".tab");
      tabs.forEach(function (tab) {{
        tab.addEventListener("click", function () {{
          tabs.forEach(function (t) {{
            var on = t === tab;
            t.setAttribute("aria-selected", on ? "true" : "false");
            document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
          }});
        }});
      }});
    }})();
  </script>

</body>
</html>
"""

DELAY = {"c": 568, "d": 428, "e": 553}
for k, p in PAGES.items():
    c = cfg.get(k, {})
    if c.get("checkout"): p["checkout"] = c["checkout"]
    vid = (c["acc"], c["pid"]) if c.get("pid") else None
    out = build(k, p, vid, DELAY[k], c.get("pixel"))
    open(sys.argv[3] + "/" + k + "/index.html", "w").write(out)
    print(k, len(out))
