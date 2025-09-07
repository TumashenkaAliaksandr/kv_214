document.addEventListener('DOMContentLoaded', () => {
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav');

  const saleUrlElem = document.getElementById('url-sale');
  const rentUrlElem = document.getElementById('url-rent');
  const saleUrl = saleUrlElem ? saleUrlElem.href : '#';
  const rentUrl = rentUrlElem ? rentUrlElem.href : '#';

  // Добавить пункт "Все объекты" в дропдауны на мобильных
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

  // Для мобильных запретить переход по основным ссылкам и переключать дропдауны
  function disableMainLinkOnMobile() {
    const saleLink = document.querySelector('.sale-dropdown > a');
    const rentLink = document.querySelector('.rent-dropdown > a');

    function clickHandler(e) {
      if (window.innerWidth <= 767) {
        e.preventDefault(); // Отменяем переход

        // Переключаем активность родительского li (для открытия/закрытия дропдауна)
        const parentLi = e.currentTarget.parentElement;
        parentLi.classList.toggle('active');
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

  // Обработчик клика на бургер меню — добавляет крестик, открывает меню
  burger.addEventListener('click', (e) => {
    e.stopPropagation(); // Предотвращаем всплытие события
    burger.classList.toggle('active'); // Переключаем крестик
    const expanded = burger.getAttribute('aria-expanded') === 'true';
    burger.setAttribute('aria-expanded', !expanded);
    nav.classList.toggle('active');
    nav.setAttribute('aria-hidden', expanded);
  });

  // Инициализация функций
  function init() {
    addAllObjectsMenu();
    disableMainLinkOnMobile();
  }

  init();

  // Обновление при изменении размера окна
  window.addEventListener('resize', () => {
    init();
  });
});
