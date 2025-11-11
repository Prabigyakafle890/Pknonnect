// Initialize theme: prefers-color-scheme fallback and localStorage
// SVG icons used for the toggle button (kept here so they can be swapped easily)
const THEME_SUN_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" width="18" height="18" aria-hidden="true"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2 12h2M20 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>';
const THEME_MOON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" width="18" height="18" aria-hidden="true"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"></path></svg>';

function setTheme(dark) {
  const root = document.documentElement;
  if (dark) root.classList.add('dark');
  else root.classList.remove('dark');
  try { localStorage.setItem('pkonnect-theme', dark ? 'dark' : 'light'); } catch(e){}

  // Update visible toggle button(s) to show sun/moon instead of rotating the icon
  document.querySelectorAll('#themeToggle').forEach(btn => {
    try {
      btn.innerHTML = dark ? THEME_MOON_SVG : THEME_SUN_SVG;
      btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
    } catch(e){}
  });
}

function toggleTheme() {
  const isDark = document.documentElement.classList.contains('dark');
  console.log('[theme] toggleTheme: currentlyDark=', isDark, '-> switching to', !isDark);
  setTheme(!isDark);
}

function initThemeToggle() {
  // Attach theme toggle buttons if present
  document.querySelectorAll('#themeToggle').forEach(btn => {
    // ensure the button has an initial icon (in case template doesn't set it)
    if (!btn.innerHTML || btn.innerHTML.trim() === '') btn.innerHTML = THEME_SUN_SVG;
    btn.addEventListener('click', toggleTheme);
  });

  // restore saved theme (or respect prefers-color-scheme)
  try {
    const saved = localStorage.getItem('pkonnect-theme');
    console.log('[theme] initThemeToggle: saved theme =', saved);
    if (saved) setTheme(saved === 'dark');
    else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) setTheme(true);
    else setTheme(false);
  } catch(e){ setTheme(false); }
}

// Run initThemeToggle now if DOM is already ready, otherwise wait for DOMContentLoaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initThemeToggle);
} else {
  initThemeToggle();
}

// Optional: Close gallery modal when clicked outside
window.addEventListener('click', function(event) {
  const galleryModal = document.getElementById('galleryModal');
  if (galleryModal && event.target === galleryModal) {
    // click on overlay closes gallery
    closeGallery();
  }
});

/* Gallery functionality -------------------------------------------------- */
function populateGallery() {
  const grid = document.getElementById('galleryGrid');
  if (!grid || !window.PK_GALLERY_IMAGES) return;
  grid.innerHTML = '';
  window.PK_GALLERY_IMAGES.forEach((entry, idx) => {
    const item = document.createElement('div');
    item.className = 'gallery-item animated-pop';
    item.style.animationDelay = (idx * 40) + 'ms';

    // Build a safe, encoded URL for the image. If the entry already looks like a URL/path, use as-is.
    let src = entry;
    if (!entry.startsWith('/') && !entry.startsWith('http')) {
      // static folder path for gallery images
      src = '/static/img/PKonnect_gallery/' + encodeURIComponent(entry);
    }

    const img = document.createElement('img');
    img.src = src;
    img.alt = 'Photo ' + (idx + 1);
    img.loading = 'lazy';
    item.appendChild(img);

    item.addEventListener('click', () => openLightbox(src));
    grid.appendChild(item);
  });
}

function openGallery() {
  const modal = document.getElementById('galleryModal');
  if (!modal) return;
  populateGallery();
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
}

function closeGallery() {
  const modal = document.getElementById('galleryModal');
  if (!modal) return;
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
  closeLightbox();
}

function openLightbox(src) {
  const lb = document.getElementById('galleryLightbox');
  const img = document.getElementById('lightboxImg');
  if (!lb || !img) return;
  img.src = src;
  lb.classList.add('visible');
  lb.setAttribute('aria-hidden', 'false');
}

function closeLightbox() {
  const lb = document.getElementById('galleryLightbox');
  const img = document.getElementById('lightboxImg');
  if (!lb || !img) return;
  lb.classList.remove('visible');
  lb.setAttribute('aria-hidden', 'true');
  img.src = '';
}

document.addEventListener('DOMContentLoaded', function(){
  const openBtn = document.getElementById('openGalleryBtn');
  const closeBtn = document.getElementById('closeGalleryBtn');
  const lightboxClose = document.getElementById('lightboxClose');
  if (openBtn) openBtn.addEventListener('click', openGallery);
  if (closeBtn) closeBtn.addEventListener('click', closeGallery);
  if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);

  // close on ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeLightbox();
      closeGallery();
    }
  });
});