from django import forms
from timetable.models import Lesson
from register.choises import STATUS_ADMIN

class LessonForm(forms.Form):

    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)
    
    name = forms.CharField(max_length=255, strip=True, label='Название', required=True)
    track = forms.CharField(max_length=120, strip=True, label='Трэк', required=False)
    lesson_format = forms.CharField(max_length=120, strip=True, required=True, label='Формат')
    lesson_date = forms.DateField(required=True, label='Дата', widget=forms.SelectDateWidget())
    lesson_time = forms.CharField(max_length=120, strip=True, required=True, label='Время')
    city = forms.CharField(max_length=120, strip=True, required=True, label='Город')
    theme = forms.CharField(required=False, label='Тема', widget=forms.Textarea(attrs={'rows':3, 'cols':28}))
    status = forms.ChoiceField(choices=STATUS_ADMIN, label='Статус участника', required=True)
    audience = forms.CharField(max_length=120, label='Целевая аудитория', required=False)
    teacher = forms.CharField(max_length=255, label='Спикер', required=False)
    place = forms.CharField(max_length=255, label='Место', required=True)
    required_items = forms.CharField(max_length=255, label='Что взять с собой', required=False)
    count_seats = forms.IntegerField(label='Кол-во мест')
    points = forms.IntegerField(initial=5, label='Кол-во баллов')

    def save(self, pk=0):
        if pk == 0:
            lesson = Lesson()
        else:
            lesson = Lesson.objects.get(pk=pk)
            
        lesson.name = self.cleaned_data['name']
        lesson.track = self.cleaned_data['track']
        lesson.lesson_format = self.cleaned_data['lesson_format']
        lesson.lesson_date = self.cleaned_data['lesson_date']
        lesson.lesson_time = self.cleaned_data['lesson_time']
        lesson.theme = self.cleaned_data['theme']
        lesson.status = self.cleaned_data['status']
        lesson.audience = self.cleaned_data['audience']
        lesson.teacher = self.cleaned_data['teacher']
        lesson.place = self.cleaned_data['place']
        lesson.city = self.cleaned_data['city']
        lesson.required_items = self.cleaned_data['required_items']
        lesson.count_seats = self.cleaned_data['count_seats']
        lesson.points = self.cleaned_data['points']

        lesson.save()