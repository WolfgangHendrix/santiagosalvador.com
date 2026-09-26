/** Physical print checkout stays on Ko-fi; unpublished products use inquiries. */
document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('prints-grid');
  const catalog = window.PRINTS_DATA;
  if (!grid || !Array.isArray(window.ARTWORKS_DATA) || !Array.isArray(catalog?.products)) return;
  const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: catalog.currency, maximumFractionDigits: 0 });
  for (const product of catalog.products) {
    const art = window.ARTWORKS_DATA.find(item => item.filename === product.filename);
    if (!art) continue;
    const card = document.createElement('article');
    card.className = 'print-card';
    const image = document.createElement('img');
    image.src = art.thumb || art.url;
    image.alt = art.title;
    image.loading = 'lazy';
    const title = document.createElement('h3');
    title.textContent = art.title;
    const price = document.createElement('p');
    price.className = 'print-price';
    price.textContent = `Signed studio print · ${money.format(product.price)} ${catalog.currency}`;
    const link = document.createElement('a');
    link.className = 'btn btn-outline btn-sm';
    link.textContent = 'Ask About This Print';
    link.setAttribute('aria-label', `Ask about a print of ${art.title}`);
    const body = `Artwork: ${art.title}\nPreferred size:\nQuantity:\nShipping country and postal code:\n`;
    link.href = `mailto:salvsantiago@gmail.com?subject=${encodeURIComponent('Print inquiry: ' + art.title)}&body=${encodeURIComponent(body)}`;
    // A support-page URL must never be presented as a product checkout.
    try {
      const checkout = new URL(product.checkoutUrl);
      if (checkout.protocol === 'https:' && checkout.hostname === 'ko-fi.com' && /^\/s\/[a-z0-9]+\/?$/i.test(checkout.pathname)) {
        link.href = checkout.href;
        link.textContent = 'Buy on Ko-fi';
        link.setAttribute('aria-label', `Buy a signed print of ${art.title} on Ko-fi`);
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
      }
    } catch { /* No live listing yet; keep the inquiry link. */ }
    card.append(image, title, price, link);
    grid.appendChild(card);
  }
});
