from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import consultation_view, send_consultation_message, RobotsTxtView, city_detail

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('cities/', views.city_list, name='city_list'),
    path('city/<slug:slug>/', city_detail, name='city_detail'),

    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('sale/', views.sale, name='sale'),
    path('property/<slug:slug>/', views.property_detail, name='property_detail'),
    path('rent/', views.rent, name='rent'),
    path('rent/<slug:slug>/', views.rent_single, name='rent_single'),
    path('sale/<slug:slug>/', views.sale_single, name='sale_single'),
    path('about/', views.about, name='about'),
    path('employees/', views.employees, name='employees'),
    path('employees_single/<slug:slug>/', views.employees_single, name='employees_single'),
    path('contacts/', views.contacts, name='contacts'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('consultation/', consultation_view, name='consultation_form'),
    path('send-consultation-message/', send_consultation_message, name='send_consultation_message'),
    path("robots.txt", RobotsTxtView.as_view(), name="robots_txt"),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
