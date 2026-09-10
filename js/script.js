// MSARO GUIDE TANZANIA — Static Site Scripts

document.addEventListener('DOMContentLoaded', function () {

  /* AOS scroll animations */
  if (window.AOS) {
    AOS.init({ duration: 800, once: true, offset: 60 });
  }

  /* Navbar shrink on scroll */
  const navbar = document.getElementById('mainNav');
  function onScroll() {
    if (navbar) navbar.classList.toggle('scrolled', window.scrollY > 60);
    const toTop = document.getElementById('toTopBtn');
    if (toTop) toTop.classList.toggle('show', window.scrollY > 500);
  }
  window.addEventListener('scroll', onScroll);
  onScroll();

  /* Active nav link = current page, matched via body[data-page] */
  const groups = {
    about: 'about-group',
    guides: 'about-group',
    certifications: 'about-group',
    packages: 'packages-group'
  };
  const currentPage = document.body.getAttribute('data-page');
  if (currentPage) {
    document.querySelectorAll('[data-page-link]').forEach((link) => {
      const val = link.getAttribute('data-page-link');
      if (val === currentPage || val === groups[currentPage]) link.classList.add('active');
    });
  }

  /* ---------- Mobile sidebar ---------- */
  const sidebar = document.getElementById('mobileSidebar');
  const overlay = document.getElementById('sidebarOverlay');
  const openBtn = document.getElementById('sidebarOpenBtn');
  const closeBtn = document.getElementById('sidebarCloseBtn');

  function openSidebar() {
    if (!sidebar) return;
    sidebar.classList.add('open');
    overlay.classList.add('open');
    document.body.classList.add('sidebar-open');
  }
  function closeSidebar() {
    if (!sidebar) return;
    sidebar.classList.remove('open');
    overlay.classList.remove('open');
    document.body.classList.remove('sidebar-open');
  }
  if (openBtn) openBtn.addEventListener('click', openSidebar);
  if (closeBtn) closeBtn.addEventListener('click', closeSidebar);
  if (overlay) overlay.addEventListener('click', closeSidebar);

  /* Sidebar submenu (Packages) accordion toggle */
  document.querySelectorAll('.sb-toggle').forEach((btn) => {
    btn.addEventListener('click', function () {
      const sub = document.getElementById(this.getAttribute('data-target'));
      const caret = this.querySelector('.sb-caret');
      if (sub) sub.classList.toggle('open');
      if (caret) caret.classList.toggle('open');
    });
  });

  /* Back to top button */
  const toTopBtn = document.getElementById('toTopBtn');
  if (toTopBtn) {
    toTopBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  /* Typed.js hero tagline */
  if (window.Typed && document.getElementById('typed-hero')) {
    new Typed('#typed-hero', {
      strings: [
        'Explore Tanzania With Local Professional Guides',
        'Climb Kilimanjaro With a Certified Local Guide',
        'Safari Tarangire, Serengeti &amp; Ngorongoro',
        'Trek Mount Meru &amp; Udzungwa'
      ],
      typeSpeed: 42,
      backSpeed: 18,
      backDelay: 1600,
      startDelay: 300,
      loop: true,
      smartBackspace: true
    });
  }

  /* CountUp.js stats, triggered once visible */
  const counters = document.querySelectorAll('[data-countup]');
  if (counters.length && window.countUp) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const end = parseFloat(el.getAttribute('data-countup'));
          const decimals = el.getAttribute('data-decimals') ? parseInt(el.getAttribute('data-decimals')) : 0;
          const suffix = el.getAttribute('data-suffix') || '';
          const cu = new window.countUp.CountUp(el, end, { duration: 2, decimalPlaces: decimals, suffix: suffix });
          if (!cu.error) cu.start();
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.4 });
    counters.forEach((c) => observer.observe(c));
  }

  /* Swiper — testimonials */
  if (window.Swiper && document.querySelector('.testi-swiper')) {
    new Swiper('.testi-swiper', {
      slidesPerView: 1,
      spaceBetween: 24,
      loop: true,
      autoplay: { delay: 5000, disableOnInteraction: false },
      pagination: { el: '.testi-swiper .swiper-pagination', clickable: true },
      breakpoints: {
        768: { slidesPerView: 2 },
        992: { slidesPerView: 3 }
      }
    });
  }

  /* Swiper — destinations */
  if (window.Swiper && document.querySelector('.dest-swiper')) {
    new Swiper('.dest-swiper', {
      slidesPerView: 1.15,
      spaceBetween: 18,
      loop: true,
      autoplay: { delay: 3800, disableOnInteraction: false },
      navigation: {
        nextEl: '.dest-swiper .swiper-next',
        prevEl: '.dest-swiper .swiper-prev'
      },
      breakpoints: {
        576: { slidesPerView: 2.2 },
        992: { slidesPerView: 3.2 },
        1200: { slidesPerView: 4.2 }
      }
    });
  }

  /* GLightbox — gallery */
  if (window.GLightbox) {
    GLightbox({ selector: '.glightbox' });
  }

  /* WhatsApp booking form: build a prefilled wa.me message and open it */
  const bookingForm = document.getElementById('bookingForm');
  if (bookingForm) {
    const PEMBA_TRIPS = ['Misali Island Day Trip', 'Ngezi Forest Tour', 'Sandbank & Snorkeling Trip'];
    const MUSSA_WA = '255749235394';
    const MASUD_WA = '255749235394';

    bookingForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const name = document.getElementById('bf-name').value.trim();
      const phone = document.getElementById('bf-phone').value.trim();
      const email = document.getElementById('bf-email').value.trim();
      const country = document.getElementById('bf-country').value.trim();
      const trip = document.getElementById('bf-trip').value;
      const dates = document.getElementById('bf-dates').value.trim();
      const people = document.getElementById('bf-people').value.trim();
      const budget = document.getElementById('bf-budget').value.trim();
      const message = document.getElementById('bf-message').value.trim();

      let text = 'Hello! I would like to request a booking.\n\n';
      text += 'BOOKING REQUEST\n';
      text += '----------------------\n';
      text += `Name: ${name}\n`;
      text += `Phone/WhatsApp: ${phone}\n`;
      if (email) text += `Email: ${email}\n`;
      if (country) text += `Nationality: ${country}\n`;
      text += `Trip: ${trip}\n`;
      if (dates) text += `Preferred Start Date: ${dates}\n`;
      text += `Number of People: ${people}\n`;
      if (budget) text += `Budget Range: ${budget}\n`;
      if (message) text += `Notes: ${message}\n`;
      text += '----------------------\n';
      text += 'Sent from the Msaro Guide Tanzania website.';

      const targetNumber = PEMBA_TRIPS.includes(trip) ? MASUD_WA : MUSSA_WA;
      const url = 'https://wa.me/' + targetNumber + '?text=' + encodeURIComponent(text);
      window.open(url, '_blank');
    });
  }

  /* Per-itinerary booking forms (packages.html) — one under every route/trip */
  document.querySelectorAll('.itin-booking-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const trip = form.dataset.trip || '';
      const waNumber = form.dataset.wa || '255749235394';
      const get = (n) => { const el = form.querySelector('[name="' + n + '"]'); return el ? el.value.trim() : ''; };

      const name = get('bf-name');
      const phone = get('bf-phone');
      const email = get('bf-email');
      const country = get('bf-country');
      const people = get('bf-people');
      const dates = get('bf-dates');
      const message = get('bf-message');

      let text = 'Hello! I would like to request a booking.\n\n';
      text += 'BOOKING REQUEST\n';
      text += '----------------------\n';
      text += `Trip: ${trip}\n`;
      text += `Name: ${name}\n`;
      text += `Phone/WhatsApp: ${phone}\n`;
      if (email) text += `Email: ${email}\n`;
      if (country) text += `Nationality: ${country}\n`;
      text += `Number of People: ${people}\n`;
      if (dates) text += `Preferred Start Date: ${dates}\n`;
      if (message) text += `Notes: ${message}\n`;
      text += '----------------------\n';
      text += 'Sent from the Msaro Guide Tanzania website.';

      const url = 'https://wa.me/' + waNumber + '?text=' + encodeURIComponent(text);
      window.open(url, '_blank');
    });
  });

  /* Image placeholder fallback: show icon tile if a photo file is missing */
  document.querySelectorAll('.ph img').forEach((img) => {
    img.addEventListener('error', function () {
      this.style.display = 'none';
      const fb = this.parentElement.querySelector('.ph-fallback');
      if (fb) fb.style.display = 'flex';
    });
  });

  /* Hero background photo: hide cleanly (keep gradient) if the file is missing */
  document.querySelectorAll('.hero-bg-img').forEach((img) => {
    img.addEventListener('error', function () { this.style.display = 'none'; });
  });

});

