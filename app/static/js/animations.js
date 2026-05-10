(function () {
  const BALLOON_COLORS = ['#FF385C','#FF9A00','#FFD700','#00C48C','#4A90E2','#9B59B6','#FF6B9D'];

  function launchBalloons(count = 12) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    for (let i = 0; i < count; i++) {
      setTimeout(() => {
        const balloon = document.createElement('div');
        balloon.className = 'balloon';
        balloon.style.left = (5 + Math.random() * 90) + 'vw';
        balloon.style.bottom = '-80px';
        balloon.style.backgroundColor = BALLOON_COLORS[Math.floor(Math.random() * BALLOON_COLORS.length)];
        document.body.appendChild(balloon);
        balloon.addEventListener('animationend', () => balloon.remove());
      }, Math.random() * 800);
    }
  }

  function initCardAnimations() {
    const cards = document.querySelectorAll('.task-card');
    cards.forEach((card, i) => {
      setTimeout(() => card.classList.add('visible'), i * 40);
    });
  }

  function initStatusChangeListeners() {
    // Listen for status select changes anywhere on the page (e.g. edit form, list view)
    document.addEventListener('change', (e) => {
      if (e.target && e.target.name === 'status' && e.target.value === 'done') {
        launchBalloons();
      }
    });
  }

  window.launchBalloons = launchBalloons;
  document.addEventListener('DOMContentLoaded', () => {
    initCardAnimations();
    initStatusChangeListeners();
  });
})();
