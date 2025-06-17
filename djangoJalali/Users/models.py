import jdatetime
from django.db import models
import django_jalali.db.models as jmodels


class CustomUser(models.Model):
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    username = models.CharField(max_length=256)
    full_name = models.CharField(max_length=256)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    national_code = models.CharField(max_length=10)
    birthday_date = jmodels.jDateField()
    ceremony_datetime = jmodels.jDateTimeField()
    country = models.CharField(default='Iran', max_length=5)

    def get_first_and_last_name(self):
        part = self.full_name.split()
        dict_full_name = {
            'first_name': part[0],
            'last_name': part[1]
        }
        return dict_full_name

    def get_age(self):
        now = jdatetime.date.today()
        age = now.year - self.birthday_date.year
        if (now.month, now.day) < (self.birthday_date.month, self.birthday_date.day):
            age -= 1
        return age
    def is_birthday(self):
        now = jdatetime.date.today()
        if self.birthday_date.month == now.month and self.birthday_date.day == now.day:
            return True
        else:
            return False
