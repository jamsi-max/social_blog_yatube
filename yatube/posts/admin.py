from django.contrib import admin

from .models import Comment, Follow, Group, Ip, Like, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
        'image',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'description',
    )
    search_fields = ('description',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'post',
        'author',
        'text',
        'created',
    )
    list_editable = ('author', 'text',)
    search_fields = ('text', 'author__username',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author',
        'created',
    )
    list_editable = ('user', 'author')
    search_fields = ('user__username', 'author__username',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'

class IpAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ip',
        'post_views',
        'created',
    )
    search_fields = ('ip',)
    list_filter = ('ip',)
    empty_value_display = '-пусто-'

class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'like',
        'user',
        'created',
    )
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'

admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Ip, IpAdmin)
admin.site.register(Like, LikeAdmin)
