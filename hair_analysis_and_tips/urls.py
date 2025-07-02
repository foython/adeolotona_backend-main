from django.urls import path
from . import views

urlpatterns = [
    path('analyze_hair/', views.analyze_hair, name='analyze_hair'),
    path('get_user_previous_analysis/', views.get_user_previous_analysis, name='get_user_previous_analysis')
]
