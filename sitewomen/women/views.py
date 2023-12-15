from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponsePermanentRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from women.models import Women, Category, TagPost, UploadFile
from women.forms import AddPostForm, UploadFileForm
from women.utils import DataMixin


# Create your views here.
class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class WomenHomePage(DataMixin, ListView):
    # queryset = Women.published.all().select_related("cat")
    context_object_name = "posts"
    template_name = 'women/index.html'
    title_page = "Главная страница"
    cat_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related("cat")


def posts(requests: HttpRequest, women_id: int) -> HttpResponse:
    return HttpResponse(f"<h1> {women_id}, {filter(lambda x: x['id'] == women_id, data_db).__next__()} </h1>")


def alter_posts(requests: HttpRequest, post_id: int) -> HttpResponse:
    return HttpResponse(f"<h3> Отображение статьи c id:{post_id} </h3>")


# @login_required(login_url="/admin")
@login_required
def about(request: HttpRequest) -> HttpResponse:
    contacts_list = Women.published.all()
    paginator = Paginator(contacts_list, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'title': "О сайте",
                                                'page_obj': page_obj
                                                }
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


class ShowCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat
        return self.get_mixin_context(context=context,
                                      title="Категория - " + cat.name,
                                      cat_selected=cat.pk
                                      )


def page_not_found(request: HttpRequest, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    allow_empty = False
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    # fields = ("title", "slug", "content", "is_published", "cat")
    template_name = 'women/addpage.html'
    title_page = "Добавление статьи"

    # login_url = 'admin/'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ("title", "content", "photo", "is_published", "cat")
    template_name = 'women/addpage.html'
    success_url = reverse_lazy("home")
    title_page = "Редактирование статьи"


def contacts(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Обратная связь")


def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Авторизация")


class ShowTag(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs["tag_slug"]).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        return self.get_mixin_context(context=context,
                                      title="Тег - " + tag.tag
                                      )
