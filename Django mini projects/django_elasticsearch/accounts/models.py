from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):

    GENDER_CHOICE = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    ]
    LEVEL = [
        ('1-5', '1-5'),
        ('5-10', '5-10'),
        ('10-12', '10-12'),
        ('Engineering', 'Engineering'),
        ('Medical', 'Medical'),
        ('Law', 'Law')
    ]
    PHONE_REGREX = RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
    sex = models.CharField(choices=GENDER_CHOICE, max_length=10, null=True)
    level = models.CharField(choices=LEVEL, max_length=20, null=True)
    date_of_birth = models.DateField(null=True)
    phone = models.CharField(validators=[PHONE_REGREX], max_length=16, null=True)
    bio = models.TextField(null=True)
    
    def __str__(self):
        return self.username