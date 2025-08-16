from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import consultation_view

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('sale', views.sale, name='sale'),
    path('rent', views.rent, name='rent'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('consultation/', consultation_view, name='consultation_form'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
