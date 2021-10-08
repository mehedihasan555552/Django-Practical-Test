from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    username = models.CharField(unique=True,max_length=200,null=True)
    email = models.EmailField(unique=True,null=True)
    phone_number = PhoneNumberField()
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username



class Plan(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    price = models.IntegerField()
    package = models.CharField(max_length=200,null=True,blank=True)
    premium = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)

    def __str__(self):
        return self.stripeid