from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.


def login_user(request: HttpRequest):
    return HttpResponse("login")


def logout_user(request: HttpRequest):
    return HttpResponse("logout")
