from django.contrib import admin
from django.utils.html import format_html

from .forms import ObjectForm
from .models import Contact, SocialNetwork, PropertyPhoto, Property, PropertyVideo, MainSliderPhoto, MainSlider, \
    TrustStats, TrustReason, About, Messengers


class PropertyPhotoInline(admin.TabularInline):
    model = PropertyPhoto
    extra = 3  # кол-во дополнительных форм для загрузки фото

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    form = ObjectForm
    list_display = ['name', 'address', 'city_name', 'price', 'area', 'area_ga', 'date_posted', 'is_active_new', 'is_active_sold']
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

    # Можно запретить создание множественных объектов, если нужна всего одна запись
    def has_add_permission(self, request):
        # Если записей больше 0, создание запрещено
        return not TrustStats.objects.exists()
