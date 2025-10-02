document.addEventListener("DOMContentLoaded", function () {
    const burger = document.querySelector('.filter-burger');
    const filterPages = document.querySelector('.filter-pages');

    burger.addEventListener('click', function () {
        filterPages.classList.toggle('active');
        burger.classList.toggle('active');  // переключаем иконки

        if (filterPages.classList.contains('active')) {
            burger.setAttribute('aria-label', 'Закрыть фильтр');
        } else {
            burger.setAttribute('aria-label', 'Открыть фильтр');
        }
    });

    // Автозаполнение для поля города
    const input = document.getElementById("city-autocomplete");
    const listContainer = document.getElementById("autocomplete-list");

    const cities = JSON.parse('{{ cities|escapejs }}');

    input.addEventListener("input", function () {
        const value = this.value.trim().toLowerCase();
        listContainer.innerHTML = '';
        if (!value) return;

        cities.forEach(city => {
            if (city.toLowerCase().startsWith(value)) {
                const div = document.createElement("div");
                div.textContent = city;
                div.classList.add("autocomplete-item");
                div.addEventListener("click", function () {
                    input.value = city;
                    listContainer.innerHTML = '';
                });
                listContainer.appendChild(div);
            }
        });
    });

    document.addEventListener("click", function (e) {
        if (e.target !== input) {
            listContainer.innerHTML = '';
        }
    });
});
