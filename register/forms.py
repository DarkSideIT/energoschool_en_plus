from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from . import choises as ch
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)

    first_name = forms.CharField(max_length=150, strip=True, label='Имя', required=True)

    last_name = forms.CharField(max_length=150, strip=True, label='Фамилия', required=True)

    middle_name = forms.CharField(max_length=150, strip=True, label='Отчество', required=False)
    
    place = forms.CharField(max_length=255, strip=True, label='Место жительства', required=True)
    
    email = forms.EmailField(label='Личный Email', required=True)
    
    educational_institution = forms.CharField(
        max_length=255, 
        strip=True, 
        label='Образовательное учреждение', 
        required=False
    )
    
    status = forms.ChoiceField(
        choices=ch.STATUS, 
        initial=ch.STATUS[0], 
        label='Статус',
        required=True
    )
    
    class_number = forms.IntegerField(max_value=11, min_value=1, label='Класс/курс', required=False)
    
    phone = forms.RegexField(
        regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', 
        label='Личный контактный телефон',
        required=True
    )
    
   

    class Meta:
        model = User
        fields = [
                'first_name', 'last_name', 'middle_name', 'status',
                'phone', 'email', 'password1', 'password2', 
                'place', 'educational_institution', 'class_number'
            ]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)

        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.middle_name = self.cleaned_data['middle_name']
        user.place = self.cleaned_data['place']
        user.phone = self.cleaned_data['phone']
        user.educational_institution = self.cleaned_data['educational_institution']
        user.class_number = self.cleaned_data['class_number']
        user.status = self.cleaned_data['status']
        
        if commit:
            user.save()
        return user