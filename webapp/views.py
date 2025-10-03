import json

from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from kv_214 import settings
from kv_214.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from webapp.models import Property, MainSlider, PropertyVideo, TrustStats, TrustReason, About, Employee, Review, City
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import logging


def index(request):
    # Начинаем с всех объектов
    properties = Property.objects.all()
    about = About.objects.first()
    sliders = MainSlider.objects.prefetch_related('photos').all()
    videos = PropertyVideo.objects.all()
    trust_stats = TrustStats.objects.first()
    trust_reasons = TrustReason.objects.all()
    reviews = Review.objects.all()[:20]

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
        'trust_reasons': trust_reasons,
        'properties_new': Property.objects.filter(is_active_new=True).prefetch_related('photos'),
        'properties_all': properties.prefetch_related('photos'),
        'cities': cities,
        'sliders': sliders,
        'videos': videos,
        'about': about,
        'sold_objects': trust_stats.sold_objects if trust_stats else 1000,
        'avg_sale_days': trust_stats.avg_sale_days if trust_stats else 21,
        'support_247': trust_stats.support_247 if trust_stats else "24",
        'reviews': reviews,
    }
    return render(request, 'webapp/index.html', context)


def about(request):
    """about page"""
    about = About.objects.first()
    properties = Property.objects.all()
    trust_stats = TrustStats.objects.first()
    trust_reasons = TrustReason.objects.all()
    all_employees = Employee.objects.all()


    context = {
        'about': about,
        'sold_objects': trust_stats.sold_objects if trust_stats else 1000,
        'avg_sale_days': trust_stats.avg_sale_days if trust_stats else 21,
        'support_247': trust_stats.support_247 if trust_stats else "24",
        'properties_new': Property.objects.filter(is_active_new=True).prefetch_related('photos'),
        'properties_all': properties.prefetch_related('photos'),
        'trust_reasons': trust_reasons,
        'employees': all_employees,
    }

    return render(request, 'webapp/about.html', context)



def employees(request):
    """Страница со списком сотрудников"""
    all_employees = Employee.objects.all()
    context = {'employees': all_employees}
    return render(request, 'webapp/employees.html', context)

def employees_single(request, slug):
    """Детальная страница сотрудника"""
    employee = get_object_or_404(Employee, slug=slug)
    context = {'employee': employee}
    return render(request, 'webapp/single_employees.html', context)


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
    # Начинаем с фильтра по продаже
    properties = Property.objects.filter(is_sale=True)

    has_filters = False  # флаг наличия фильтров

    # Фильтрация по булевым типам из GET параметров
    property_types = request.GET.getlist('property_type')
    if property_types:
        has_filters = True
        filter_args = {}
        valid_fields = [f.name for f in Property._meta.get_fields() if f.get_internal_type() == 'BooleanField']
        for ptype in property_types:
            if ptype in valid_fields:
                filter_args[ptype] = True
        if filter_args:
            properties = properties.filter(**filter_args)

    # Фильтр по адресу
    direction = request.GET.get('direction', '').strip()
    if direction:
        has_filters = True
        properties = properties.filter(address__icontains=direction)

    # Фильтрация по минимальной цене
    price_min = request.GET.get('price_min')
    if price_min:
        has_filters = True
        try:
            price_min_val = float(price_min)
            properties = properties.filter(price__gte=price_min_val)
        except (ValueError, TypeError):
            pass

    # Фильтрация по максимальной цене
    price_max = request.GET.get('price_max')
    if price_max:
        has_filters = True
        try:
            price_max_val = float(price_max)
            properties = properties.filter(price__lte=price_max_val)
        except (ValueError, TypeError):
            pass

    # Фильтрация по валюте
    currency = request.GET.get('currency')
    if currency and currency.upper() in dict(Property.CURRENCY_CHOICES).keys():
        has_filters = True
        properties = properties.filter(currency=currency.upper())

    # Сортируем properties по pk, чтобы избежать ошибок в пагинации
    properties = properties.order_by('pk')

    # Пагинация
    paginator = Paginator(properties, 12)  # 10 объектов на страницу
    page = request.GET.get('page', 1)

    try:
        properties_page = paginator.page(page)
    except PageNotAnInteger:
        properties_page = paginator.page(1)
    except EmptyPage:
        properties_page = paginator.page(paginator.num_pages)

    # Получаем первый объект из всего queryset (отсортированного)
    first_property = properties.first()

    # Формируем GET-параметры без page для пагинации с фильтрами
    get_params = request.GET.copy()
    if 'page' in get_params:
        del get_params['page']
    query_string = get_params.urlencode()

    context = {
        'properties': properties_page,
        'first_property': first_property,
        'has_filters': has_filters,
        'paginator': paginator,
        'page_obj': properties_page,
        'query_string': query_string,
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

    about = About.objects.first()

    context = {
        'about': about,
    }

    return render(request, 'webapp/contacts.html', context=context)

def consultation_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        agree = request.POST.get('agree')

        if not (name and phone and agree):
            return JsonResponse({'success': False, 'message': '⚠️ Пожалуйста, заполните все поля и согласитесь с обработкой данных.'})

        message = f"<b>💬 Новая заявка на консультацию</b>\n\n🧑🏻 Имя: {name}\n📞 Телефон: {phone}"

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
                return JsonResponse({'success': True, 'message': '🤝 Спасибо! Ваш запрос отправлен.'})
            else:
                error_msg = response.json().get('description', '⚠️ Ошибка при отправке в Telegram.')
                return JsonResponse({'success': False, 'message': error_msg})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'⚠️ Ошибка сервера: {str(e)}'})

    return JsonResponse({'success': False, 'message': '⚠️ Некорректный запрос.'})


