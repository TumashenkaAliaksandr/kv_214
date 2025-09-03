from .models import Contact

def contact_data(request):
    contact = Contact.objects.prefetch_related('social_networks').first()
    if contact:
        social_networks = contact.social_networks.filter(is_had=True)
    else:
        social_networks = []
    return {
        'contact': contact,
        'social_networks': social_networks,
    }
