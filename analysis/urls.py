from django.urls import path
from . import views

urlpatterns = [
    path('analysis/', views.analysis_home, name='analysis_home'),
    path('analysis/combos-results/', views.generate_combos, name='generate_combos'),
    path('analysis/mmps-results/', views.generate_mmps, name='generate_mmps'),
    path('analysis/mmps/', views.get_mmps_ppty_relplot, name='get_mmps_ppty_relplot'),
    path('analysis/boxPlot/', views.display_bbs_ppty_boxPlot, name='display_bbs_ppty_boxPlot'),
    path('analysis/boxPlot/<str:bb_tag>/<str:property>/', views.display_bbs_ppty_boxPlot, name='display_bbs_ppty_boxPlot_with_args'),
    path('analysis/swarmPlot/<str:bb_id>/<str:property>/', views.display_duo_swarmPlot, name='display_duo_swarmPlot'),
    ]
