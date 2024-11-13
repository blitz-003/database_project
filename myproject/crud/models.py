from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 70)
    email = models.CharField(max_length = 70) # Here can use Emailfield, have Django's inbuilt validation for emails
    password = models.CharField(max_length = 70) #django does not have a passwordfield. have to use charfield and render it using widget=passwordinput
    