from rest_framework import generics

from api.permissions import get_level_permission
from .serializers import PostSerializer
from ..models import Post


class ListBlogPostsView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [get_level_permission(1)]


class PublishPostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [get_level_permission(2)]


class ListOwnPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [get_level_permission(2)]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class DeletePostView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [get_level_permission(3)]
