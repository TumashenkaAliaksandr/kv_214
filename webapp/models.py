from django.db import models
from django.utils.text import slugify


class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, default='phone')
    phone_two = models.CharField(max_length=20, default='phone')
    email = models.EmailField()

    def __str__(self):
        return self.name

class SocialNetwork(models.Model):
    contact = models.ForeignKey(Contact, related_name='social_networks', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField()
    icon = models.CharField(max_length=100, help_text='Название иконки (например, fa-facebook) или путь')

    def __str__(self):
        return f"{self.name} - {self.contact.name}"


class About(models.Model):
    name = models.CharField("Имя компании", max_length=255)
    photo = models.ImageField("Фото компании", upload_to='about_photos/')
    description = models.TextField("Описание")
    unp = models.CharField("УНП", max_length=100, blank=True, null=True)
    license = models.CharField("Лицензия", max_length=100, blank=True, null=True)
    phone = models.CharField("Телефон", max_length=20)

    def __str__(self):
        return self.name



class Property(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('BYN', 'BYN'),
    ]
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    city_name = models.CharField(max_length=255, default='город')
    description = models.TextField()
    notes = models.TextField(default='Примечание')
    address = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    floor = models.TextField(help_text='Этаж', default=0)
    many_rooms = models.TextField(help_text='Сколько комнат', default=0)
    area = models.FloatField(help_text='Площадь в квадратных метрах')
    area_ga = models.FloatField(help_text='Площадь в гектарах/сотках', null=True, blank=True)
    date_posted = models.DateField(auto_now_add=True)
    is_sale = models.BooleanField(default=True)
    is_rent = models.BooleanField(default=True)
    is_active_new = models.BooleanField(default=True)
    is_active_house = models.BooleanField(default=True)
    is_active_country_house = models.BooleanField(default=True)
    is_active_apartment = models.BooleanField(default=True)
    is_active_sold = models.BooleanField(default=False)
    contacts = models.ManyToManyField(Contact, related_name='properties')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

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
    name = models.CharField("Название", max_length=255)


    def __str__(self):
        return self.name

class MainSliderPhoto(models.Model):
    name_photo = models.ForeignKey(MainSlider, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='main_slider_photos/')
    desc_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Фото Слайдера {self.name_photo.name}"


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

