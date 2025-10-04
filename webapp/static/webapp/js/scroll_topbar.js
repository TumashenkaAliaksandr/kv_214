const scrollTopBtn = document.getElementById('scrollTopBtn');

window.onscroll = function() {
    if (window.scrollY > 300) { // Показывать кнопку, если прокручено вниз больше 300px
        scrollTopBtn.style.display = "block";
    } else {
        scrollTopBtn.style.display = "none";
    }
};

scrollTopBtn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' }); // Плавный скролл наверх
});
