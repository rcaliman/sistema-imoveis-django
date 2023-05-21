from django.shortcuts import render, redirect
from imoveis.forms import FormLogin
from django.contrib.auth import authenticate, login, logout
from helper import verifica_autenticacao


def index(request):
    verifica_autenticacao(request)
    if request.method == "POST":
        usuario = request.POST["usuario"]
        senha = request.POST["senha"]
        autenticacao = authenticate(request, username=usuario, password=senha)
        if autenticacao is not None:
            login(request, autenticacao)
            return redirect("index")
    form = FormLogin()
    return render(request, "index.html", {"form": form})


def imoveis_logout(request):
    verifica_autenticacao(request)
    logout(request)
    return redirect("index")
