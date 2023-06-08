from django.contrib import admin

from .models import Comment, Review, Title

admin.site.register(Title)
admin.site.register(Comment)
admin.site.register(Review)