/* ---------- WhatsApp floating menu (choose a number) ---------- */
document.addEventListener('DOMContentLoaded', function () {
  const waBtn = document.getElementById('waFloatBtn');
  const waWrap = document.getElementById('waFloatWrap');
  if (waBtn && waWrap) {
    waBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      waWrap.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (waWrap.classList.contains('open') && !waWrap.contains(e.target)) {
        waWrap.classList.remove('open');
      }
    });
  }
});

/* ---------- Language switcher (EN / ES) — cookie + reload method ----------
   This is the reliable way to drive Google Translate: we set the same
   cookie Google's own widget reads on load, then reload the page. This
   avoids depending on the internal dropdown markup Google sometimes
   changes, which is the usual reason the old "click the hidden select"
   trick stops working. Requires the site to be served over http/https
   (a real host, not opened as a local file) since it relies on cookies. */
(function () {
  function getHostname() {
    try { return window.location.hostname; } catch (e) { return ''; }
  }
  /* localhost / 127.0.0.1 / file:// are not real registrable domains —
     browsers reject a cookie with a "domain=.host" attribute for these,
     which silently breaks the language switch during local testing.
     Only add the domain attribute for a real public hostname. */
  function isLocalHost(host) {
    return !host || host === 'localhost' || host === '127.0.0.1' || host === '' ||
      window.location.protocol === 'file:' || /^(\d{1,3}\.){3}\d{1,3}$/.test(host);
  }
  function setLangCookie(lang) {
    const host = getHostname();
    document.cookie = 'googtrans=/en/' + lang + '; path=/;';
    if (host && !isLocalHost(host)) {
      document.cookie = 'googtrans=/en/' + lang + '; path=/; domain=.' + host + ';';
    }
  }
  function clearLangCookie() {
    const host = getHostname();
    document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    if (host && !isLocalHost(host)) {
      document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.' + host + ';';
    }
  }
  window.changeSiteLanguage = function (lang) {
    if (localStorage.getItem('msaroLang') === lang) return;
    localStorage.setItem('msaroLang', lang);
    if (lang === 'en') {
      clearLangCookie();
    } else {
      setLangCookie(lang);
    }
    location.reload();
  };
  document.addEventListener('DOMContentLoaded', function () {
    const saved = localStorage.getItem('msaroLang') || 'en';
    document.querySelectorAll('.lang-btn').forEach(function (btn) {
      btn.classList.toggle('active', btn.getAttribute('data-lang') === saved);
      btn.addEventListener('click', function () {
        window.changeSiteLanguage(btn.getAttribute('data-lang'));
      });
    });
  });
})();

