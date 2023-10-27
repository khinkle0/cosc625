from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='posts'),
    path('post/<int:id>', views.post_detail, name='post_detail'),
    path('post/create', views.create_post, name='post-create'),
]
