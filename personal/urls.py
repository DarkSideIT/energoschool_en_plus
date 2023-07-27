from django.urls import path
from . import views


urlpatterns = [
    path('', views.personalView, name='personal'),
    path('edit/', views.editPersonal, name='edit_personal'),
    path('cancel_record_<int:pk>/', views.cancelRecordLesson, name='cancel_record'),
]