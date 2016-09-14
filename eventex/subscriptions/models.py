from django.db import models

class Subscription(models.Model):
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    email = models.CharField()
    phone = models.CharField(max_length=20)
