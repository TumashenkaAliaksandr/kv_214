from django.contrib import admin, messages
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.urls import path
from django.core.cache import cache, caches
from django.urls import reverse

from .forms import ObjectForm
from .models import (
    Contact, SocialNetwork, PropertyPhoto, Property, PropertyVideo, MainSliderPhoto,
    MainSlider, TrustStats, TrustReason, About, Messengers, Employee, Review, City
)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo_preview')
    readonly_fields = ('photo_preview',)
    prepopulated_fields = {'slug': ('name',)}


class PropertyPhotoInline(admin.TabularInline):
    model = PropertyPhoto
    extra = 3


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    form = ObjectForm
    list_display = ['name', 'address', 'city_name', 'price', 'area', 'area_ga', 'map_embed_html', 'date_posted', 'is_active_newstroy', 'is_active_new', 'is_active_sold']
    list_filter = ['is_active_newstroy', 'is_active_new', 'is_active_sold', 'date_posted']
    search_fields = ['name', 'address', 'description']
    inlines = [PropertyPhotoInline]
    filter_horizontal = ['contacts']


class SocialNetworkInline(admin.TabularInline):
    model = SocialNetwork
    extra = 1


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'phone_two', 'email')
    inlines = [SocialNetworkInline]


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'contact', 'is_had')
    search_fields = ('name', 'contact__name')


@admin.register(Messengers)
class MessengersAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'is_had', 'preview_icon')
    list_filter = ('is_had', )
    search_fields = ('name',)

    def preview_icon(self, obj):
        if obj.icon_svg:
            return format_html('<img src="{}" style="height:24px; width:auto;" />', obj.icon_svg.url)
        return "-"
    preview_icon.short_description = 'Иконка'


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'unp', 'license')
    search_fields = ('name',)


@admin.register(PropertyVideo)
class PropertyVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_address', 'date', 'video_url')
    list_filter = ('date',)
    search_fields = ('title', 'property_address', 'description')
    ordering = ('-date',)
    readonly_fields = ('date',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'property_address', 'video_url')
        }),
        ('Дополнительно', {
            'fields': ('date',),
            'classes': ('collapse',),
        }),
    )


class MainSliderPhotoInline(admin.TabularInline):
    model = MainSliderPhoto
    extra = 1


@admin.register(MainSlider)
class MainSliderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [MainSliderPhotoInline]


@admin.register(MainSliderPhoto)
class MainSliderPhotoAdmin(admin.ModelAdmin):
    list_display = ('name_photo', 'desc_text')


@admin.register(TrustReason)
class TrustReasonAdmin(admin.ModelAdmin):
    list_display = ('text', 'icon_class', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(TrustStats)
class TrustStatsAdmin(admin.ModelAdmin):
    list_display = ('sold_objects', 'avg_sale_days', 'support_247')

    def has_add_permission(self, request):
        return not TrustStats.objects.exists()


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'agency_name', 'phone', 'rating', 'reviews_count')
    list_filter = ('position', 'agency_name')
    search_fields = ('full_name', 'position', 'agency_name', 'regions', 'specialties')
    prepopulated_fields = {'slug': ('full_name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('full_name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('name', 'text')



class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('cache/', self.admin_view(self.cache_management_view), name='cache-management'),
            path('cache/clear-cache/', self.admin_view(self.clear_cache_view), name='cache-clear'),
        ]
        return custom_urls + urls

    def get_cache_info(self):
        """Получить информацию о кэше для отображения"""
        cache_backend = caches['default']  # используемый кэш (по умолчанию)
        try:
            # Пример для memcached и некоторых других: нельзя получить ключи, но можно пофантазировать
            if hasattr(cache_backend, 'get_stats'):
                stats = cache_backend.get_stats()
                if stats:
                    return f"Статус кэша: {stats}"
            # Для локального кэша можно хранить количество ключей в самом коде (если нужно)
            return "Кэш интерфейс не поддерживает подробную статистику."
        except Exception:
            return "Информация о кэше недоступна."

    def cache_management_view(self, request):
        cache_info = request.session.pop('cache_info', None)
        if not cache_info:
            cache_info = self.get_cache_info()

        context = {
            **self.each_context(request),
            'cache_info': cache_info,
        }
        return TemplateResponse(request, 'admin/cache_admin.html', context)

    def clear_cache_view(self, request):
        if request.method == 'POST':
            cache_backend = caches['default']
            try:
                # Можно перед очисткой сохранить состояние или количество
                cache_info_before = self.get_cache_info()
                cache_backend.clear()
                request.session['cache_info'] = f"Кэш успешно очищен. До очистки: {cache_info_before}"
                messages.success(request, "Кэш успешно очищен")
            except Exception:
                request.session['cache_info'] = "Кэш очищен, но информация о состоянии недоступна."
                messages.error(request, "Ошибка при очистке кэша, подробности в логах.")
        return HttpResponseRedirect(reverse('admin:cache-management'))

# Экземпляр кастомного админ-сайта
custom_admin_site = CustomAdminSite()

# Регистрируем модели в кастомном сайте
custom_admin_site.register(City, CityAdmin)
custom_admin_site.register(Property, PropertyAdmin)
custom_admin_site.register(Contact, ContactAdmin)
custom_admin_site.register(SocialNetwork, SocialNetworkAdmin)
custom_admin_site.register(Messengers, MessengersAdmin)
custom_admin_site.register(About, AboutAdmin)
custom_admin_site.register(PropertyVideo, PropertyVideoAdmin)
custom_admin_site.register(MainSlider, MainSliderAdmin)
custom_admin_site.register(MainSliderPhoto, MainSliderPhotoAdmin)
custom_admin_site.register(TrustReason, TrustReasonAdmin)
custom_admin_site.register(TrustStats, TrustStatsAdmin)
custom_admin_site.register(Employee, EmployeeAdmin)
custom_admin_site.register(Review, ReviewAdmin)
