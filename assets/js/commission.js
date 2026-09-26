/** Published commission inquiry form, owned by Santiago Salvador. */
const GOOGLE_COMMISSION_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSfd_IwNh6RA4ryV9DJunfJ93cDXP_nc98INL8ZK5mXzNAkZKA/viewform';

document.addEventListener('DOMContentLoaded', () => {
  const link = document.getElementById('commission-form-link');
  const status = document.getElementById('commission-form-status');
  if (!link || !status || !/^https:\/\/(?:docs\.google\.com\/forms\/|forms\.gle\/)/.test(GOOGLE_COMMISSION_FORM_URL)) return;
  link.href = GOOGLE_COMMISSION_FORM_URL;
  link.hidden = false;
  status.textContent = 'Share a short project brief and optional reference images. This Google Form requires sign-in because it supports file uploads. You can also email me directly.';
});
