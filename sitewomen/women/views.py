from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Страница приложения women")


def categories(request: HttpRequest, cat_id: int) -> HttpResponse:
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id : {cat_id}</p>")


def categories_by_slug(request: HttpRequest, cat_slug: str) -> HttpResponse:
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug : {cat_slug}</p>")


def archive(request: HttpRequest, year: int) -> HttpResponse:
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")