from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponsePermanentRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from women.models import Women, Category, TagPost, UploadFile
from women.forms import AddPostForm, UploadFileForm

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


class WomenHomePage(ListView):
    # model = Women
    # queryset = Women.published.all().select_related("cat")
    context_object_name = "posts"
    template_name = 'women/index.html'
    extra_context = {'title': 'главная страница',
                     'menu': menu,
                     'cat_selected': 0,
                     }

    def get_queryset(self):
        return Women.published.all().select_related("cat")


def posts(requests: HttpRequest, women_id: int) -> HttpResponse:
    return HttpResponse(f"<h1> {women_id}, {filter(lambda x: x['id'] == women_id, data_db).__next__()} </h1>")


def alter_posts(requests: HttpRequest, post_id: int) -> HttpResponse:
    return HttpResponse(f"<h3> Отображение статьи c id:{post_id} </h3>")


# def handle_upload_file(file):
#     with open(f"uploads/{file.name}", "+wb") as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)


def about(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # handle_upload_file(request.FILES["file_upload"])
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            UploadFile(file=form.cleaned_data["file"]).save()
    else:
        form = UploadFileForm()
    return render(request, 'women/about.html', {'title': "О сайте",
                                                'menu': menu,
                                                'form': form}
                  )


def categories(request: HttpRequest, cat_id: int) -> HttpResponse:
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id : {cat_id}</p>")


def categories_by_slug(request: HttpRequest, cat_slug: str) -> HttpResponse:
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug : {cat_slug}</p>")


def archive(request: HttpRequest, year: int) -> HttpResponse:
    if year > 2023:
        uri = reverse("cats", args=("sport",))
        return HttpResponsePermanentRedirect(uri)

    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


class ShowCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        context["title"] = "Категория - " + cat.name
        context["menu"] = menu
        context["cat_selected"] = cat.pk
        return context


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


class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    allow_empty = False
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["post"].title
        context["menu"] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(CreateView):
    model = Women
    fields = ("title", "slug", "content", "is_published", "cat")
    template_name = 'women/addpage.html'
    # success_url = reverse_lazy("home")

    extra_context = {
        "title": "Добавление статьи",
        "menu": menu,
    }


class UpdatePage(UpdateView):
    model = Women
    fields = ("title", "content", "photo", "is_published", "cat")
    template_name = 'women/addpage.html'
    success_url = reverse_lazy("home")

    extra_context = {
        "title": "Редактирование статьи",
        "menu": menu,
    }


def contacts(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Обратная связь")


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Авторизация")


class ShowTag(ListView):
    template_name = 'women/index.html'
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs["tag_slug"]).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        context["title"] = "Тег - " + tag.tag
        context["menu"] = menu
        context["cat_selected"] = None
        return context
