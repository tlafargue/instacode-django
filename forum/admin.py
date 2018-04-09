from django.contrib import admin
from .models import Forum, Topic, Post, ProfaneWord

class ForumAdmin(admin.ModelAdmin):
    list_display = ["title", "categorie", "creator", "created"]
    list_filter = ["title", "creator"]

class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "forum", "creator", "created"]
    list_filter = ["forum", "creator"]

class PostAdmin(admin.ModelAdmin):
    search_fields = [ "creator"]
    list_display = [ "topic", "creator", "created"]

class ProfaneWordAdmin(admin.ModelAdmin):
    pass

admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(ProfaneWord, ProfaneWordAdmin)
