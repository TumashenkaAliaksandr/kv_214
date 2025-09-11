document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.messenger-toggle');
  const menu = document.getElementById('messenger-options');

  toggle.addEventListener('click', () => {
    const isHidden = menu.classList.toggle('hidden');
    toggle.setAttribute('aria-expanded', !isHidden);
    menu.setAttribute('aria-hidden', isHidden);
  });
});
