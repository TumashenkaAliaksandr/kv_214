from django.shortcuts import render

from webapp.models import Property


def index(request):
    """this main page"""
    properties_new = Property.objects.filter(is_active_new=True).prefetch_related('photos')
    properties_all = Property.objects.prefetch_related('photos').all()
    return render(request, 'webapp/index.html', {'properties_new': properties_new, 'properties_all': properties_all})


