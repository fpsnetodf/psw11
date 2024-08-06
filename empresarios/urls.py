from django.urls import path
from . import views

urlpatterns = [
    path("empresarios/", views.empresarios, name="empresarios"),
    path("cadastrar_empresa/", views.cadastrar_empresa, name="cadastrar-empresa")
]
