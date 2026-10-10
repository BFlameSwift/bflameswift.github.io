// Combine the archived page-view baseline with the new domain's live count.
// Unique visitors remain domain-specific because identities cannot be deduplicated.
(() => {
  const initialize = () => {
    const stats = document.querySelector('[data-legacy-pv]');
    const current = document.getElementById('busuanzi_value_site_pv');
    const total = document.getElementById('visitor_total_views');
    if (!stats || !current || !total) return;
    const baseline = Number(stats.dataset.legacyPv);
    if (!Number.isSafeInteger(baseline) || baseline < 0) return;
    const update = () => {
      const value = current.textContent.trim();
      if (!/^\d+$/.test(value)) return;
      const count = Number(value);
      if (Number.isSafeInteger(count) && count >= 0) {
        total.textContent = (baseline + count).toLocaleString('en-US');
      }
    };
    new MutationObserver(update).observe(current, {
      childList: true,
      characterData: true,
      subtree: true,
    });
    update();
    setTimeout(() => {
      for (const element of [total, current, document.getElementById('busuanzi_value_site_uv')]) {
        if (element && element.textContent.trim() === 'Loading…') {
          element.textContent = 'Unavailable';
        }
      }
    }, 10000);
  };
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize, { once: true });
  } else {
    initialize();
  }
})();
