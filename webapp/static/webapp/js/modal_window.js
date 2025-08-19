document.addEventListener('DOMContentLoaded', () => {
  const openBtn = document.getElementById('openConsultationBtn');
  const modal = document.getElementById('consultationModal');
  const closeBtn = document.getElementById('closeConsultationBtn');
  const form = document.getElementById('consultationFormtwo');  // Имя формы из HTML

  openBtn.addEventListener('click', () => {
    modal.style.display = 'flex';
    document.getElementById('inputName').focus();
  });

  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === "Escape" && modal.style.display === 'flex') {
      modal.style.display = 'none';
    }
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const name = form.name.value.trim();
    const phone = form.phone.value.trim();

    if (!name || !phone) {
      alert('✍️ Пожалуйста, заполните обязательные поля: имя и телефон.');
      return;
    }

    const formData = new FormData(form);

    fetch(form.action, {
      method: 'POST',
      headers: {
        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
      },
      body: formData,
    })
    .then(response => {
      if (!response.ok) throw new Error('⚠️ Ошибка сети');
      return response.json();
    })
    .then(data => {
      if (data.success) {
        alert(data.message || '🤝 Спасибо! Ваша заявка отправлена, мы свяжемся с вами в ближайшее время.');
        form.reset();
        modal.style.display = 'none';
      } else {
        alert(data.message || '⚠️ Ошибка отправки. Попробуйте ещё раз.');
      }
    })
    .catch(() => {
      alert('⚠️ Ошибка сети. Попробуйте позже.');
    });
  });
});
