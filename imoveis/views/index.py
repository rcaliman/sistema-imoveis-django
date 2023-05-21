from django.shortcuts import render, redirect
from imoveis.forms import FormLogin
from django.contrib.auth import authenticate, login, logout


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    if request.method == 'POST':
        usuario = request.POST['usuario']
        senha = request.POST['senha']
        autenticacao = authenticate(request, username=usuario, password=senha)
        if autenticacao is not None:
            login(request, autenticacao)
            return redirect('index')
    form = FormLogin()
    return render(request, 'index.html', {'form': form})


def imoveis_logout(request):
    if not request.user.is_authenticated:
        return redirect('index')
    logout(request)
    return redirect('index')

