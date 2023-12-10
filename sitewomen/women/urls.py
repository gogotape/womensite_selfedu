from django.urls import path, register_converter, include
from . import views
from . import converters
from .views import AddPage, WomenHomePage, ShowCategory, ShowTag

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', WomenHomePage.as_view(), name='home'),
    path('cats/<int:cat_id>/', views.categories, name='cats_id'),
    path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'),
    path(r'archive/<year4:year>/', views.archive, name='archive'),
    path('about/', views.about, name='about'),
    path('posts/<int:women_id>/', views.posts, name='posts'),
    path('alter_posts/<int:post_id>/', views.alter_posts, name='alter_posts'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contacts/', views.contacts, name='contacts'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='show_post'),
    path('login/', views.login, name='login'),
    path('category/<slug:cat_slug>/', ShowCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', ShowTag.as_view(), name='tag'),
    path('edit/<int:pk>', views.UpdatePage.as_view(), name='edit_page')

]
