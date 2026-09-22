/**
 * Zero-dependency Modern Lightbox Modal
 */
const Lightbox = (function() {
  let modal, img, titleEl, metaEl, dlBtn;
  let items = [];
  let currentIndex = 0;
  let touchStartX = 0;

  function init() {
    modal = document.getElementById('lightbox-modal');
    if (!modal) return;

    img = modal.querySelector('.lightbox-img');
    titleEl = modal.querySelector('.lightbox-title');
    metaEl = modal.querySelector('.lightbox-meta');
    dlBtn = modal.querySelector('.lightbox-btn-dl');

    modal.querySelector('.lightbox-btn-close').addEventListener('click', close);
    modal.querySelector('.lightbox-btn-prev').addEventListener('click', prev);
    modal.querySelector('.lightbox-btn-next').addEventListener('click', next);

    modal.addEventListener('click', (e) => {
      if (e.target === modal || e.target.classList.contains('lightbox-content')) {
        close();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (!modal.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') prev();
      if (e.key === 'ArrowRight') next();
    });

    modal.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    modal.addEventListener('touchend', (e) => {
      const touchEndX = e.changedTouches[0].screenX;
      if (touchStartX - touchEndX > 50) next();
      if (touchEndX - touchStartX > 50) prev();
    }, { passive: true });
  }

  function open(itemList, index) {
    items = itemList;
    currentIndex = index;
    update();
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    modal.classList.remove('open');
    document.body.style.overflow = '';
  }

  function update() {
    if (!items || items.length === 0) return;
    const item = items[currentIndex];
    
    const cleanUrl = item.url.startsWith('/') ? item.url.slice(1) : item.url;
    img.src = cleanUrl;
    img.onerror = function() {
      if (!this.dataset.fallback) {
        this.dataset.fallback = '1';
        this.src = '../' + cleanUrl;
      }
    };
    img.alt = item.title || '';

    titleEl.textContent = item.title || 'Untitled';
    if (metaEl) {
      metaEl.textContent = item.categoryLabel || item.console || '';
    }
    if (dlBtn) {
      dlBtn.href = cleanUrl;
      dlBtn.download = item.filename || '';
    }
  }

  function prev() {
    if (items.length <= 1) return;
    currentIndex = (currentIndex - 1 + items.length) % items.length;
    update();
  }

  function next() {
    if (items.length <= 1) return;
    currentIndex = (currentIndex + 1) % items.length;
    update();
  }

  return { init, open, close, prev, next };
})();

if (typeof window !== 'undefined') {
  window.Lightbox = Lightbox;
}
