from .models import Contact

def contact_data(request):
    # Получаем первый объект Contact, либо None если нет
    contact = Contact.objects.prefetch_related('social_networks').first()
    return {
        'contact': contact,
        # Соцсети можно получить через contact.social_networks.all() в шаблоне
    }
