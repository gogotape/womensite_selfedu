from django.urls import path, register_converter
from . import views
from . import converters


register_converter(converters.FourDigitYearConverter, "year4")


urlpatterns = [
    path('', views.index, name='home'),
    path('cats/<int:cat_id>/', views.categories, name='cats_id'),
    path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),
    path(r'archive/<year4:year>/', views.archive, name='archive'),
    path('about/', views.about, name='about'),
    path('posts/<int:women_id>/', views.posts, name='posts'),
    path('alter_posts/<int:post_id>/', views.alter_posts, name='alter_posts'),
    path('addpage/', views.addpage, name='add_page'),
    path('contacts/', views.contacts, name='contacts'),
    path('post/<slug:post_slug>/', views.show_post, name='show_post'),
    path('login/', views.login, name='login'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
]