from typing import Any
from django import forms
from Users.models import CustomUser
from django.forms import ValidationError


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "username", 
            'gender',
            'country',
            'full_name',
            'national_code',
            'birthday_date',
            'ceremony_datetime'
        ]

    def clean_national_code(self):
        na = self.cleaned_data.get('national_code')
        if not na:
            raise ValidationError('error')
        if not na.isdigit():
            raise ValidationError('wrong')
        elif len(na) != 10:
            raise ValidationError('invalid code')
        else:
            return na



    def clean_full_name(self):
        if not self.cleaned_data.get('full_name'):
            raise ValidationError('is Empty')
        if ' ' in self.cleaned_data.get('full_name'):
            fn = self.cleaned_data.get('full_name').split()
            if len(fn) < 2:
                raise ValidationError('invalid')
            name = fn[0]
            lname = fn[1]
            if name != name.capitalize():
                raise ValidationError('This name is not valid.')
            elif lname != lname.capitalize():
                raise ValidationError('This name is not valid.')

            else:
                return self.cleaned_data.get('full_name')
        else:
            raise ValidationError('Full name must contain a space between first and last name.')

