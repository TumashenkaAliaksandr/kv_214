from django.db import models

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
