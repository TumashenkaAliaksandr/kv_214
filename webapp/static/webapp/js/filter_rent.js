document.addEventListener("DOMContentLoaded", function() {
  const input = document.getElementById("city-autocomplete");
  const listContainer = document.getElementById("autocomplete-list");

  input.addEventListener("input", function() {
    const value = this.value.trim();
    listContainer.innerHTML = '';
    if (!value) return;

    // AJAX запрос к серверу для получения совпадений
    fetch(`/autocomplete/?q=${encodeURIComponent(value)}`)
      .then(response => response.json())
      .then(data => {
        // data — массив строк с подходящими названиями населенных пунктов
        data.forEach(city => {
          const div = document.createElement("div");
          div.textContent = city;
          div.classList.add("autocomplete-item");
          div.addEventListener("click", function() {
            input.value = city;
            listContainer.innerHTML = '';
          });
          listContainer.appendChild(div);
        });
      });
  });

  document.addEventListener("click", function(e) {
    if (e.target !== input) {
      listContainer.innerHTML = '';
    }
  });
});
