from rest_framework import serializers

from user.api.serializers import UserSerializer
from ..models import Post


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'created_at', 'updated_at')
        read_only_fields = ('author', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        return Post.objects.create(author=user, **validated_data)
