from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from timetable.models import Lesson


@login_required
@permission_required('events.view_event')
def scanner(request):
    try:
        event = Lesson.objects.get(pk=request.user.id_active_event)
    except Lesson.DoesNotExist:
        event = None

    navbars = [
        {
            'url': 'events',
            'title': 'Занятия',
            'is_active': False
        },
        {
            'url': 'scanner',
            'title': 'Сканер',
            'is_active': True
        },
        {
            'url': 'admin:index',
            'title': 'Админка',
            'is_active': False
        }
    ]

    return render(
        request,
        'scanner.html',
        {
            'navbars': navbars,
            'event': event
        }
    )

@login_required
def events_view(request):
    return redirect('events/')
