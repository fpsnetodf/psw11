from django.shortcuts import render
from .models import Empresas
# Create your views here.


def empresarios(request):
    return render(request, "empresarios/empresarios.html")


def cadastrar_empresa(request):
    if request.method == "GET":
        tempos = Empresas.tempo_existencia_choices
        areas = Empresas.area_choices
        return render(request, "empresarios/cadastrar_empresa.html", {"tempos": tempos, "areas": areas })