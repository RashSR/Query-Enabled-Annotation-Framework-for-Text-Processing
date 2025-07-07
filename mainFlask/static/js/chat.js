window.addEventListener('load', () => {
  /* ── 1. Scroll to element with id="scroll‑anchor" (if present) ── */
  const anchorEl = document.getElementById('scroll-anchor');
  if (anchorEl) {
    anchorEl.scrollIntoView({ behavior: 'auto' });
  }

  /* ── 2. If URL ends with #something, highlight & center that element ── */
  const hash = window.location.hash;
  if (hash) {
    const target = document.querySelector(hash);
    if (target) {
      target.classList.add('highlighted');
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }
});