/* ---------- 3D tilt + glare effect for cards (desktop pointer only) ---------- */
(function () {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (reduceMotion || !finePointer) return;

  const selector = '.pkg-card, .guide-card, .cert-card, .testi-card, .dest-card';
  /* Keep in sync with --ease in css/style.css. Setting the full
     `transition` shorthand (instead of just transitionDuration) is
     required so box-shadow/border-color keep transitioning smoothly —
     but that means every override below must re-list ALL three
     properties, or the missing ones silently stop transitioning. */
  const EASE = 'cubic-bezier(0.4,0,0.2,1)';
  const TILT_IN = 'transform .1s linear, box-shadow .5s ' + EASE + ', border-color .4s ' + EASE;
  const TILT_OUT = 'transform .6s cubic-bezier(.22,.85,.3,1.15), box-shadow .5s ' + EASE + ', border-color .4s ' + EASE;

  function bindTilt(el) {
    function onEnter() {
      el.style.transition = TILT_IN;
      el.classList.add('tilting');
    }
    function onMove(e) {
      // Recomputed every move (cheap for a handful of cards) rather than
      // cached on enter, so a scroll mid-hover can't leave stale
      // coordinates driving the tilt math.
      const rect = el.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = (e.clientY - rect.top) / rect.height;
      const rotY = (x - 0.5) * 10;
      const rotX = (0.5 - y) * 7;
      el.style.transform = 'perspective(1000px) rotateX(' + rotX + 'deg) rotateY(' + rotY + 'deg) translateY(-8px) scale(1.02)';
      el.style.setProperty('--glare-x', (x * 100) + '%');
      el.style.setProperty('--glare-y', (y * 100) + '%');
    }
    function onLeave() {
      el.classList.remove('tilting');
      el.style.transition = TILT_OUT;
      el.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0) scale(1)';
    }

    el.addEventListener('mouseenter', onEnter);
    el.addEventListener('mousemove', onMove);
    el.addEventListener('mouseleave', onLeave);
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll(selector).forEach(bindTilt);
  });
})();

/* ---------- Mobile sidebar — staggered menu entrance ---------- */
document.addEventListener('DOMContentLoaded', function () {
  const navItems = document.querySelectorAll('.mobile-sidebar .nav-flex > *');
  navItems.forEach(function (item, i) {
    item.style.transitionDelay = (i * 0.045) + 's';
  });
});
