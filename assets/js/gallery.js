/** Art portfolio and separate cards reference collection. */
const ArtGallery = (function() {
  const PAGE_SIZE = 36;

  function createGallery(config) {
    const grid = document.getElementById(config.gridId);
    const search = document.getElementById(config.searchId);
    const more = document.getElementById(config.moreId);
    const buttons = [...document.querySelectorAll(config.filterSelector)];
    let items = [];
    let visible = [];
    let shown = 0;
    let filter = config.initialFilter;

    function updateCounts() {
      buttons.forEach(button => {
        const category = button.dataset.filter;
        const count = category === 'all' ? items.length :
          items.filter(item => category === 'featured' ? item.featured : item.category === category).length;
        button.textContent = `${button.dataset.label} (${count})`;
      });
    }

    function setActiveFilter() {
      buttons.forEach(button => {
        const active = button.dataset.filter === filter;
        button.classList.toggle('active', active);
        button.setAttribute('aria-pressed', String(active));
      });
    }

    function makeCard(item, index) {
      const card = document.createElement('div');
      card.className = 'art-card';
      card.tabIndex = 0;
      card.setAttribute('role', 'button');
      card.setAttribute('aria-label', `View ${item.title}`);
      const img = document.createElement('img');
      img.className = 'art-card-img';
      img.src = (item.thumb || item.url).replace(/^\//, '');
      img.alt = item.title;
      img.loading = 'lazy';
      img.addEventListener('error', () => {
        const master = item.url.replace(/^\//, '');
        if (img.dataset.fallback || img.src.endsWith(master)) return;
        img.dataset.fallback = '1';
        img.src = master;
      });
      const overlay = document.createElement('div');
      overlay.className = 'art-card-overlay';
      const category = document.createElement('span');
      category.className = 'art-card-cat';
      category.textContent = item.categoryLabel || item.category;
      const title = document.createElement('h4');
      title.className = 'art-card-title';
      title.textContent = item.title;
      overlay.append(category, title);
      card.append(img, overlay);
      const open = () => {
        const view = visible.map(entry => ({ ...entry, url: window.masterUrl(entry.url) }));
        Lightbox.open(view, index, card);
      };
      card.addEventListener('click', open);
      card.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          open();
        }
      });
      return card;
    }

    function renderChunk() {
      const next = Math.min(shown + PAGE_SIZE, visible.length);
      const fragment = document.createDocumentFragment();
      for (let index = shown; index < next; index++) fragment.appendChild(makeCard(visible[index], index));
      grid.appendChild(fragment);
      shown = next;
      if (more) {
        more.hidden = shown >= visible.length;
        more.textContent = `Load More (${visible.length - shown} remaining)`;
      }
    }

    function applyFilter() {
      const query = (search?.value || '').toLowerCase().trim();
      visible = items.filter(item => {
        const matchesCategory = filter === 'all' || (filter === 'featured' ? item.featured : item.category === filter);
        return matchesCategory && (!query || item.title.toLowerCase().includes(query));
      });
      grid.replaceChildren();
      shown = 0;
      if (!visible.length) {
        const empty = document.createElement('div');
        empty.className = 'empty-state';
        const heading = document.createElement('h3');
        heading.className = 'empty-state-title';
        heading.textContent = 'No matching items found';
        const hint = document.createElement('p');
        hint.className = 'empty-state-desc';
        hint.textContent = 'Try another search or clear the filters.';
        const reset = document.createElement('button');
        reset.type = 'button';
        reset.className = 'btn btn-outline btn-sm';
        reset.textContent = 'Clear search and filters';
        reset.addEventListener('click', () => {
          if (search) search.value = '';
          filter = config.initialFilter;
          setActiveFilter();
          applyFilter();
        });
        empty.append(heading, hint, reset);
        grid.appendChild(empty);
        if (more) more.hidden = true;
        return;
      }
      renderChunk();
    }

    buttons.forEach(button => button.addEventListener('click', () => {
      filter = button.dataset.filter;
      setActiveFilter();
      applyFilter();
    }));
    search?.addEventListener('input', () => {
      // Search the whole original-art archive when a visitor starts on Selected Work.
      if (filter === 'featured' && search.value.trim()) {
        filter = 'all';
        setActiveFilter();
      }
      applyFilter();
    });
    more?.addEventListener('click', renderChunk);

    return {
      setItems(nextItems) {
        items = nextItems;
        updateCounts();
        setActiveFilter();
        applyFilter();
      }
    };
  }

  function init() {
    const portfolio = createGallery({
      gridId: 'art-grid', searchId: 'art-search', moreId: 'art-load-more',
      filterSelector: '.art-filter-btn', initialFilter: 'featured'
    });
    const cards = createGallery({
      gridId: 'cards-grid', searchId: 'cards-search', moreId: 'cards-load-more',
      filterSelector: '.cards-filter-btn', initialFilter: 'all'
    });
    const useData = data => {
      portfolio.setItems(data.filter(item => item.category !== 'cards'));
      cards.setItems(data.filter(item => item.category === 'cards'));
    };
    if (Array.isArray(window.ARTWORKS_DATA)) {
      useData(window.ARTWORKS_DATA);
    } else {
      fetch('assets/data/artworks.json').then(response => response.json()).then(useData)
        .catch(error => console.error('Error loading artworks:', error));
    }
  }

  return { init };
})();

if (typeof window !== 'undefined') window.ArtGallery = ArtGallery;
