from django.shortcuts import render, redirect, get_object_or_404

from webapp.models import Property
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    # Начинаем с всех объектов
    properties = Property.objects.all()

    # Фильтрация по типам (булевым полям)
    property_types = request.GET.getlist('property_type')
    if property_types:
        filter_args = {}
        for ptype in property_types:
            model_fields = [f.name for f in Property._meta.get_fields()]
            if ptype in model_fields:
                filter_args[ptype] = True
        if filter_args:
            properties = properties.filter(**filter_args)

    # Фильтрация по городу/направлению (вхождение в поле address)
    direction = request.GET.get('direction', '').strip()
    if direction:
        properties = properties.filter(address__icontains=direction)

    # Фильтрация по цене
    price_min = request.GET.get('price_min')
    if price_min:
        try:
            price_min = float(price_min)
            properties = properties.filter(price__gte=price_min)
        except (ValueError, TypeError):
            pass

    price_max = request.GET.get('price_max')
    if price_max:
        try:
            price_max = float(price_max)
            properties = properties.filter(price__lte=price_max)
        except (ValueError, TypeError):
            pass

    # Фильтрация по валюте (учитывая большие буквы как в модели)
    currency = request.GET.get('currency')
    if currency:
        valid_currencies = dict(Property.CURRENCY_CHOICES).keys()
        if currency.upper() in valid_currencies:
            properties = properties.filter(currency=currency.upper())

    # Для автодополнения городов, сформируем список уникальных городов из адресов
    addresses = Property.objects.values_list('address', flat=True).distinct()
    cities_set = set()
    for addr in addresses:
        if addr and "," in addr:
            city = addr.split(",")[0].strip()
        else:
            city = addr
        cities_set.add(city)
    cities = sorted(cities_set)

    context = {
        'properties_new': Property.objects.filter(is_active_new=True).prefetch_related('photos'),
        'properties_all': properties.prefetch_related('photos'),
        'cities': cities,
    }
    return render(request, 'webapp/index.html', context)


def about(request):
    """about page"""

    return render(request, 'webapp/about.html')

def rent(request):
    properties = Property.objects.filter(is_rent=True)  # добавляем фильтр по аренде

    property_types = request.GET.getlist('property_type')
    if property_types:
        filter_args = {}
        for ptype in property_types:
            if ptype in [f.name for f in Property._meta.get_fields()]:
                filter_args[ptype] = True
        if filter_args:
            properties = properties.filter(**filter_args)

    direction = request.GET.get('direction', '').strip()
    if direction:
        properties = properties.filter(address__icontains=direction)

    price_min = request.GET.get('price_min')
    if price_min:
        try:
            price_min = float(price_min)
            properties = properties.filter(price__gte=price_min)
        except (ValueError, TypeError):
            pass

    price_max = request.GET.get('price_max')
    if price_max:
        try:
            price_max = float(price_max)
            properties = properties.filter(price__lte=price_max)
        except (ValueError, TypeError):
            pass

    currency = request.GET.get('currency')
    if currency in dict(Property.CURRENCY_CHOICES).keys():
        properties = properties.filter(currency=currency.upper())

    context = {
        'properties': properties,
    }
    return render(request, 'webapp/rent_page.html', context)

def sale_single(request, slug):
    property = get_object_or_404(Property, slug=slug, is_sale=True)
    photos = property.photos.all()
    return render(request, 'webapp/sale_single.html', {
        'property': property,
        'photos': photos,
    })

def rent_single(request, slug):
    property = get_object_or_404(Property, slug=slug, is_rent=True)
    photos = property.photos.all()
    return render(request, 'webapp/rent_single.html', {
        'property': property,
        'photos': photos,
    })


def sale(request):
    properties = Property.objects.filter(is_sale=True)  # добавляем фильтр по продаже

    property_types = request.GET.getlist('property_type')
    if property_types:
        filter_args = {}
        for ptype in property_types:
            if ptype in [f.name for f in Property._meta.get_fields()]:
                filter_args[ptype] = True
        if filter_args:
            properties = properties.filter(**filter_args)

    direction = request.GET.get('direction', '').strip()
    if direction:
        properties = properties.filter(address__icontains=direction)

    price_min = request.GET.get('price_min')
    if price_min:
        try:
            price_min = float(price_min)
            properties = properties.filter(price__gte=price_min)
        except (ValueError, TypeError):
            pass

    price_max = request.GET.get('price_max')
    if price_max:
        try:
            price_max = float(price_max)
            properties = properties.filter(price__lte=price_max)
        except (ValueError, TypeError):
            pass

    currency = request.GET.get('currency')
    if currency in dict(Property.CURRENCY_CHOICES).keys():
        properties = properties.filter(currency=currency.upper())

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
