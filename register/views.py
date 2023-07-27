from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from .forms import RegisterForm
from django.contrib.auth import login


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return HttpResponseRedirect(reverse('timetable'))

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})