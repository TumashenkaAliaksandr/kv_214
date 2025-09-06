document.addEventListener('DOMContentLoaded', () => {
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav');

  const saleUrlElem = document.getElementById('url-sale');
  const rentUrlElem = document.getElementById('url-rent');
  const saleUrl = saleUrlElem ? saleUrlElem.href : '#';
  const rentUrl = rentUrlElem ? rentUrlElem.href : '#';

  function addAllObjectsMenu() {
    if (window.innerWidth > 767) {
      const allPropsItems = document.querySelectorAll('.all-properties');
      allPropsItems.forEach(item => item.remove());
      return;
    }

    const saleDropdownMenu = document.querySelector('.sale-dropdown > .dropdown-menu');
    if (saleDropdownMenu && !saleDropdownMenu.querySelector('.all-properties')) {
      const li = document.createElement('li');
      li.classList.add('all-properties');
      li.innerHTML = `<a href="${saleUrl}"><i class="fa-solid fa-house"></i> Все объекты</a>`;
      saleDropdownMenu.appendChild(li);
    }

    const rentDropdownMenu = document.querySelector('.rent-dropdown > .dropdown-menu');
    if (rentDropdownMenu && !rentDropdownMenu.querySelector('.all-properties')) {
      const li = document.createElement('li');
      li.classList.add('all-properties');
      li.innerHTML = `<a href="${rentUrl}"><i class="fa-solid fa-key"></i> Все объекты</a>`;
      rentDropdownMenu.appendChild(li);
    }
  }

  function disableMainLinkOnMobile() {
    const saleLink = document.querySelector('.sale-dropdown > a');
    const rentLink = document.querySelector('.rent-dropdown > a');

    function clickHandler(e) {
      if (window.innerWidth <= 767) {
        e.preventDefault();
      }
    }

    if (saleLink) {
      saleLink.removeEventListener('click', clickHandler);
      saleLink.addEventListener('click', clickHandler);
    }

    if (rentLink) {
      rentLink.removeEventListener('click', clickHandler);
      rentLink.addEventListener('click', clickHandler);
    }
  }

   // Открытие/закрытие меню по клику на бургер
  burger.addEventListener('click', (e) => {
    e.stopPropagation(); // предотвращаем всплытие, чтобы клик не закрыл меню мгновенно
    burger.classList.toggle('active'); // переключаем крестик
    const expanded = burger.getAttribute('aria-expanded') === 'true';
    burger.setAttribute('aria-expanded', !expanded);
    nav.classList.toggle('active');
    nav.setAttribute('aria-hidden', expanded);
  });

  function init() {
    addAllObjectsMenu();
    disableMainLinkOnMobile();
  }

  init();

  window.addEventListener('resize', () => {
    init();
  });
});
