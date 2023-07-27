from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, Http404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import FileResponse
from timetable.models import Lesson, RecordsLesson
from register.models import User
from .forms import LessonForm
from . import api
from datetime import date, timedelta


@login_required
@permission_required('events.view_event')
def events(request):
    try:
        active_lesson = Lesson.objects.get(pk=request.user.id_active_event)
    except Lesson.DoesNotExist:
        active_lesson = None

    lessons = []

    startdate = date.today()
    enddate = startdate + timedelta(days=31)

    try:
        lessons = Lesson.objects.filter(lesson_date__range=[startdate, enddate]).order_by('lesson_date')
    except Lesson.DoesNotExist:
        pass
    # try:
    #     lessonsID = RecordsLesson.objects.all().values_list('lesson', flat=True).distinct()
    #     startdate = date.today()
    #     enddate = startdate + timedelta(days=10)
    #     for lessonID in lessonsID:
    #         try:
    #             lesson = Lesson.objects.get(pk=lessonID, lesson_date__range=[startdate, enddate])
    #             lessons.append(lesson)
    #         except Lesson.DoesNotExist:
    #             pass
    #             # User.objects.filter(id_active_event=request.user.id_active_event).update(id_active_event=None)

    #     lessons.sort(key=lambda x: x.lesson_date)
    # except RecordsLesson.DoesNotExist:
    #     User.objects.filter(id_active_event=request.user.id_active_event).update(id_active_event=None)


    navbars = [
        {
            'url': 'events',
            'title': 'Занятия',
            'is_active': True
        },
        {
            'url': 'scanner',
            'title': 'Сканер',
            'is_active': False
        },
        {
            'url': 'admin:index',
            'title': 'Админка',
            'is_active': False
        }
    ]

    return render(
        request,
        'events.html',
        {
            'navbars': navbars,
            'lessons': lessons, 
            'active_lesson': active_lesson
        }
    )

@login_required
@permission_required('events.view_event')
def scanner_view(request):
    return redirect('scanner/')

@login_required
@permission_required('events.view_event')
def eventDetail(request, pk):
    try:
        lesson = Lesson.objects.get(pk=pk)
    except Lesson.DoesNotExist:
        raise Http404("Lesson does not exist")

    records = RecordsLesson.objects.filter(lesson=pk).values_list('user', 'presence')
    members_info = []
    for i, record in enumerate(records): 
        member_info = {
            'member': User.objects.get(pk=record[0]),
            'number': i + 1,
            'presence': record[1]
        }
        members_info.append(member_info)
    is_active_lesson = request.user.id_active_event == pk
    name_button = "Активно" if is_active_lesson else "Сделать активным"

    return render(
        request,
        'events/event_detail.html',
        {
            'lesson': lesson,
            'members_info': members_info,
            'cnt_members': '' if len(members_info) == 0 else len(members_info),
            'is_active_lesson': is_active_lesson,
            'name_button': name_button,
        }
    )

@login_required
@permission_required('events.view_event')
def eventCreate(request):

    if request.method == 'POST':
        form = LessonForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('events'))
    else:
        form = LessonForm()

    return render(
        request, 
        'events/event_form.html', 
        {
            'form': form, 
            'nameButton': 'Добавить'
        }
    )

@login_required
@permission_required('events.view_event')
def eventUpdate(request, pk):

    try:
        lesson = Lesson.objects.get(pk=pk)
    except Lesson.DoesNotExist:
        raise Http404("Event does not exist")

    if request.method == 'POST':
        form = LessonForm(request.POST)

        if form.is_valid():
            form.save(pk)
            return HttpResponseRedirect(reverse('events') )
    else:
        form = LessonForm(initial={
                'name': lesson.name,
                'track': lesson.track,
                'lesson_format': lesson.lesson_format,
                'lesson_date': lesson.lesson_date,
                'lesson_time': lesson.lesson_time,
                'theme': lesson.theme,
                'status': lesson.status,
                'audience': lesson.audience,
                'teacher': lesson.teacher,
                'place': lesson.place,
                'city': lesson.city,
                'required_items': lesson.required_items,
                'count_seats': lesson.count_seats,
                'points': lesson.points
            })

    return render(
        request, 
        'events/event_form.html', 
        {
            'form': form,
            'event_id': lesson.id,
            'nameButton': 'Изменить'
        }
    )

@login_required
@permission_required('events.view_event')
def eventDelete(request, pk):
    try:
        lesson = Lesson.objects.get(pk=pk)
    except Lesson.DoesNotExist:
        raise Http404("Event does not exist")

    lesson.delete()
    User.objects.filter(id_active_event=pk).update(id_active_event=None)

    return HttpResponseRedirect(reverse('events'))

@login_required
@permission_required('events.view_event')
def eventSetActive(request, pk):
    try:
        event = Lesson.objects.get(pk=pk)
    except Lesson.DoesNotExist:
        raise Http404("Event does not exist")

    User.objects.filter(pk=request.user.id).update(id_active_event=event.id)

    return HttpResponseRedirect(reverse('events'))

@login_required
@permission_required('events.view_event')
def eventSetComplete(request, pk):
    """Помечает мероприятие как завершенное и списывает баллы с людей, которых не отсканили"""
    records = RecordsLesson.objects.filter(lesson=pk)
    lesson = Lesson.objects.get(pk=pk)
    User.objects.filter(id_active_event=pk).update(id_active_event=None)
    for record in records:
        if not record.presence:
            record.user.score -= lesson.points
            record.user.save()
    
    lesson.is_completed = True
    lesson.save()

    return HttpResponseRedirect(reverse('events'))