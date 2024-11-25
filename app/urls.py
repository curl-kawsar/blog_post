from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('request-author/', views.request_author, name='request_author'),
    path('profile/', views.profile, name='profile'),
    path('create-post/', views.create_post, name='create_post'),
    path('edit-post/<int:id>/', views.edit_post, name='edit_post'),
    path('delete-post/<int:id>/', views.delete_post, name='delete_post'),
    path('search/', views.search_posts, name='search_posts'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
]