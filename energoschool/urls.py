from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('events/', include('events.urls')),
    path('scanner/', include('scanner.urls')),
    path('register/', include('register.urls')),
    path('timetable/', include('timetable.urls')),
    path('personal/', include('personal.urls')),
    path('market/', include('market.urls')),

    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('', RedirectView.as_view(url='accounts/login', permanent=True)),
    path('', RedirectView.as_view(url='accounts/password-reset', permanent=True)),
    path('', RedirectView.as_view(url='accounts/password-reset/done/', permanent=True)),
    path('', RedirectView.as_view(url='accounts/password-reset/confirm/', permanent=True)),
    path('', RedirectView.as_view(url='accounts/password-reset/complete/', permanent=True)),
]