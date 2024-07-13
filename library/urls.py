from . import views
from django.urls import path

app_name = 'library'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about-page'),

    path('return_book/<int:pk>', views.return_book, name='return_book'),
    path('borrow_book/<int:pk>', views.borrow_book, name='borrow_book'),
    path('show_books', views.show_books, name='show_books'),
    path('borrowed_books', views.borrowed_books, name='borrowed_books'),


    path('add_book', views.add_book, name='add_book'),
    path('written_books', views.written_books, name='written_books'),
    path('edit_book/<int:pk>', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>', views.delete_book, name='delete_book'),
]
