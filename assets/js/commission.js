/** Replace this value with the published Google Form responder URL. */
const GOOGLE_COMMISSION_FORM_URL = '';

document.addEventListener('DOMContentLoaded', () => {
  const link = document.getElementById('commission-form-link');
  const status = document.getElementById('commission-form-status');
  if (!link || !status || !/^https:\/\/(?:docs\.google\.com\/forms\/|forms\.gle\/)/.test(GOOGLE_COMMISSION_FORM_URL)) return;
  link.href = GOOGLE_COMMISSION_FORM_URL;
  link.hidden = false;
  status.textContent = 'Share a short project brief and reference images. Google will ask you to sign in if you upload files.';
});
