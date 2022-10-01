from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from test_app.serializers import *  # pylint: disable=wildcard-import,unused-wildcard-import


class CreateAPIMixin:
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ListRetrieveUpdateDestroyAPIMixin:
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.filter(author=self.request.user)


class PostCreateAPIView(CreateAPIMixin, CreateAPIView):
    serializer_class = PostSerializer


class PostRetrieveUpdateDestroyAPIView(
    ListRetrieveUpdateDestroyAPIMixin, RetrieveUpdateDestroyAPIView
):
    serializer_class = PostSerializer


class PostListAPIView(ListRetrieveUpdateDestroyAPIMixin, ListAPIView):
    serializer_class = PostListSerializer


class CommentCreateAPIView(CreateAPIMixin, CreateAPIView):
    serializer_class = CommentSerializer


class CommentRetrieveUpdateDestroyAPIView(
    ListRetrieveUpdateDestroyAPIMixin, RetrieveUpdateDestroyAPIView
):
    serializer_class = CommentSerializer
