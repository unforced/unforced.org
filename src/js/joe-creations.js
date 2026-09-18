(() => {
  const photo = document.getElementById('selected-photo');
  if (!photo) return;
  document.documentElement.classList.add('js');
  const thumbnails = [...document.querySelectorAll('.thumbnail')];
  const gallery = document.body.classList.contains('is-gallery');
  const status = document.getElementById('photo-status');
  const full = document.getElementById('full-photo');
  let current = Math.max(0, thumbnails.findIndex(link => link.dataset.photo === photo.getAttribute('src')));
  let request = 0;

  function select(index) {
    const link = thumbnails[index];
    if (!link || !link.dataset.photo) return;
    current = index;
    const ticket = ++request;
    const next = new Image();
    next.onload = () => {
      if (ticket !== request) return;
      photo.src = link.dataset.photo;
      photo.alt = link.dataset.label;
      if (full) full.href = link.dataset.photo;
      if (status) status.textContent = `Photograph ${index + 1} of ${thumbnails.length}`;
      thumbnails.forEach((item, n) => {
        if (gallery && n === index) item.setAttribute('aria-current', 'true');
        else item.removeAttribute('aria-current');
      });
    };
    next.onerror = () => {
      if (ticket === request && status) status.textContent = 'Photograph could not load. Select it again to retry.';
    };
    next.src = link.dataset.photo;
  }

  thumbnails.forEach((link, index) => {
    link.addEventListener('pointerenter', event => {
      if (event.pointerType === 'mouse') select(index);
    });
    link.addEventListener('focus', () => select(index));
    if (gallery) link.addEventListener('click', event => {
      // Preserve normal link behavior for opening the original-size photo.
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      select(index);
    });
    link.addEventListener('keydown', event => {
      if (!gallery || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
      event.preventDefault();
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? thumbnails.length - 1
        : (index + (event.key === 'ArrowLeft' ? -1 : 1) + thumbnails.length) % thumbnails.length;
      thumbnails[next].focus();
    });
  });
  document.querySelectorAll('[data-step]').forEach(button => button.addEventListener('click', () => {
    select((current + Number(button.dataset.step) + thumbnails.length) % thumbnails.length);
  }));
  if (gallery) select(current);
})();
