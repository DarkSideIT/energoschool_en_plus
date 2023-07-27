from django.urls import path
from . import api, views


urlpatterns = [
    path('', views.scanner, name='scanner'),
    path('events', views.events_view)
]

urlpatterns += [
    path('qrCodeResult/', api.qrCodeResult, name='qrCodeResult')
]
