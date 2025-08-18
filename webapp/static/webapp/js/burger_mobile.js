document.addEventListener('DOMContentLoaded', () => {
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav');

  // Получаем реальные URL из скрытых ссылок в HTML, чтобы избежать проблем с шаблонами Django в JS
  const saleUrlElem = document.getElementById('url-sale');
  const rentUrlElem = document.getElementById('url-rent');
  const saleUrl = saleUrlElem ? saleUrlElem.href : '#';
  const rentUrl = rentUrlElem ? rentUrlElem.href : '#';

  // Добавляем доп. ссылку «Все объекты» если нужно
  function addAllObjectsMenu() {
    // Продажа
    const saleDropdownMenu = document.querySelector('.sale-dropdown > .dropdown-menu');
    if (saleDropdownMenu && !saleDropdownMenu.querySelector('.all-properties')) {
      const li = document.createElement('li');
      li.classList.add('all-properties');
      li.innerHTML = `<a href="${saleUrl}"><i class="fa-solid fa-house"></i> Все объекты</a>`;
      saleDropdownMenu.appendChild(li);
    }
    // Аренда
    const rentDropdownMenu = document.querySelector('.rent-dropdown > .dropdown-menu');
    if (rentDropdownMenu && !rentDropdownMenu.querySelector('.all-properties')) {
      const li = document.createElement('li');
      li.classList.add('all-properties');
      li.innerHTML = `<a href="${rentUrl}"><i class="fa-solid fa-key"></i> Все объекты</a>`;
      rentDropdownMenu.appendChild(li);
    }
  }

  function disableMainLinkOnMobile() {
    // Ссылки "Продажа" и "Аренда"
    const saleLink = document.querySelector('.sale-dropdown > a');
    const rentLink = document.querySelector('.rent-dropdown > a');

    function clickHandler(e) {
      if (window.innerWidth <= 767) {
        // Отменяем переход по ссылке на мобильных
        e.preventDefault();
        // Здесь можно дополнительно показать/спрятать подменю, если нужно
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

  // Переключение меню по клику на бургер
  burger.addEventListener('click', (e) => {
    e.stopPropagation();
    const expanded = burger.getAttribute('aria-expanded') === 'true';
    burger.setAttribute('aria-expanded', !expanded);
    nav.classList.toggle('active');
    nav.setAttribute('aria-hidden', expanded);
  });

  // Инициализация при загрузке и при изменении размера экрана
  function init() {
    addAllObjectsMenu();
    disableMainLinkOnMobile();
  }

  init();

  window.addEventListener('resize', () => {
    init();
  });
});
