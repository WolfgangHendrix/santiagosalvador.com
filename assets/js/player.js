/**
 * Ambient Audio Player Controller
 */
const MusicPlayer = (function() {
  let audio = new Audio();
  let playlist = [];
  let currentIndex = 0;
  let isPlaying = false;

  let playBtn, prevBtn, nextBtn, timeline, currentTimeEl, totalTimeEl, volSlider;
  let trackTitleEl, trackArtistEl, waveformEl, listToggleBtn, drawerEl, listContainer, listSearch;

  function init() {
    playBtn = document.getElementById('player-play-btn');
    prevBtn = document.getElementById('player-prev-btn');
    nextBtn = document.getElementById('player-next-btn');
    timeline = document.getElementById('player-timeline');
    currentTimeEl = document.getElementById('player-current-time');
    totalTimeEl = document.getElementById('player-total-time');
    volSlider = document.getElementById('player-volume');
    trackTitleEl = document.getElementById('player-track-title');
    trackArtistEl = document.getElementById('player-track-artist');
    waveformEl = document.getElementById('player-waveform');
    listToggleBtn = document.getElementById('player-list-toggle');
    drawerEl = document.getElementById('playlist-drawer');
    listContainer = document.getElementById('playlist-items');
    listSearch = document.getElementById('playlist-search-input');

    if (!playBtn) return;

    if (window.MUSIC_DATA && Array.isArray(window.MUSIC_DATA) && window.MUSIC_DATA.length > 0) {
      playlist = window.MUSIC_DATA;
      loadTrack(0, false);
      renderPlaylist(playlist);
    } else {
      fetch('assets/data/music.json')
        .then(r => r.json())
        .then(data => {
          playlist = data;
          if (playlist.length > 0) {
            loadTrack(0, false);
            renderPlaylist(playlist);
          }
        })
        .catch(err => console.error('Error loading music:', err));
    }

    playBtn.addEventListener('click', togglePlay);
    prevBtn.addEventListener('click', prevTrack);
    nextBtn.addEventListener('click', nextTrack);

    audio.addEventListener('play', () => {
      isPlaying = true;
      updateUI();
    });
    audio.addEventListener('pause', () => {
      isPlaying = false;
      updateUI();
    });
    audio.addEventListener('timeupdate', updateProgress);
    audio.addEventListener('ended', nextTrack);

    if (timeline) {
      timeline.addEventListener('input', () => {
        if (audio.duration) {
          audio.currentTime = (timeline.value / 100) * audio.duration;
        }
      });
    }

    if (volSlider) {
      volSlider.addEventListener('input', (e) => {
        audio.volume = e.target.value / 100;
      });
    }

    if (listToggleBtn && drawerEl) {
      listToggleBtn.addEventListener('click', () => {
        drawerEl.classList.toggle('open');
      });
    }

    if (listSearch) {
      listSearch.addEventListener('input', (e) => {
        const q = e.target.value.toLowerCase().trim();
        const filtered = playlist.filter(t => t.title.toLowerCase().includes(q));
        renderPlaylist(filtered);
      });
    }
  }

  function loadTrack(index, autoPlay = true) {
    currentIndex = index;
    const track = playlist[currentIndex];
    if (!track) return;

    const cleanUrl = track.url.startsWith('/') ? track.url.slice(1) : track.url;
    audio.src = cleanUrl;
    audio.dataset.fallback = '';
    audio.onerror = function() {
      if (!audio.dataset.fallback) {
        audio.dataset.fallback = '1';
        audio.src = '../' + cleanUrl;
      }
    };

    if (trackTitleEl) trackTitleEl.textContent = track.title;
    if (trackArtistEl) trackArtistEl.textContent = `${track.album} • ${track.artist}`;

    highlightPlaylistItem(track.id);

    if (autoPlay) {
      audio.play().catch(e => {
        console.log('Playback prevented:', e);
        isPlaying = false;
        updateUI();
      });
    } else {
      isPlaying = false;
      updateUI();
    }
  }

  function togglePlay() {
    if (!audio.src) {
      if (playlist.length > 0) loadTrack(0, true);
      return;
    }

    if (audio.paused) {
      audio.play().catch(e => console.log('Playback failed:', e));
    } else {
      audio.pause();
    }
  }

  function prevTrack() {
    if (playlist.length === 0) return;
    const idx = (currentIndex - 1 + playlist.length) % playlist.length;
    loadTrack(idx, true);
  }

  function nextTrack() {
    if (playlist.length === 0) return;
    const idx = (currentIndex + 1) % playlist.length;
    loadTrack(idx, true);
  }

  function updateUI() {
    if (playBtn) {
      playBtn.setAttribute('aria-label', isPlaying ? 'Pause audio' : 'Play audio');
      playBtn.setAttribute('title', isPlaying ? 'Pause' : 'Play');
      playBtn.innerHTML = isPlaying ? 
        '<svg width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5z"/></svg>' :
        '<svg width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="m11.596 8.697-6.363 3.692c-.54.313-1.233-.066-1.233-.697V4.308c0-.63.692-1.01 1.233-.696l6.363 3.692a.802.802 0 0 1 0 1.393z"/></svg>';
    }
    if (waveformEl) {
      if (isPlaying) waveformEl.classList.add('playing');
      else waveformEl.classList.remove('playing');
    }
  }

  function updateProgress() {
    if (!audio.duration) return;
    const current = audio.currentTime;
    const total = audio.duration;
    if (timeline) timeline.value = (current / total) * 100;
    if (currentTimeEl) currentTimeEl.textContent = formatTime(current);
    if (totalTimeEl) totalTimeEl.textContent = formatTime(total);
  }

  function formatTime(secs) {
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  }

  function renderPlaylist(items) {
    if (!listContainer) return;
    listContainer.innerHTML = items.map(t => `
      <li class="playlist-item ${playlist[currentIndex] && playlist[currentIndex].id === t.id ? 'active' : ''}" data-id="${t.id}">
        <span>${t.title}</span>
        <span style="font-size:0.75rem;color:var(--text-muted);">${t.album}</span>
      </li>
    `).join('');

    listContainer.querySelectorAll('.playlist-item').forEach(el => {
      el.addEventListener('click', () => {
        const id = parseInt(el.dataset.id);
        const idx = playlist.findIndex(t => t.id === id);
        if (idx !== -1) loadTrack(idx, true);
      });
    });
  }

  function highlightPlaylistItem(trackId) {
    if (!listContainer) return;
    listContainer.querySelectorAll('.playlist-item').forEach(el => {
      if (parseInt(el.dataset.id) === trackId) el.classList.add('active');
      else el.classList.remove('active');
    });
  }

  return { init, togglePlay };
})();

if (typeof window !== 'undefined') {
  window.MusicPlayer = MusicPlayer;
}
