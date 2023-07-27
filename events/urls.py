from django.urls import path
from . import views, api


urlpatterns = [
    path('', views.events, name='events'),
    path('scanner', views.scanner_view)
]

urlpatterns += [
    path('create/', views.eventCreate, name='event_create'),
    path('export/', api.allExportData, name='all_export'),
    path('<int:pk>/', views.eventDetail, name='event_detail'),
    path('<int:pk>/update/', views.eventUpdate, name='event_update'),
    path('<int:pk>/delete/', views.eventDelete, name='event_delete'),
    path('<int:pk>/set_active/', views.eventSetActive, name='event_set_active'),
    path('<int:pk>/export/', api.exportData, name='event_export'),
    path('<int:pk>/complete/', views.eventSetComplete, name='event_complete'),
]

urlpatterns += [
    path('<int:pk>/markVisit/', api.markVisit, name='mark_visit'),
    path('<int:pk>/cancelVisit/', api.cancelVisit, name='cancel_visit'),
]