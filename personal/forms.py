from django import forms
from register.models import User
from register import choises as ch
from django.core.exceptions import ValidationError


class EditForm(forms.Form):

    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)

    first_name = forms.CharField(max_length=150, strip=True, label='Имя', required=True)

    last_name = forms.CharField(max_length=150, strip=True, label='Фамилия', required=True)

    middle_name = forms.CharField(max_length=150, strip=True, label='Отчество', required=False)
    
    place = forms.CharField(max_length=255, strip=True, label='Место жительства', required=True)
    
    status = forms.ChoiceField(
        choices=ch.STATUS, 
        initial=ch.STATUS[0], 
        label='Статус',
        required=True
    )
    
    educational_institution = forms.CharField(
        max_length=255, 
        strip=True, 
        label='Образовательное учреждение', 
        required=False
    )
    
    class_number = forms.IntegerField(max_value=11, min_value=1, label='Класс/курс', required=False)
   

    class Meta:
        model = User
        fields = [
                'first_name', 'last_name', 'middle_name', 'status',
                'place', 'educational_institution', 'class_number'
            ]

    def save(self, user):
        
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.middle_name = self.cleaned_data['middle_name']
        user.place = self.cleaned_data['place']
        user.educational_institution = self.cleaned_data['educational_institution']
        user.class_number = self.cleaned_data['class_number']
        user.status = self.cleaned_data['status']
        
        user.save()