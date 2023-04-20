from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return HttpResponse('Hello '+request.user.nickname+'!')
    else:
        return HttpResponse('Hello there!')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})
