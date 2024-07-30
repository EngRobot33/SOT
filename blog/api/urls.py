from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('posts/', views.ListBlogPostsView.as_view(), name='list-blog-posts'),
    path('posts/publish/', views.PublishPostView.as_view(), name='publish-post'),
    path('posts/current-user/', views.ListOwnPostsView.as_view(), name='list-own-posts'),
    path('posts/delete/<int:pk>/', views.DeletePostView.as_view(), name='delete-post'),
]
