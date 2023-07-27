from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Lesson, RecordsLesson
from register.choises import STATUS_ADMIN
import json
from datetime import date, timedelta, datetime
import pytz
import re


@login_required
def timetableView(request):
    if request.user.has_perm('events.view_event') or request.user.is_superuser:
        return HttpResponseRedirect(reverse('events'))
        
    now = datetime.now(pytz.timezone('Asia/Irkutsk'))
    current_hours = now.strftime("%H")

    startdate = date.today()
    tomorrow = startdate + timedelta(days=1)
    enddate = startdate + timedelta(days=14)
    try:
        lessons = Lesson.objects.filter(lesson_date__range=[startdate, enddate]).order_by('lesson_date')
    except Lesson.DoesNotExist:
        pass

    user_status = request.user.status

    lessons_filter = []
    try:
        for lesson in lessons:
            lesson_status = lesson.status
            if lesson_status in (STATUS_ADMIN[0][0], STATUS_ADMIN[1][0]) and user_status == lesson_status:
                user_class = request.user.class_number
                class_range = re.findall(r'\d+', lesson.audience)
                if len(class_range) == 1:
                    if user_class >= int(class_range[0]):
                        lessons_filter.append(lesson)
                else:
                    if int(class_range[0]) <= user_class <= int(class_range[1]):
                        lessons_filter.append(lesson)
            elif lesson_status == STATUS_ADMIN[2][0] and user_status == lesson_status:
                lessons_filter.append(lesson)
            elif lesson_status == STATUS_ADMIN[3][0]:
                lessons_filter.append(lesson)
    except Exception:
        pass

    my_lessons, other_lessons = [], []

    for lesson in lessons_filter:
        if RecordsLesson.objects.filter(user=request.user, lesson=lesson):
            my_lessons.append({
                'lesson': lesson, 
                'available': lesson.lesson_date > tomorrow or (lesson.lesson_date == tomorrow and int(current_hours) < 17)
            })
        else:
            if lesson.lesson_date > tomorrow or (lesson.lesson_date == tomorrow and int(current_hours) < 17):
                other_lessons.append(lesson)


    navbars = [
        {
            'url': 'personal',
            'title': request.user.first_name,
            'is_active': False
        },
        {
            'url': 'timetable',
            'title': 'Расписание',
            'is_active': True
        },
        {
            'url': 'market',
            'title': 'Магазин',
            'is_active': False
        },
    ]

    return render(
        request,
        'timetable.html',
        {
            'navbars': navbars,
            'other_lessons': other_lessons,
            'my_lessons': my_lessons 
        }
    )

@login_required
def recordLesson(request, pk):
    lesson = Lesson.objects.get(pk=pk)

    if lesson.count_seats > lesson.count_records:
        if not RecordsLesson.objects.filter(user=request.user, lesson=lesson):
            RecordsLesson.createRecord(RecordsLesson, request.user, lesson)
            response = {
                'type': 'success',
                'message': 'Вы успешно записаны', 
                'count_records': lesson.count_records + 1,
                'count_seats': lesson.count_seats
            }
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            response = {
                'type': 'error',
                'message': 'Вы уже записаны на данное занятие!'
            }
            return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        response = {
            'type': 'error',
            'message': 'Места на запись закончены'
        }
        return HttpResponse(json.dumps(response), content_type='application/json')
