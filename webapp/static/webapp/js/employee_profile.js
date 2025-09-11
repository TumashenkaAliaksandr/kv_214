document.addEventListener('DOMContentLoaded', () => {
    const phoneBtn = document.querySelector('.show-phone-btn');
    const phoneNumber = document.getElementById('phone-number');

    phoneBtn.addEventListener('click', () => {
        const isShown = phoneNumber.classList.toggle('show');
        phoneBtn.textContent = isShown ? 'Скрыть телефон' : 'Показать телефон';
        phoneBtn.setAttribute('aria-expanded', isShown);
    });
});
