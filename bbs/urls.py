from django.urls import path
from . import views

urlpatterns = [
    path('bbs/', views.bbs_home, name='bbs_home'),
    path('bbs/<bb_id>', views.bb_home, name='bb_home')
]