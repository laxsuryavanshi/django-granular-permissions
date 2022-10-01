from rest_framework.serializers import ModelSerializer

from test_app.models import Comment, Post


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostSerializer(PostListSerializer):
    comments = CommentSerializer(many=True, read_only=True)
