/* =============================================
   ASHA GARMENT FACTORY — Shared page script
   Used by the homepage and every service page.
   ============================================= */

/* — Navbar scroll shadow — */
const navbar = document.getElementById('navbar');
const onScroll = () => navbar.classList.toggle('scrolled', window.scrollY > 60);
window.addEventListener('scroll', onScroll, { passive: true });

/* — Mobile nav toggle — */
const toggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');
const setMenu = (open) => {
  navLinks.classList.toggle('open', open);
  toggle.setAttribute('aria-expanded', open);
};
toggle.addEventListener('click', () => setMenu(!navLinks.classList.contains('open')));
document.querySelectorAll('.nav-links a').forEach(link =>
  link.addEventListener('click', () => setMenu(false))
);

/* — Intro video (homepage only): play only while on screen — */
const introVideo = document.getElementById('intro-video');
if (introVideo && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) introVideo.play().catch(() => { });
    else introVideo.pause();
  }, { threshold: 0.35 }).observe(introVideo);
}

/* — Scroll reveal — */
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
    }
  });
}, { threshold: 0.10, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

/* — FAQ accordion — */
document.querySelectorAll('.faq-q').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(el => {
      el.classList.remove('open');
      el.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
    });
    if (!isOpen) {
      item.classList.add('open');
      btn.setAttribute('aria-expanded', 'true');
    }
  });
});

/*
 * — Lead source —
 * Remembers where the visitor first arrived from (search engine, AI tool,
 * directory…) and which page they landed on, so each quote request in the
 * sheet shows which page and channel produced it.
 */
const SOURCE_KEY = 'agf-source';
const getLeadSource = () => {
  try {
    const saved = sessionStorage.getItem(SOURCE_KEY);
    if (saved) return JSON.parse(saved);
  } catch { }
  const ref = document.referrer;
  const source = {
    landing: location.pathname,
    referrer: ref && new URL(ref).host !== location.host ? ref : '(direct)',
    utm: new URLSearchParams(location.search).get('utm_source') || ''
  };
  try { sessionStorage.setItem(SOURCE_KEY, JSON.stringify(source)); } catch { }
  return source;
};
const leadSource = getLeadSource();

/* — Quote form submission — */
const form = document.getElementById('quote-form');
const successMsg = document.getElementById('form-success');

/*
 * The form posts to the Google Apps Script web app (Code.gs), which logs
 * each request to the "Quote Requests" sheet and emails a notification.
 */
const SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwElEcpKldf3kNuXworSTfBozzYf11jbozgzE2SQRuhcl1FTX9DGMVHxaXJKtxsIblaIw/exec';

if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending…';
    successMsg.className = 'success-msg';

    const payload = {};
    new FormData(form).forEach((val, key) => payload[key] = val);
    payload.timestamp = new Date().toISOString();
    payload.page = location.pathname;
    Object.assign(payload, leadSource);

    try {
      const res = await fetch(SCRIPT_URL, {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      const result = res.ok ? await res.json() : null;
      if (result && result.result === 'success') {
        successMsg.textContent = '✓ Thank you! We\'ll get back to you within 24 hours.';
        successMsg.classList.add('show');
        form.reset();
      } else {
        throw new Error('Server error');
      }
    } catch {
      successMsg.textContent = 'Something went wrong. Please email us at ashagarmentfactory@gmail.com';
      successMsg.classList.add('error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Send My Request';
      successMsg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  });
}