logger = logging.getLogger(__name__)

@csrf_protect
def send_consultation_message(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '⛔ Метод не разрешён'}, status=405)

    name = request.POST.get('name')
    phone = request.POST.get('phone')
    description = request.POST.get('description', '⚠️ Нет описания')

    if not name or not phone:
        return JsonResponse({'success': False, 'message': '⚠️ Пожалуйста, заполните обязательные поля: имя и телефон.'}, status=400)

    message = (
        f"<b>✔️ Новая заявка на консультацию</b>\n\n"
        f"<b>🧑🏻 Имя:</b> {name}\n"
        f"<b>📞 Телефон:</b> {phone}\n"
        f"<b>📝 Описание:</b> {description}"
    )

    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML',
    }

    try:
        response = requests.post(telegram_api_url, data=payload, timeout=10)
        if response.status_code == 200:
            return JsonResponse({'success': True, 'message': '🤝 Спасибо! Ваш запрос отправлен.'}, json_dumps_params={'ensure_ascii': False})
        else:
            error_desc = response.json().get('description', '⚠️ Ошибка при отправке в Telegram.')
            logger.error(f'Telegram API error: {error_desc}')
            return JsonResponse({'success': False, 'message': error_desc}, status=500)
    except Exception as e:
        logger.exception('⚠️ Ошибка при отправке сообщения в Telegram')
        return JsonResponse({'success': False, 'message': f'⚠️ Ошибка сервера: {str(e)}'}, status=500)


class RobotsTxtView(TemplateView):
    template_name = "robots.txt"
    content_type = "text/plain"

    def get_context_data(self, **kwargs):
        domain = self.request.scheme + "://" + self.request.get_host()
        sitemap_url = domain + "/sitemap.xml"
        return {'sitemap_url': sitemap_url}


logger = logging.getLogger(__name__)

@require_POST
def submit_review(request):
    name = request.POST.get('reviewerName')
    rating = request.POST.get('reviewRating')
    text = request.POST.get('reviewText')

    # Проверяем обязательные поля
    if not name or not rating or not text:
        return JsonResponse(
            {'success': False, 'message': '⚠️ Пожалуйста, заполните имя, оценку и текст отзыва'},
            status=400
        )

    # Проверяем корректность рейтинга (1-5)
    try:
        rating_value = int(rating)
        if rating_value < 1 or rating_value > 5:
            raise ValueError("⚠️ Некорректная оценка")
    except Exception:
        return JsonResponse({'success': False, 'message': '⚠️ Оценка должна быть числом от 1 до 5'}, status=400)

    # Формируем письмо
    subject = '✔️ Новый отзыв на сайте'
    message = f'🙎🏻‍♂️ Имя: {name}\n\n⭐ Оценка: {rating_value}\n\n📝 Отзыв:\n{text}'
    recipient_list = ['Badminton500@inbox.lv']  # Замените на нужный email

    # Отправляем email
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            fail_silently=False,
        )
        logger.info(f'✔️ Email отправлено от {settings.EMAIL_HOST_USER} о отзыве от {name}')
    except Exception as e:
        logger.error(f'⛔ Ошибка отправки email: {e}')
        return JsonResponse({'success': False, 'message': f'⛔ Ошибка при отправке email: {str(e)}'}, status=500)

    # Отправляем в Telegram
    telegram_api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    telegram_message = (
        f"<b>🐸 Новый отзыв с сайта</b>\n\n\n"
        f"<b>🙎🏻‍♂️ Имя:</b> {name}\n\n"
        f"<b>⭐ Оценка:</b> {rating_value}\n\n"
        f"<b>📝 Отзыв:</b> {text}"
    )
    payload = {
        'chat_id': settings.TELEGRAM_CHAT_ID,
        'text': telegram_message,
        'parse_mode': 'HTML',
    }

    try:
        response = requests.post(telegram_api_url, data=payload, timeout=10)
        logger.info(f'✔️ Ответ Telegram: {response.text}')
        if response.status_code != 200:
            desc = response.json().get('description', '⚠️error⚠️ Ошибка при отправке сообщения в Telegram.')
            return JsonResponse({'success': False, 'message': desc}, status=500)
    except Exception as e:
        logger.error(f'⚠️error⚠️ Ошибка подключения к Telegram: {e}')
        return JsonResponse({'success': False, 'message': f'⚠️error⚠️ Ошибка соединения с Telegram: {str(e)}'}, status=500)

    return JsonResponse({'success': True, 'message': '🐸 Спасибо, отзыв появиться когда пройдет модерацию!'}, json_dumps_params={'ensure_ascii': False})


def city_list(request):
    cities = City.objects.annotate(property_count=Count('properties'))

    return render(request, 'webapp/category_objects.html', {'cities': cities})


def city_detail(request, slug):
    city = get_object_or_404(City, slug=slug)
    properties = city.properties.all()
    return render(request, 'webapp/category_objects.html', {'city': city, 'properties': properties})
