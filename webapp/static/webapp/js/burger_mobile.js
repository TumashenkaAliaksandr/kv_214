document.addEventListener('DOMContentLoaded', () => {
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav');

  burger.addEventListener('click', () => {
    const expanded = burger.getAttribute('aria-expanded') === 'true' || false;
    burger.setAttribute('aria-expanded', !expanded);
    nav.classList.toggle('active');
  });

  // Закрываем меню при клике вне меню (опционально)
  document.addEventListener('click', (e) => {
    if (!nav.contains(e.target) && !burger.contains(e.target)) {
      nav.classList.remove('active');
      burger.setAttribute('aria-expanded', false);
    }
  });
});
