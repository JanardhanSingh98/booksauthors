from django.urls import path
from . import views

urlpatterns = [
    path('books', views.BooksListApi.as_view(), name='books'),
    path('books/details', views.BookDetailsApi.as_view(), name='books'),
    path('authors', views.AuthorListApi.as_view(), name='authors'),
]
