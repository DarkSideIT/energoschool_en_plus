from django.db import models
from django.urls import reverse
from register.models import User
from register.choises import STATUS_ADMIN

class Lesson(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name='Название')
    track = models.CharField(max_length=50, blank=True, verbose_name='Трэк')
    lesson_format = models.CharField(max_length=120, verbose_name='Формат')
    lesson_date = models.DateField(verbose_name='Дата')
    lesson_time = models.CharField(max_length=50, verbose_name='Время')
    theme = models.TextField(blank=True, verbose_name='Тема')
    status = models.CharField(max_length=120, choices=STATUS_ADMIN, default=STATUS_ADMIN[0][0], verbose_name='Статус участника')
    audience = models.CharField(max_length=120, verbose_name='Целевая аудитория', blank=True)
    teacher = models.CharField(max_length=255, blank=True, verbose_name='Спикер')
    city = models.CharField(max_length=120, default='Иркутск', verbose_name='Город')
    place = models.CharField(max_length=255, verbose_name='Место')
    required_items = models.CharField(max_length=255, verbose_name='Что взять с собой', blank=True)
    count_seats = models.IntegerField(default=0, verbose_name='Кол-во мест')
    count_records = models.IntegerField(default=0, verbose_name='Кол-во записей')
    points = models.IntegerField(default=5, verbose_name='Кол-во баллов')
    is_completed = models.BooleanField(default=False, verbose_name='Завершенно')

    def get_absolute_url(self):
        return reverse('event_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.lesson_date}: {self.name if self.name else self.theme}'

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'


class RecordsLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson')
    presence = models.BooleanField(blank=True, default=False)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def updateCountRecords(lesson):
        cnt_records = RecordsLesson.objects.filter(lesson=lesson).count()
        Lesson.objects.filter(pk=lesson.id).update(count_records=cnt_records)

    def createRecord(self, user, lesson):
        record = RecordsLesson()
        record.user = user
        record.lesson = lesson
        record.save()
        self.updateCountRecords(lesson)

    def deleteRecord(self, user, lesson):
        record = RecordsLesson.objects.filter(user=user, lesson=lesson)
        record.delete()
        self.updateCountRecords(lesson)

    def getLessons(user):
        records_id = RecordsLesson.objects.filter(user=user).values('lesson')
        records = []
        for record in records_id:
            records.append(Lesson.objects.get(pk=record['lesson']))

        return records

    def getPresence(user, lesson):
        try:
            record = RecordsLesson.objects.get(user=user, lesson=lesson)
        except RecordsLesson.DoesNotExist:
            return False

        return record.presence