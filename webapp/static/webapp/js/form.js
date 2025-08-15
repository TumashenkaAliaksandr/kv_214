document.getElementById('consultationForm').addEventListener('submit', function(event) {
  event.preventDefault(); // Останавливаем стандартную отправку формы

  const form = event.target;
  const formData = new FormData(form);

  fetch("{% url 'consultation_form' %}", {
    method: 'POST',
    headers: {
      'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
    },
    body: formData,
  })
  .then(response => response.json())
  .then(data => {
    const messageDiv = document.getElementById('formMessage');
    if (data.success) {
      messageDiv.style.color = 'green';
      messageDiv.textContent = data.message;
      form.reset();
    } else {
      messageDiv.style.color = 'red';
      messageDiv.textContent = data.message;
    }
  })
  .catch(error => {
    const messageDiv = document.getElementById('formMessage');
    messageDiv.style.color = 'red';
    messageDiv.textContent = 'Ошибка при отправке. Попробуйте позже.';
    console.error('Error:', error);
  });
});
