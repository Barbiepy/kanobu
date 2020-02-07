from django.contrib import admin

from vote.models import News, Article, Comment, Vote

admin.site.register(News)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Vote)
