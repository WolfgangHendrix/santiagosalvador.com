/** Full masters stay in the git repository. The published site serves thumbnails. */
window.masterUrl = function masterUrl(path) {
  if (!path || /^(?:https?:|data:|blob:)/i.test(path)) return path;
  const clean = String(path).replace(/^\//, '');
  const host = location.hostname;
  const local = !host || host === 'localhost' || host === '127.0.0.1' || host === '[::1]';
  if (local) return clean;
  const remoteMaster = clean.startsWith('Labels/fulls/')
    || (clean.startsWith('Art/') && !clean.startsWith('Art/thumbs/') && !clean.startsWith('Art/Music_Audio/'));
  if (!remoteMaster) return clean;
  const encoded = clean.split('/').map(encodeURIComponent).join('/');
  return `https://media.githubusercontent.com/media/WolfgangHendrix/santiagosalvador.com/main/${encoded}`;
};
