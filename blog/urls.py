from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='posts'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='post-create'),
    path('post/edit/<int:id>/', views.edit_post, name='post-edit'),
    path('post/delete/<int:id>/', views.delete_post, name='post-delete'),
    path('comment/delete/<int:id>/', views.delete_comment, name='comment-delete'),
    path('comment/edit/<int:id>/', views.edit_comment, name='comment-edit'),
]
