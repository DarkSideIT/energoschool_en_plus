from django.shortcuts import render
from django.shortcuts import get_object_or_404, Http404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from timetable.models import RecordsLesson, Lesson
from .forms import EditForm


@login_required
def personalView(request):

    user = request.user
    records = RecordsLesson.getLessons(user)

    if user.has_perm('events.view_event') or user.is_superuser:
        return HttpResponseRedirect(reverse('events'))

    navbars = [
        {
            'url': 'personal', 
            'title': request.user.first_name,
            'is_active': True
        },
        {
            'url': 'timetable',
            'title': 'Расписание',
            'is_active': False
        },
        {
            'url': 'market',
            'title': 'Магазин',
            'is_active': False
        },
    ]

    return render(
        request,
        'personal.html',
        {
            'navbars': navbars,
            'records': records
        }
    )

@login_required
def cancelRecordLesson(request, pk):
    lesson = Lesson.objects.get(pk=pk)
    RecordsLesson.deleteRecord(RecordsLesson, request.user, lesson)

    return HttpResponseRedirect(reverse('timetable'))


@login_required
def editPersonal(request):
    if request.method == 'POST':
        form = EditForm(request.POST)

        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('personal') )
    else:
        user = request.user
        form = EditForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'middle_name': user.middle_name,
                'place': user.place,
                'educational_institution': user.educational_institution,
                'class_number': user.class_number,
                'status': user.status,
            })

    return render(
        request, 
        'personal_edit_form.html', 
        {
            'form': form
        }
    )

