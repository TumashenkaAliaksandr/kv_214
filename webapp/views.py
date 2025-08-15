from django.shortcuts import render, redirect

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
