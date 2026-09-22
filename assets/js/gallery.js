/**
 * Master Art Gallery Controller
 */
const ArtGallery = (function() {
  let allArtworks = [];
  let filteredArtworks = [];
  let currentFilter = 'all';
  let searchQuery = '';
  let itemsPerPage = 36;
  let displayedCount = 0;

  let gridEl, filterBtns, searchInput, loadMoreBtn;

  function init() {
    gridEl = document.getElementById('art-grid');
    filterBtns = document.querySelectorAll('.art-filter-btn');
    searchInput = document.getElementById('art-search');
    loadMoreBtn = document.getElementById('art-load-more');

    if (!gridEl) return;

    // Use synchronous offline data if present (file:// protocol safe)
    if (window.ARTWORKS_DATA && Array.isArray(window.ARTWORKS_DATA) && window.ARTWORKS_DATA.length > 0) {
      allArtworks = window.ARTWORKS_DATA;
      applyFilter();
    } else {
      // Fallback to fetch for web servers
      fetch('assets/data/artworks.json')
        .then(r => r.json())
        .then(data => {
          allArtworks = data;
          applyFilter();
        })
        .catch(err => console.error('Error loading artworks:', err));
    }

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentFilter = btn.dataset.filter;
        applyFilter();
      });
    });

    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase().trim();
        applyFilter();
      });
    }

    if (loadMoreBtn) {
      loadMoreBtn.addEventListener('click', () => {
        renderChunk();
      });
    }
  }

  function applyFilter() {
    filteredArtworks = allArtworks.filter(item => {
      const matchCat = (currentFilter === 'all') ? true :
                       (currentFilter === 'featured') ? item.featured :
                       (item.category === currentFilter);
      const matchSearch = !searchQuery || item.title.toLowerCase().includes(searchQuery);
      return matchCat && matchSearch;
    });

    displayedCount = 0;
    gridEl.innerHTML = '';
    renderChunk();
  }

  function renderChunk() {
    const nextCount = Math.min(displayedCount + itemsPerPage, filteredArtworks.length);
    const fragment = document.createDocumentFragment();

    for (let i = displayedCount; i < nextCount; i++) {
      const item = filteredArtworks[i];
      const card = document.createElement('div');
      card.className = 'art-card';
      
      const cleanUrl = item.url.startsWith('/') ? item.url.slice(1) : item.url;
      const img = document.createElement('img');
      img.className = 'art-card-img';
      img.src = cleanUrl;
      img.alt = item.title;
      img.loading = 'lazy';
      img.onerror = function() {
        if (!this.dataset.fallback) {
          this.dataset.fallback = '1';
          this.src = '../' + cleanUrl;
        } else {
          // Auto-remove card if image was deleted or missing from disk
          card.remove();
        }
      };

      const overlay = document.createElement('div');
      overlay.className = 'art-card-overlay';
      overlay.innerHTML = `
        <span class="art-card-cat">${item.categoryLabel || item.category}</span>
        <h4 class="art-card-title">${item.title}</h4>
      `;

      card.appendChild(img);
      card.appendChild(overlay);

      card.addEventListener('click', () => {
        Lightbox.open(filteredArtworks, i);
      });

      fragment.appendChild(card);
    }

    gridEl.appendChild(fragment);
    displayedCount = nextCount;

    if (loadMoreBtn) {
      if (displayedCount >= filteredArtworks.length) {
        loadMoreBtn.style.display = 'none';
      } else {
        loadMoreBtn.style.display = 'inline-flex';
        loadMoreBtn.textContent = `Load More (${filteredArtworks.length - displayedCount} remaining)`;
      }
    }
  }

  return { init };
})();

if (typeof window !== 'undefined') {
  window.ArtGallery = ArtGallery;
}
