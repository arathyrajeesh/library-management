from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='login'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('book-list/', views.book_list, name='all-book'),
    path('add-book/', views.add_book, name='add-book'),
    path('delete-book/<int:book_id>/', views.delete_book, name='delete-book'),
]
