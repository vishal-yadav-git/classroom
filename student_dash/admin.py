from django.contrib import admin
from .models import Lecture, Playlist, LectureAccess, LectureNote

# Register your models here.

class PublishActionMixin:
    def mark_as_published(self, request, queryset):
        queryset.update(is_published=True)
    mark_as_published.short_description = "Show on Frontend"

    def mark_as_unpublished(self, request, queryset):
        queryset.update(is_published=False)
    mark_as_unpublished.short_description = "Hide from Frontend"

    actions = ['mark_as_published', 'mark_as_unpublished']


class LectureNoteInline(admin.TabularInline):
    model = LectureNote
    extra = 1  # number of empty forms shown

class LectureAdmin(PublishActionMixin, admin.ModelAdmin):
    list_display = ('title', 'playlist', 'is_published', 'pub_date')
    fields = ('title', 'playlist', 'youtube_url', 'description', 'is_published', 'pub_date')
    search_fields = ('title',)
    readonly_fields = ('pub_date',)
    list_filter = ('playlist', 'is_published')
    inlines = [LectureNoteInline]

admin.site.register(Lecture,LectureAdmin)

class PlaylistAdmin(PublishActionMixin, admin.ModelAdmin):
    list_display = ('name', 'is_published')  
    fields = ('name', 'image','description', 'is_published')
    search_fields = ('name',)
    list_filter = ('is_published',)

admin.site.register(Playlist, PlaylistAdmin)