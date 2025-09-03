from django.db import models
from django.utils.text import slugify


class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, default='phone')
    phone_two = models.CharField(max_length=20, default='phone')
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class SocialNetwork(models.Model):
    contact = models.ForeignKey(Contact, related_name='social_networks', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField()
    icon = models.CharField(max_length=100, help_text='Название иконки (например, fa-facebook) или путь')
    is_had = models.BooleanField(default=True, verbose_name="В верхнее меню")

    def __str__(self):
        return f"{self.name} - {self.contact.name}"

    class Meta:
        verbose_name = "Соц сети"
        verbose_name_plural = "Соц сети"


class About(models.Model):
    name = models.CharField("Имя компании", max_length=255)
    photo = models.ImageField("Фото компании", upload_to='about_photos/')
    description = models.TextField("Описание")
    unp = models.CharField("УНП", max_length=100, blank=True, null=True)
    license = models.CharField("Лицензия", max_length=100, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"



class Property(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('BYN', 'BYN'),
    ]
    name = models.CharField(max_length=255, verbose_name="Имя/Адрес")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="Для адресной строки ЮРЛ")
    city_name = models.CharField(max_length=255, default='город', verbose_name="Город")
    description = models.TextField(verbose_name="Описание")
    notes = models.TextField(default='Примечание', verbose_name="Примечание")
    address = models.CharField(max_length=500, verbose_name="Адрес")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    floor = models.TextField(help_text='Этаж', verbose_name="Этаж", default=0)
    many_rooms = models.TextField(help_text='Сколько комнат', verbose_name="Сколько комнат", default=0)
    area = models.FloatField(help_text='Площадь в квадратных метрах', verbose_name="Полщадь м/кв")
    area_ga = models.FloatField(help_text='Площадь в гектарах/сотках', verbose_name="Площадь в гектарах/сотках", null=True, blank=True)
    date_posted = models.DateField(auto_now_add=True, verbose_name="Дата добавления")
    is_sale = models.BooleanField(default=True, verbose_name="Продается")
    is_rent = models.BooleanField(default=True, verbose_name="Сдается в аренду")
    is_active_new = models.BooleanField(default=True, verbose_name="Новое объявление")
    is_active_house = models.BooleanField(default=True, verbose_name="Доступен дом")
    is_active_country_house = models.BooleanField(default=True, verbose_name="Доступен загородный дом")
    is_active_apartment = models.BooleanField(default=True, verbose_name="Доступна квартира")
    is_active_sold = models.BooleanField(default=False, verbose_name="Продан")
    contacts = models.ManyToManyField('Contact', related_name='properties', verbose_name="Контакты")
    currency = models.CharField(max_length=3, choices=[('USD', 'USD'), ('BYN', 'BYN')], default='USD', verbose_name="Валюта")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Если slug пустой, генерируем уникальный slug
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Проверяем уникальность slug в базе
            while Property.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Объекты"
        verbose_name_plural = "Объекты"


class PropertyPhoto(models.Model):
    property = models.ForeignKey(Property, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='property_photos/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Фото объекта {self.property.name}"


class PropertyVideo(models.Model):
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    date = models.DateField("Дата", auto_now_add=True)
    property_address = models.CharField("Адрес объекта", max_length=255)
    video_url = models.URLField("Ссылка на видео", max_length=500)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Видео объекта"
        verbose_name_plural = "Видео объектов"
        ordering = ['-date']


class MainSlider(models.Model):
    name = models.CharField("Название слайдера", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Главный слайдер"
        verbose_name_plural = "Главные слайдеры"


class MainSliderPhoto(models.Model):
    name_photo = models.ForeignKey(MainSlider, related_name='photos', on_delete=models.CASCADE, verbose_name="Слайдер")
    photo = models.ImageField("Фото слайда", upload_to='main_slider_photos/')
    desc_text = models.CharField("Описание", max_length=255, blank=True)

    def __str__(self):
        return f"Фото слайдера {self.name_photo.name}"

    class Meta:
        verbose_name = "Фото слайдера"
        verbose_name_plural = "Фото слайдера"



class TrustReason(models.Model):
    icon_class = models.CharField(max_length=100, verbose_name="Класс иконки FontAwesome")
    text = models.CharField(max_length=100, verbose_name="Текст причины")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок вывода")

    class Meta:
        ordering = ['order']
        verbose_name = "Причина доверия"
        verbose_name_plural = "Причины доверия"

    def __str__(self):
        return self.text


class TrustStats(models.Model):
    sold_objects = models.PositiveIntegerField(default=1000, verbose_name="Объектов продано")
    avg_sale_days = models.PositiveIntegerField(default=21, verbose_name="Средний срок продажи (дней)")
    support_247 = models.CharField(max_length=10, default="24", verbose_name="На связи (часов в сутки)")

    def __str__(self):
        return "Статистика доверия"

    class Meta:
        verbose_name = "Статистика доверия"
        verbose_name_plural = "Статистика доверия"

