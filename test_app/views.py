from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from granular_permissions.mixins import GranularPermissionMixin
from test_app.models import *  # pylint: disable=wildcard-import,unused-wildcard-import
from test_app.serializers import *  # pylint: disable=wildcard-import,unused-wildcard-import


class CreateAPIMixin:
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RetrieveUpdateDestroyAPIMixin:
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.model_class.objects.all()


class PostCreateAPIView(CreateAPIMixin, CreateAPIView):
    serializer_class = PostSerializer


class PostRetrieveUpdateDestroyAPIView(
    GranularPermissionMixin, RetrieveUpdateDestroyAPIMixin, RetrieveUpdateDestroyAPIView
):
    model_class = Post


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()


class CommentCreateAPIView(CreateAPIMixin, CreateAPIView):
    serializer_class = CommentSerializer


class CommentRetrieveUpdateDestroyAPIView(
    GranularPermissionMixin, RetrieveUpdateDestroyAPIMixin, RetrieveUpdateDestroyAPIView
):
    model_class = Comment
