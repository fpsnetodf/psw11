from django.urls import path
from . import views

urlpatterns = [
    path("empresarios/", views.empresarios, name="empresarios")
]
