/**
 * Retro Game Labels Hub Controller
 */
const LabelsHub = (function() {
  let allLabels = [];
  let filteredLabels = [];
  let currentConsole = 'all';
  let searchQuery = '';
  let itemsPerPage = 32;
  let displayedCount = 0;

  let gridEl, consoleBtns, searchInput, loadMoreBtn;
  let loaded = false;
  let loading = null;

  function loadCatalog() {
    if (loaded) return Promise.resolve();
    if (loading) return loading;
    gridEl.textContent = 'Loading cartridge labels…';
    gridEl.setAttribute('aria-busy', 'true');
    loading = new Promise((resolve, reject) => {
      if (window.LABELS_DATA?.labels) return resolve();
      // A deferred script also works when the portfolio is opened from disk.
      const script = document.createElement('script');
      script.src = 'assets/data/labels.js';
      script.onload = () => {
        script.remove();
        if (Array.isArray(window.LABELS_DATA?.labels)) resolve();
        else reject(new Error('Invalid label catalog'));
      };
      script.onerror = () => {
        script.remove();
        reject(new Error('Could not load label catalog'));
      };
      document.head.appendChild(script);
    }).then(() => {
      allLabels = window.LABELS_DATA.labels;
      loaded = true;
      applyFilter();
    }).catch(error => {
      loading = null;
      gridEl.textContent = 'Could not load labels. Please try again.';
      if (loadMoreBtn) {
        loadMoreBtn.style.display = 'inline-flex';
        loadMoreBtn.textContent = 'Retry Loading Labels';
      }
      console.error('Error loading labels:', error);
    }).finally(() => gridEl.setAttribute('aria-busy', 'false'));
    return loading;
  }

  function init() {
    gridEl = document.getElementById('labels-grid');
    consoleBtns = document.querySelectorAll('.label-filter-btn');
    searchInput = document.getElementById('label-search');
    loadMoreBtn = document.getElementById('label-load-more');

    if (!gridEl) return;

    if (loadMoreBtn) loadMoreBtn.style.display = 'none';
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        if (entries.some(entry => entry.isIntersecting)) {
          observer.disconnect();
          loadCatalog();
        }
      }, { rootMargin: '400px' });
      observer.observe(document.getElementById('labels') || gridEl);
    } else {
      loadCatalog();
    }

    consoleBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        consoleBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentConsole = btn.dataset.console;
        if (loaded) applyFilter();
        else loadCatalog();
      });
    });

    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase().trim();
        if (loaded) applyFilter();
        else loadCatalog();
      });
    }

    if (loadMoreBtn) {
      loadMoreBtn.addEventListener('click', () => {
        if (loaded) renderChunk();
        else loadCatalog();
      });
    }
  }

  function applyFilter() {
    filteredLabels = allLabels.filter(item => {
      const matchConsole = (currentConsole === 'all') ? true :
                            (item.console.toLowerCase() === currentConsole.toLowerCase());
      const matchSearch = !searchQuery || item.title.toLowerCase().includes(searchQuery);
      return matchConsole && matchSearch;
    });

    displayedCount = 0;
    gridEl.innerHTML = '';

    if (filteredLabels.length === 0) {
      const emptyDiv = document.createElement('div');
      emptyDiv.className = 'empty-state';
      emptyDiv.style.gridColumn = '1 / -1';
      emptyDiv.innerHTML = `
        <div class="empty-state-icon">🏷️</div>
        <h3 class="empty-state-title">No matching cartridge labels found</h3>
        <p class="empty-state-desc">No labels match "${searchQuery || currentConsole}". Try another game title or switch to "All Labels".</p>
        <button type="button" class="btn btn-emerald btn-sm empty-state-reset">Reset Search & Console Filter</button>
      `;
      const resetBtn = emptyDiv.querySelector('.empty-state-reset');
      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          if (searchInput) searchInput.value = '';
          searchQuery = '';
          currentConsole = 'all';
          consoleBtns.forEach(b => b.classList.toggle('active', b.dataset.console === 'all'));
          applyFilter();
        });
      }
      gridEl.appendChild(emptyDiv);
      if (loadMoreBtn) loadMoreBtn.style.display = 'none';
      return;
    }

    renderChunk();
  }

  function renderChunk() {
    const nextCount = Math.min(displayedCount + itemsPerPage, filteredLabels.length);
    const fragment = document.createDocumentFragment();

    for (let i = displayedCount; i < nextCount; i++) {
      const item = filteredLabels[i];
      const card = document.createElement('div');
      card.className = 'label-card';

      const thumbWrap = document.createElement('div');
      thumbWrap.className = 'label-thumb-wrap';
      thumbWrap.setAttribute('tabindex', '0');
      thumbWrap.setAttribute('role', 'button');
      thumbWrap.setAttribute('aria-label', `View ${item.title} cartridge label in high resolution`);

      const img = document.createElement('img');
      img.src = item.thumbUrl;
      img.alt = item.title;
      img.loading = 'lazy';
      img.onerror = function() {
        if (!this.dataset.fallback) {
          this.dataset.fallback = '1';
          this.src = '../' + item.thumbUrl;
        } else {
          // Auto-remove label card if thumbnail was deleted from disk
          card.remove();
        }
      };
      thumbWrap.appendChild(img);

      const infoWrap = document.createElement('div');
      infoWrap.className = 'label-info';
      infoWrap.innerHTML = `
        <span class="label-console-tag">${item.console}</span>
        <h4 class="label-title" title="${item.title}">${item.title}</h4>
        <a href="${window.masterUrl(item.downloadUrl)}" class="btn btn-emerald btn-sm label-dl-btn" ${window.masterUrl(item.downloadUrl).startsWith('http') ? 'target="_blank" rel="noopener"' : `download="${item.filename}"`}>
          Download Free
        </a>
      `;

      card.appendChild(thumbWrap);
      card.appendChild(infoWrap);

      const openModal = () => {
        const lightboxItems = filteredLabels.map(l => ({
          title: l.title,
          url: window.masterUrl(l.downloadUrl),
          console: l.console,
          filename: l.filename
        }));
        Lightbox.open(lightboxItems, i, thumbWrap);
      };

      thumbWrap.addEventListener('click', openModal);
      thumbWrap.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openModal();
        }
      });

      fragment.appendChild(card);
    }

    gridEl.appendChild(fragment);
    displayedCount = nextCount;

    if (loadMoreBtn) {
      if (displayedCount >= filteredLabels.length) {
        loadMoreBtn.style.display = 'none';
      } else {
        loadMoreBtn.style.display = 'inline-flex';
        loadMoreBtn.textContent = `Load More (${filteredLabels.length - displayedCount} remaining)`;
      }
    }
  }

  return { init };
})();

if (typeof window !== 'undefined') {
  window.LabelsHub = LabelsHub;
}
