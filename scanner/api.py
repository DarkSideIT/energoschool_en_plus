from django.http import JsonResponse, HttpRequest
from json import loads

from timetable.models import Lesson, RecordsLesson
from register.models import User


def qrCodeResult(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        user_email = loads(request.body)['email']

        if not User.objects.filter(email=user_email).exists():
            return JsonResponse({
                'error': 'Ученик не зарегистрирован'
            }, status=404)

        if request.user.id_active_event is None: 
            return JsonResponse({'error': 'Не установленно активное событие!'})

        lesson = Lesson.objects.get(pk=request.user.id_active_event)
        member = User.objects.get(email=user_email)

        if not RecordsLesson.objects.filter(user=member.id, lesson=lesson.id).exists():
            return JsonResponse({'error': 'Ученик не был записан на данное занятие'})

        record = RecordsLesson.objects.get(lesson=lesson.id, user=member.id)

        if record.presence:
            return JsonResponse({'error': 'Был отмечен ранее'})

        record.presence = True
        record.save()
        member.score += lesson.points
        member.save()
        return JsonResponse({'result': 'Успешно отмечен'})

