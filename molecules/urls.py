from django.urls import path
from . import views

urlpatterns = [
    path('molecules/', views.molecules_home, name='molecules_home'),
    path('molecules/<mol_id>', views.molecule_home, name='molecule_home'),
    path('molecules/suggest/<str:mol_id>/<str:property>/', views.suggested_molecules, name='suggested_molecules'),
]
