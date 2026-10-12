// Combine the archived page-view baseline with the new domain's live count.
// Unique visitors remain domain-specific because identities cannot be deduplicated.
(() => {
  const initialize = () => {
    const today = document.getElementById('visitor_today_views');
    const daily = document.getElementById('visitor_daily_days');
    if (today && daily) {
      fetch('/stats/daily.json', { cache: 'no-store' })
        .then(response => {
          if (!response.ok) throw new Error('Daily statistics unavailable');
          return response.json();
        })
        .then(data => {
          if (!Array.isArray(data.days) || data.days.length !== 7) throw new Error('Invalid daily statistics');
          daily.replaceChildren();
          for (const day of data.days) {
            const item = document.createElement('li');
            const value = Number.isSafeInteger(day.views) && day.views >= 0 ? day.views.toLocaleString('en-US') : '—';
            item.textContent = `${day.date}${day.partial ? ' (partial)' : ''}: ${value}`;
            daily.appendChild(item);
          }
          today.textContent = data.days[6].views.toLocaleString('en-US');
        })
        .catch(() => { today.textContent = 'Unavailable'; });
    }
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
