from django.shortcuts import render

# Create your views here.


def empresarios(request):
    return render(request, "empresarios/empresarios.html")