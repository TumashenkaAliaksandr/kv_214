from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import consultation_view, send_consultation_message

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),

    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('sale', views.sale, name='sale'),
    path('property/<slug:slug>/', views.property_detail, name='property_detail'),
    path('rent', views.rent, name='rent'),
    path('rent/<slug:slug>/', views.rent_single, name='rent_single'),
    path('sale/<slug:slug>/', views.sale_single, name='sale_single'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('consultation/', consultation_view, name='consultation_form'),
    path('send-consultation-message/', send_consultation_message, name='send_consultation_message'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
