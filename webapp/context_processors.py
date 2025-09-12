import requests

from .models import Contact

def contact_data(request):
    contact = Contact.objects.prefetch_related('social_networks', 'messengers').first()
    if contact:
        social_networks = contact.social_networks.filter(is_had=True)
        messengers = contact.messengers.filter(is_had=True)
    else:
        social_networks = []
        messengers = []
    return {
        'contact': contact,
        'social_networks': social_networks,
        'messengers': messengers,
    }

def get_usd_to_byn_rate():
    url = "https://api.nbrb.by/exrates/rates/USD?parammode=2"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['Cur_OfficialRate']
    return None

def currency_rates(request):
    rate = get_usd_to_byn_rate()
    return {
        'usd_to_byn_rate': rate
    }