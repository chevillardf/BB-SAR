from django.urls import path
from . import views

urlpatterns = [
    path('design/', views.design_home, name='design_home'),
    path('design/mols-results', views.design_new_mols, name='design_new_mols'),
    ]
