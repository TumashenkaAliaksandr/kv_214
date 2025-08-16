from django.shortcuts import render, redirect, get_object_or_404

from webapp.models import Property
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    """this main page"""
    properties_new = Property.objects.filter(is_active_new=True).prefetch_related('photos')
    properties_all = Property.objects.prefetch_related('photos').all()
    return render(request, 'webapp/index.html', {'properties_new': properties_new, 'properties_all': properties_all})


def about(request):
    """about page"""

    return render(request, 'webapp/about.html')


def rent(request):
    """rent page"""

    return render(request, 'webapp/rent_page.html')


def sale(request):
    properties = Property.objects.all()

    # Фильтрация по типу недвижимости
    property_types = request.GET.getlist('property_type')
    if property_types:
        filter_args = {ptype: True for ptype in property_types if hasattr(Property, ptype)}
        if filter_args:
            properties = properties.filter(**filter_args)

    # Фильтрация по городу (по любому совпадению в адресе)
    direction = request.GET.get('direction', '').strip()
    if direction:
        properties = properties.filter(address__icontains=direction)

    # Фильтрация по цене
    price_min = request.GET.get('price_min')
    if price_min:
        try:
            price_min = float(price_min)
            properties = properties.filter(price__gte=price_min)
        except ValueError:
            pass

    price_max = request.GET.get('price_max')
    if price_max:
        try:
            price_max = float(price_max)
            properties = properties.filter(price__lte=price_max)
        except ValueError:
            pass

    context = {
        'properties': properties,
    }
    return render(request, 'webapp/sale_page.html', context)

def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug)
    return render(request, 'webapp/sale_page.html', {'property': property})

def autocomplete(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        qs = Property.objects.filter(address__icontains=query).values_list('address', flat=True).distinct()
        cities = set()
        for addr in qs:
            city = addr.split(',')[0].strip()
            if city.lower().startswith(query.lower()):
                cities.add(city)
        results = list(cities)[:10]
    return JsonResponse(results, safe=False)

def contacts(request):
    """contacts page"""

    return render(request, 'webapp/contacts.html')

def consultation_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        agree = request.POST.get('agree')

        if not (name and phone and agree):
            return JsonResponse({'success': False, 'message': 'Пожалуйста, заполните все поля и согласитесь с обработкой данных.'})

        message = f"<b>Новая заявка на консультацию</b>\nИмя: {name}\nТелефон: {phone}"

        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID
        telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
        }

        try:
            response = requests.post(telegram_api_url, data=data)
            if response.status_code == 200:
                return JsonResponse({'success': True, 'message': 'Спасибо! Ваш запрос отправлен.'})
            else:
                error_msg = response.json().get('description', 'Ошибка при отправке в Telegram.')
                return JsonResponse({'success': False, 'message': error_msg})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Ошибка сервера: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Некорректный запрос.'})
