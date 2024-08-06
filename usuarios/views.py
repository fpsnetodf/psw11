from django.shortcuts import render, redirect
from django.contrib import auth 
# from django.models import User

# Create your views here.


def home(request):
    return render(request, "usuarios/home.html")


def cadastro(request):
    if request.method == "GET":
        return render(request, "usuarios/cadastro.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if not senha == confirmar_senha:
            print(1)
            return redirect('/cadastro')
        
        if len(senha) < 6:
            print(2)
            return redirect('/cadastro')
        
        users = User.objects.filter(username=username)
        if users.exists():
            print(3)
            return redirect('/cadastro')
        # user = User.objects.create_user(
        # username=username,
        # password=senha
        # )
        return redirect('/usuarios/logar')

def logar(request):
    if request.method == "GET":
        return render(request, 'usuarios/logar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = auth.authenticate(request, username=username, password=senha)
        if user:
            auth.login(request, user)
            return redirect('/home') # Vai dar erro
            messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
            return redirect('/usuarios/logar')
