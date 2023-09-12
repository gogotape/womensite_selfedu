from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify


# Create your views here.
menu = {"О сайте", "Добавить статью", "Обратная связь", "Войти"}


class MyClass:
    def __init__(self, a ,b):
        self.a = a
        self.b = b


data_db = [
    {'id': 1, 'title': 'Джоли', 'content': 'Биография Джоли', 'is_published': True},
    {'id': 2, 'title': 'Робби', 'content': 'Биография Робби', 'is_published': False},
    {'id': 3, 'title': 'Роббертс', 'content': 'Биография Роббертс', 'is_published': True},
    ]


def index(request: HttpRequest) -> HttpResponse:
    data = {'title': 'главная страница',
            'menu': menu,
            'posts': data_db,
            'float': 28.56,
            'lst': [1, 2, 'abcd', True],
            'set': {1, 2, 3, 4, 10, 555},
            'dict': {'key_1': 'value_1', 'key_2': 'value_2'},
            'obj': MyClass(10, 20),
            'url': slugify("The Main page.")
            }

    return render(request, 'women/index.html', context=data)


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'women/about.html')


def categories(request: HttpRequest, cat_id: int) -> HttpResponse:
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id : {cat_id}</p>")


def categories_by_slug(request: HttpRequest, cat_slug: str) -> HttpResponse:
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug : {cat_slug}</p>")


def archive(request: HttpRequest, year: int) -> HttpResponse:
    if year > 2023:
        uri = reverse("cats", args=("sport", ))
        return HttpResponsePermanentRedirect(uri)

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_not_found(request: HttpRequest, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
