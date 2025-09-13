document.getElementById('reviewForm').addEventListener('submit', function(e){
    e.preventDefault();
    const formData = new FormData(this);

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(() => alert('Ошибка при отправке формы'));
});