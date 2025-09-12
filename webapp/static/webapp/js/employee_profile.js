document.addEventListener('DOMContentLoaded', () => {
    const phoneBtn = document.querySelector('.show-phone-btn');
    const phoneNumber = document.getElementById('phone-number');
    let hideTimeout;

    // Изначально скрываем телефон, показываем кнопку "Показать телефон"
    phoneNumber.style.display = 'none';
    phoneBtn.textContent = 'Показать телефон';
    phoneBtn.setAttribute('aria-expanded', 'false');

    // Функция скрытия телефона и сброса кнопки
    function hidePhone() {
        phoneNumber.style.display = 'none';
        phoneBtn.textContent = 'Показать телефон';
        phoneBtn.setAttribute('aria-expanded', 'false');
    }

    // Функция показа телефона и запуска таймера на автоматическое скрытие
    function showPhone() {
        phoneNumber.style.display = 'inline'; // или 'block', в зависимости от стилей
        phoneBtn.textContent = 'Скрыть телефон';
        phoneBtn.setAttribute('aria-expanded', 'true');

        // Очистить предыдущий таймер, если есть
        if (hideTimeout) clearTimeout(hideTimeout);

        // Запускаем таймер скрытия через 10 секунд, если не наведение
        hideTimeout = setTimeout(() => {
            // Если мышь не наведена на телефон
            if (!phoneNumber.matches(':hover')) {
                hidePhone();
            }
        }, 10000);
    }

    // Обработчик клика по кнопке
    phoneBtn.addEventListener('click', () => {
        if (phoneNumber.style.display === 'none') {
            showPhone();
        } else {
            // Скрываем телефон и очищаем таймер
            hidePhone();
            if (hideTimeout) clearTimeout(hideTimeout);
        }
    });

    // При наведении на телефон отменяем скрытие
    phoneNumber.addEventListener('mouseenter', () => {
        if (hideTimeout) clearTimeout(hideTimeout);
    });

    // При уходе мыши с телефона снова запускаем таймер скрытия
    phoneNumber.addEventListener('mouseleave', () => {
        hideTimeout = setTimeout(() => {
            hidePhone();
        }, 10000);
    });
});
