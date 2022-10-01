from django.contrib import admin

from test_app.models import Comment, Post

admin.site.register([Comment, Post])
