from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListActividad.as_view(), name='lista-actividad'),
]
