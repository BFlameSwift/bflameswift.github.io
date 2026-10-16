// Keep the rendered snapshot if the last-good endpoint is unavailable or invalid.
(() => {
  const badges = [...document.querySelectorAll('[data-scholar-paper]')];
  if (!badges.length) return;
  fetch('/stats/scholar.json', { cache: 'no-store' })
    .then(response => {
      if (!response.ok) throw new Error('Citation snapshot unavailable');
      return response.json();
    })
    .then(data => {
      const date = new Date(data.updated_at);
      if (!Number.isFinite(date.getTime()) || !badges.every(badge => {
        const count = data.papers?.[badge.dataset.scholarPaper]?.count;
        return Number.isSafeInteger(count) && count >= 0;
      })) throw new Error('Invalid citation snapshot');
      badges.forEach(badge => {
        badge.lastElementChild.textContent = `Cited by ${data.papers[badge.dataset.scholarPaper].count}`;
        badge.title = `Google Scholar citations; checked ${date.toLocaleDateString('en-CA', { timeZone: 'Asia/Taipei' })}`;
      });
    })
    .catch(() => {});
})();
