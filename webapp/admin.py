from django.contrib import admin
from .models import Contact, SocialNetwork, PropertyPhoto, Property, PropertyVideo


class PropertyPhotoInline(admin.TabularInline):
    model = PropertyPhoto
    extra = 3  # кол-во дополнительных форм для загрузки фото

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'price', 'area', 'area_ga', 'date_posted', 'is_active_new', 'is_active_sold']
    list_filter = ['is_active_new', 'is_active_sold', 'date_posted']
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
    list_display = ('name', 'url', 'contact')
    search_fields = ('name', 'contact__name')

from django.contrib import admin
from .models import PropertyVideo

@admin.register(PropertyVideo)
class PropertyVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_address', 'date', 'video_url')  # колонки в списке
    list_filter = ('date',)                 # фильтр по дате
    search_fields = ('title', 'property_address', 'description')  # поиск по этим полям
    ordering = ('-date',)                   # сортировка по дате (новые сверху)
    readonly_fields = ('date',)             # дату редактировать нельзя

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'property_address', 'video_url')
        }),
        ('Дополнительно', {
            'fields': ('date',),
            'classes': ('collapse',),  # скрываем блок
        }),
    )
