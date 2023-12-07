from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponsePermanentRedirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from women.models import Women, Category, TagPost
from women.forms import AddPostForm

# Create your views here.
menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contacts'},
    {'title': 'Войти', 'url_name': 'login'},
]


class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


def index(request: HttpRequest) -> HttpResponse:
    posts = Women.published.all().select_related("cat")

    data = {'title': 'главная страница',
            'menu': menu,
            'posts': posts,
            'float': 28.56,
            'lst': [1, 2, 'abcd', True],
            'set': {1, 2, 3, 4, 10, 555},
            'dict': {'key_1': 'value_1', 'key_2': 'value_2'},
            'obj': MyClass(10, 20),
            'url': slugify("The Main page."),
            'cat_selected': 0,
            }

    return render(request, 'women/index.html', context=data)


def posts(requests: HttpRequest, women_id: int) -> HttpResponse:
    return HttpResponse(f"<h1> {women_id}, {filter(lambda x: x['id'] == women_id, data_db).__next__()} </h1>")


def alter_posts(requests: HttpRequest, post_id: int) -> HttpResponse:
    return HttpResponse(f"<h3> Отображение статьи c id:{post_id} </h3>")


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'women/about.html', {'title': "О сайте", 'menu': menu})


def categories(request: HttpRequest, cat_id: int) -> HttpResponse:
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id : {cat_id}</p>")


def categories_by_slug(request: HttpRequest, cat_slug: str) -> HttpResponse:
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug : {cat_slug}</p>")


def archive(request: HttpRequest, year: int) -> HttpResponse:
    if year > 2023:
        uri = reverse("cats", args=("sport",))
        return HttpResponsePermanentRedirect(uri)

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def show_category(request: HttpRequest, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category).select_related("cat")
    data = {'title': f'Рубрика: {category.name}',
            'menu': menu,
            'posts': posts,
            'float': 28.56,
            'lst': [1, 2, 'abcd', True],
            'set': {1, 2, 3, 4, 10, 555},
            'dict': {'key_1': 'value_1', 'key_2': 'value_2'},
            'obj': MyClass(10, 20),
            'url': slugify("The Main page."),
            'cat_selected': category.pk,
            }

    return render(request, 'women/index.html', context=data)


def page_not_found(request: HttpRequest, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_post(request: HttpRequest, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1
    }

    return render(request, 'women/post.html', data)


def addpage(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            try:
                Women.objects.create(**form.cleaned_data)
                return redirect("home")
            except:
                form.add_error(None, "Ошибка добавления поста")
    else:
        form = AddPostForm()

    data = {
        "menu": menu,
        "title": "Добавление статьи",
        "form": form,
    }

    return render(request, 'women/addpage.html', data)


def contacts(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Обратная связь")


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Авторизация")


def show_tag_postlist(request: HttpRequest, tag_slug) -> HttpResponse:
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related("cat")

    data = {
        'title': f"TAG: {tag.tag}",
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', context=data)
