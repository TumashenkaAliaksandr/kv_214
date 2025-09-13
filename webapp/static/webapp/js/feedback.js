document.addEventListener('DOMContentLoaded', () => {
    const openBtn = document.getElementById('openReviewBtn');
    const modal = document.getElementById('reviewModal');
    const closeBtn = document.getElementById('closeReviewBtn');
    const reviewForm = document.getElementById('reviewForm');

    // Функция открыть модалку
    function openModal() {
        modal.style.display = 'block';
        modal.setAttribute('aria-hidden', 'false');
        // Фокус на первое поле формы (например, имя)
        reviewForm.reviewerName.focus();
    }

    // Функция закрыть модалку
    function closeModal() {
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
        // Вернуть фокус обратно на кнопку открывания
        openBtn.focus();
    }

    // Открыть по кнопке
    openBtn.addEventListener('click', openModal);

    // Закрыть по кнопке
    closeBtn.addEventListener('click', closeModal);

    // Закрыть по клику вне формы
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });

    // Обработка отправки формы
    reviewForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Здесь можно добавить отправку формы, например через fetch, ajax и т.п.
        alert('Спасибо за отзыв, ' + reviewForm.reviewerName.value + '!');

        // Закрыть модалку и очистить форму
        closeModal();
        reviewForm.reset();
    });

    // Закрывать модалку по Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === "Escape" && modal.style.display === 'block') {
            closeModal();
        }
    });
});