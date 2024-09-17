from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.projects_home, name='projects_home'),
    path('projects', views.projects_home, name='projects_home'),
    path('set-series/<int:series_id>/', views.set_series, name='set_series'),
    path('projects/pw', views.password_login, name='password_login'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# https://stackoverflow.com/questions/51464131/multiple-parameters-url-pattern-django-2-0
