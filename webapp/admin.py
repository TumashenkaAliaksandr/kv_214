from django.contrib import admin
from .models import Contact, SocialNetwork

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
