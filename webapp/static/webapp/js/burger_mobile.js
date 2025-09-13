document.addEventListener('DOMContentLoaded', () => {
  const MOBILE_BREAKPOINT = 767;
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('#navMenu') || document.querySelector('.nav');
  const saleUrl = document.getElementById('url-sale')?.getAttribute('href') || '#';
  const rentUrl = document.getElementById('url-rent')?.getAttribute('href') || '#';

  function removeAllObjectsItems() {
    document.querySelectorAll('.all-properties').forEach(el => el.remove());
  }

  function addAllObjectsMenu() {
    removeAllObjectsItems();
    if (window.innerWidth > MOBILE_BREAKPOINT) return;
    const maps = [
      { parentSelector: '.sale-dropdown', menuSelector: '.sale-dropdown .dropdown-menu', url: saleUrl, icon: 'fa-house' },
      { parentSelector: '.rent-dropdown', menuSelector: '.rent-dropdown .dropdown-menu', url: rentUrl, icon: 'fa-key' }
    ];
    maps.forEach(({ parentSelector, menuSelector, url, icon }) => {
      const parent = document.querySelector(parentSelector);
      const menu = document.querySelector(menuSelector);
      if (!menu || !url || !parent) return;
      if (!menu.querySelector('.all-properties')) {
        const li = document.createElement('li');
        li.className = 'all-properties';
        li.innerHTML = `<a href="${url}"><i class="fa-solid ${icon}"></i> Все объекты</a>`;
        const firstItem = menu.querySelector('li');
        if (firstItem) menu.insertBefore(li, firstItem);
        else menu.appendChild(li);
      }
    });
  }

  function closeAllDropdowns() {
    document.querySelectorAll('.dropdown.active').forEach(drop => {
      drop.classList.remove('active');
      const a = drop.querySelector(':scope > a');
      if (a) a.setAttribute('aria-expanded', 'false');
    });
  }

  function disableMainLinkOnMobile() {
    const dropdownLinks = document.querySelectorAll('.dropdown > a[href]');

    dropdownLinks.forEach(link => {
      if (link._menuHandlerAdded) return;
      if (!link.hasAttribute('aria-expanded')) link.setAttribute('aria-expanded', 'false');

      link.addEventListener('click', (e) => {
        if (window.innerWidth > MOBILE_BREAKPOINT) {
          // На десктопе блокируем переход и раскрываем меню
          // e.preventDefault();
          // e.stopPropagation();

          const parentLi = link.parentElement;
          const wasActive = parentLi.classList.contains('active');

          document.querySelectorAll('.dropdown.active').forEach(drop => {
            if (drop !== parentLi) {
              drop.classList.remove('active');
              const otherA = drop.querySelector(':scope > a');
              if (otherA) otherA.setAttribute('aria-expanded', 'false');
            }
          });

          if (!wasActive) {
            parentLi.classList.add('active');
            link.setAttribute('aria-expanded', 'true');
          } else {
            parentLi.classList.remove('active');
            link.setAttribute('aria-expanded', 'false');
          }

        } else {
          // Мобильная версия - исключение для ссылки "О нас" (url 'about')
          if (link.getAttribute('href').includes('/about')) {
            // Разрешаем переход по ссылке без блокировки и раскрытия
            // Ничего не делаем, позволяя открыть страницу "О нас"
            return;
          }
          // Для остальных пунктов ведем себя как раньше - блокируем переход и управляеи классом active
          e.preventDefault();
          e.stopPropagation();

          const parentLi = link.parentElement;
          const wasActive = parentLi.classList.contains('active');

          document.querySelectorAll('.dropdown.active').forEach(drop => {
            if (drop !== parentLi) {
              drop.classList.remove('active');
              const otherA = drop.querySelector('> a');
              if (otherA) otherA.setAttribute('aria-expanded', 'false');
            }
          });

          if (!wasActive) {
            parentLi.classList.add('active');
            link.setAttribute('aria-expanded', 'true');
          } else {
            parentLi.classList.remove('active');
            link.setAttribute('aria-expanded', 'false');
          }
        }
      });

      link._menuHandlerAdded = true;
    });
  }

  if (burger) {
    burger.addEventListener('click', (e) => {
      e.stopPropagation();
      const expanded = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!expanded));
      burger.classList.toggle('active');
      if (nav) {
        nav.classList.toggle('active');
        nav.setAttribute('aria-hidden', String(expanded));
      }
    });
  }

  document.addEventListener('click', (e) => {
    const insideNav = e.target.closest && e.target.closest('#navMenu, .nav, .burger');
    if (!insideNav) {
      closeAllDropdowns();
      // НЕ закрываем бургер меню при кликах вне
    }
  });

  function init() {
    addAllObjectsMenu();
    disableMainLinkOnMobile();
    if (window.innerWidth > MOBILE_BREAKPOINT) {
      closeAllDropdowns();
    }
  }

  init();
  window.addEventListener('resize', init);
});
