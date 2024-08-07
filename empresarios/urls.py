from django.urls import path
from . import views

urlpatterns = [
    path("empresarios/", views.empresarios, name="empresarios"),
    path("cadastrar_empresa/", views.cadastrar_empresa, name="cadastrar-empresa"),
    path('listar_empresas/', views.listar_empresas, name="listar_empresas"),
    path('empresa/<int:id>/', views.empresa, name="empresa"),
]
