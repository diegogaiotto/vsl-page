/* ── Vturb: revelar conteúdo aos 520s (8min40s) ── */
(function () {
  var delaySeconds = 520;
  var player = document.querySelector("vturb-smartplayer");
  if (!player) return;
  player.addEventListener("player:ready", function () {
    player.displayHiddenElements(delaySeconds, [".esconder"], { persist: true });
  });
})();

/* ── Countdown timer da oferta ── */
(function () {
  var total = 15 * 60;
  var el = document.getElementById("countdown-timer");
  if (!el) return;
  var interval = setInterval(function () {
    total--;
    if (total <= 0) {
      clearInterval(interval);
      el.textContent = "00:00";
      return;
    }
    var m = Math.floor(total / 60);
    var s = total % 60;
    el.textContent = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
  }, 1000);
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

  document.querySelectorAll(".testimonial-card").forEach(function (card) {
    card.addEventListener("click", function () {
      openModal(card.getAttribute("data-video-id"));
    });
    card.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        openModal(card.getAttribute("data-video-id"));
      }
    });
  });

  btnClose.addEventListener("click", closeModal);

  modal.addEventListener("click", function (e) {
    if (e.target === modal) closeModal();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeModal();
  });
})();
