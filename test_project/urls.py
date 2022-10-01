from django.contrib import admin
from django.urls import path

from test_app.views import *  # pylint: disable=wildcard-import,unused-wildcard-import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/post', PostCreateAPIView.as_view()),
    path('api/post/<int:pk>', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('api/posts', PostListAPIView.as_view()),
    path('api/comment', CommentCreateAPIView.as_view()),
    path('api/comment/<int:pk>', CommentRetrieveUpdateDestroyAPIView.as_view()),
]
