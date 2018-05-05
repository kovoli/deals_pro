from django.contrib import admin
from .models import Post, Category, Tag
from imagekit.admin import AdminThumbnail

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'author', 'category', 'status', 'admin_thumbnail')
    search_fields = ['title', 'body']
    ordering = ['status', 'publish']
    list_filter = ('status', 'created', 'publish', 'author')
    date_hierarchy = 'publish'
    filter_horizontal = ('tags',)
    # raw_id_fields = ('author',)
    # prepopulated_fields = {'slug': ('title', )}  # Автоматически пишет slug
    readonly_fields = ('slug',)  # поле только для чтения
    fields = ('title', 'slug', 'body', 'publish', 'status', 'author', 'category', 'tags', 'image') # Очередность полей в админке
    admin_thumbnail = AdminThumbnail(image_field='image_sidebar_blog')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)

    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='image')



admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)