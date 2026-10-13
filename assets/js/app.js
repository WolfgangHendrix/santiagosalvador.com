/**
 * SantiagoSalvador.com — Main App Coordinator
 */
document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize Lightbox
  Lightbox.init();

  // 2. Initialize Galleries & Music
  ArtGallery.init();
  LabelsHub.init();
  MusicPlayer.init();
  renderGames();

  // 3. Navbar scroll effect & Mobile Menu
  const navbar = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) navbar.classList.add('scrolled');
    else navbar.classList.remove('scrolled');
  });

  const menuToggle = document.getElementById('menu-toggle');
  const mobileNav = document.getElementById('mobile-nav');
  if (menuToggle && mobileNav) {
    const toggleNav = () => {
      const isOpen = mobileNav.classList.toggle('open');
      menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      mobileNav.setAttribute('aria-hidden', isOpen ? 'false' : 'true');
    };
    menuToggle.addEventListener('click', toggleNav);
    mobileNav.querySelectorAll('.mobile-nav-link').forEach(link => {
      link.addEventListener('click', () => {
        mobileNav.classList.remove('open');
        menuToggle.setAttribute('aria-expanded', 'false');
        mobileNav.setAttribute('aria-hidden', 'true');
      });
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileNav.classList.contains('open')) {
        mobileNav.classList.remove('open');
        menuToggle.setAttribute('aria-expanded', 'false');
        mobileNav.setAttribute('aria-hidden', 'true');
        menuToggle.focus();
      }
    });
  }

  // 4. Poetry Tab Switcher
  const poemTabs = document.querySelectorAll('.poetry-tab-btn');
  const poemTitle = document.getElementById('active-poem-title');
  const poemBody = document.getElementById('active-poem-body');
  const poems = {
    angels: {
      title: "Consolation to the Angels That Slipped Through the Cracks of Time",
      body: `we share the same light that shines down from heaven above<br>
feel the same warmth that God gives us with love<br>
faith is all I have to go on<br>
alone or together we must be strong<br>
like a tree or a plant we grow towards the sky<br>
branch out in beauty and take part in this life<br>
every moment a breath, every whisper a song<br>
held in the arms of the truth that was here all along.`
    },
    cat: {
      title: "Several Names Ago (An Ode to My Cat)",
      body: `R2D2 how I love you<br>
so gently you rest upon my chest<br>
like a kitten still purrrrr and trust me with your life<br>
knowing I'd never hurt you and only treat you right<br><br>
R2D2 so far from Arturito<br>
twice removed from Arthur and even Ginger<br>
Brody long gone, where is your mom?<br>
R2 my lil head butter you<br><br>
now you're so grown, escape on your own<br>
a bucket of fleas no matter how I clean thee<br>
but outdoors is where you get it and that's where you'd rather be.`
    },
    arms: {
      title: "A.M. Hours, In the Arms of My Lover",
      body: `you text me<br>
expecting, replying<br>
I'm dying, my heart's free<br>
you left me though nothing's between<br><br>
you tied me and set me<br>
depressing, impressing<br>
I've risen, I've given<br>
my lover is driven<br><br>
the meaning? committing<br>
my kitty, no looking back or regretting.`
    },
    gameover: {
      title: "Game Over",
      body: `fish float freely from fire<br>
towards the tapering twilight<br>
looking, lovingly, losing leads<br>
repose, remember realities reason?<br><br>
heaven holds her heart hostage<br>
painfully pining prayers prisoner<br>
so she shall see subconsciously<br>
devils do develop deep despair.`
    }
  };

  if (poemTabs.length > 0 && poemTitle && poemBody) {
    poemTabs.forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.poem;
        const data = poems[key];
        if (!data) return;
        poemTabs.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        poemTitle.textContent = data.title;
        poemBody.innerHTML = `<p>${data.body}</p>`;
      });
    });
  }

  console.log('SantiagoSalvador.com loaded successfully.');
});

function renderGames() {
  const grid = document.getElementById('games-grid');
  const games = window.GAMES_DATA;
  if (!grid || !Array.isArray(games)) return;

  const badgeClass = {
    'Top Played': 'badge-gold',
    'CRT Retro': 'badge-cyan',
    'Vector Neon': 'badge-purple',
    'Cozy Arcade': 'badge-emerald',
    'Experimental': 'badge-purple',
    'Dark Horror': 'badge-purple',
    'Audio Tool': 'badge-cyan',
    'Multiplayer': 'badge-emerald'
  };

  grid.replaceChildren();
  games.forEach(game => {
    const card = document.createElement('div');
    card.className = 'game-card';

    const thumbWrap = document.createElement('div');
    thumbWrap.className = 'game-thumb-wrap';
    const badge = document.createElement('span');
    badge.className = `badge ${badgeClass[game.badge] || 'badge-cyan'} game-badge`;
    badge.textContent = game.badge || 'Play';
    const img = document.createElement('img');
    img.src = game.capsule;
    img.alt = game.title;
    img.className = 'game-thumb';
    img.loading = 'lazy';
    thumbWrap.append(badge, img);

    const content = document.createElement('div');
    content.className = 'game-content';
    const title = document.createElement('h3');
    title.className = 'game-title';
    title.textContent = game.title;
    const genre = document.createElement('span');
    genre.className = 'game-genre';
    genre.textContent = game.genre;
    const tagline = document.createElement('p');
    tagline.className = 'game-tagline';
    tagline.textContent = game.tagline;
    const actions = document.createElement('div');
    actions.className = 'game-actions';
    const play = document.createElement('a');
    play.href = game.playUrl;
    play.target = '_blank';
    play.rel = 'noopener';
    play.className = 'btn btn-cyan btn-sm';
    play.style.width = '100%';
    play.textContent = 'Play in Browser ↗';
    actions.appendChild(play);
    content.append(title, genre, tagline, actions);
    card.append(thumbWrap, content);
    grid.appendChild(card);
  });
}

// Unlisted personal archive shortcut. This is navigation, not access control.
let archiveKeys = '';
let archiveKeyTime = 0;
document.addEventListener('keydown', event => {
  if (event.repeat || event.isComposing) return;
  const key = event.key.toLowerCase();
  const isM = event.code === 'KeyM' || key === 'm';
  if (event.altKey && event.shiftKey && !event.ctrlKey && !event.metaKey && isM) {
    event.preventDefault();
    window.location.assign('marvel-archive.html');
    return;
  }

  // A modifier-free fallback for browsers or systems that intercept Alt+Shift.
  const target = event.target;
  const editing = target instanceof Element &&
    (target.closest('input, textarea, select, [role="textbox"]') || target.isContentEditable);
  if (editing || event.altKey || event.ctrlKey || event.metaKey || key.length !== 1) {
    archiveKeys = '';
    return;
  }
  const now = Date.now();
  archiveKeys = (now - archiveKeyTime > 2000 ? '' : archiveKeys) + key;
  archiveKeys = archiveKeys.slice(-6);
  archiveKeyTime = now;
  if (archiveKeys === 'marvel') {
    archiveKeys = '';
    window.location.assign('marvel-archive.html');
  }
});
