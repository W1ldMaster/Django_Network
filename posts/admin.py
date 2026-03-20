from django.contrib import admin
from .models import Post, Group

# Register your models here.
admin.site.register(Group)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'created_at',
        'author',
        'group',
    )
    list_editable = ('group', )
    search_fields = ('text', )
    list_filter = ('created_at', )
    empty_value_display = '-пусто-'

