from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Car(models.Model):
    time = models.IntegerField(null=True, blank=True)
    about = models.TextField(max_length=355, null=True, blank=True)
    shortAbout = models.CharField(max_length=70, null=True, blank=True)
    brand = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=70, null=True, blank=True)
    topSpeed = models.IntegerField(null=True, blank=True)
    nm = models.IntegerField(null=True, blank=True)
    hp = models.IntegerField(null=True, blank=True)
    seats = models.IntegerField(null=True, blank=True)
    price = models.CharField(max_length=10, null=True, blank=True)
    insurance = models.IntegerField(null=True, blank=True)
    tank = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.model


class Rental(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    total_price = models.IntegerField(null=True, blank=True)
    borrow_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user_id.first_name + ' ' + self.user_id.last_name
