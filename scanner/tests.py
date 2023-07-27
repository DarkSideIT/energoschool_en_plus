from django.test import TestCase, RequestFactory
from json import loads
from datetime import datetime

from register.models import User
from timetable.models import Lesson, RecordsLesson
from .api import qrCodeResult

# Create your tests here.

class ScannerTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(email='example@mail.com')
        self.lesson = Lesson.objects.create(
            name='Тестовое событие',
            lesson_date=datetime.now().date(),
            lesson_time='11:00-12:00'
            )
    
    def _make_request(self, email: str):
        request = self.factory.post('/scanner/qrCodeResult/', {'email': email})
        request.user = self.user
        response = qrCodeResult(request)
        data = loads(response.content)

        return response.status_code, data
    
    def test_user_does_not_exists(self):
        status_code, data = self._make_request(email='unknown')
        
        self.assertEqual(status_code, 404)
        self.assertEqual(data.get('error'), 'Ученик не зарегистрирован')

    def test_event_not_setted(self):
        status_code, data = self._make_request(email=self.user.email)
        
        self.assertEqual(status_code, 200)
        self.assertEqual(data.get('error'), 'Не установленно активное событие!')
    
    def test_member_have_not_appointed(self):
        self.user.id_active_event = self.lesson.pk
        self.user.save()

        status_code, data = self._make_request(email=self.user.email)

        self.assertEqual(status_code, 200)
        self.assertEqual(data.get('error'), 'Ученик не был записан на данное занятие')
    
    def test_member_have_appointed(self):
        self.user.id_active_event = self.lesson.pk

        RecordsLesson.objects.create(user=self.user, lesson=self.lesson)
        status_code, data = self._make_request(email=self.user.email)

        self.assertEqual(status_code, 200)
        self.assertEqual(data.get('result'), 'Успешно отмечен')
    
    def test_member_already_presence(self):
        self.user.id_active_event = self.lesson.pk

        RecordsLesson.objects.create(user=self.user, lesson=self.lesson, presence=True)
        status_code, data = self._make_request(email=self.user.email)

        self.assertEqual(status_code, 200)
        self.assertEqual(data.get('error'), 'Был отмечен ранее')
    
