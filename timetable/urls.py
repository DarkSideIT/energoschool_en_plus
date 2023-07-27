from django.urls import path
from . import views


urlpatterns = [
    path('', views.timetableView, name='timetable'),
    path('record_<int:pk>/', views.recordLesson, name='record_lesson'),
]