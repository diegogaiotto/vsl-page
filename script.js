/* ── Vturb: revelar conteúdo aos 415s ── */
(function () {
  var delaySeconds = 1303;
  var player = document.querySelector("vturb-smartplayer");
  if (!player) return;
  player.addEventListener("player:ready", function () {
    player.displayHiddenElements(delaySeconds, [".esconder"], { persist: true });
  });
})();

/* ── Modal de depoimentos ── */
(function () {
  var modal   = document.getElementById("video-modal");
  var iframe  = document.getElementById("modal-iframe");
  var btnClose = document.getElementById("modal-close");

  function openModal(videoId) {
    iframe.src = "https://www.youtube.com/embed/" + videoId + "?autoplay=1&rel=0&playsinline=1";
    modal.classList.add("modal-active");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    modal.classList.remove("modal-active");
    modal.setAttribute("aria-hidden", "true");
    iframe.src = "";
    document.body.style.overflow = "";
  }

  /* clique nos cards de depoimento */
  document.querySelectorAll(".testimonial-card").forEach(function (card) {
    card.addEventListener("click", function () {
      openModal(card.getAttribute("data-video-id"));
    });
    /* acessibilidade: Enter e Espaço também abrem */
    card.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        openModal(card.getAttribute("data-video-id"));
      }
    });
  });

  /* fechar pelo botão X */
  btnClose.addEventListener("click", closeModal);

  /* fechar clicando fora do vídeo */
  modal.addEventListener("click", function (e) {
    if (e.target === modal) closeModal();
  });

  /* fechar com tecla ESC */
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeModal();
  });
})();
