from django.contrib import admin
from .models import Contact, SocialNetwork, PropertyPhoto, Property


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
