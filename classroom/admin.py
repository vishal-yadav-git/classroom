from django.contrib import admin
from .models import Lecture, SlideBanner, Franchisee, Filter, Course, Faculty
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'phone', 'occupation', 'course', 'wallet_balance')}),
        (_('User Type'), {'fields': ('user_type',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'occupation', 'course', 'user_type', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(CustomUser, CustomUserAdmin)


class PublishActionMixin:
    def mark_as_published(self, request, queryset):
        queryset.update(is_published=True)
    mark_as_published.short_description = "Show on Frontend"

    def mark_as_unpublished(self, request, queryset):
        queryset.update(is_published=False)
    mark_as_unpublished.short_description = "Hide from Frontend"

    actions = ['mark_as_published', 'mark_as_unpublished']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']

class LectureAdmin(PublishActionMixin, admin.ModelAdmin):
    list_display = ('title', 'faculty', 'total_price', 'price', 'is_published', 'show_on_homepage', 'pub_date')
    fields = ('image', 'title', 'faculty', 'course',  'description', 'total_price', 'price', 'is_published', 'show_on_homepage')
    readonly_fields = ('pub_date',)
  
admin.site.register(Lecture, LectureAdmin)


class FacultyAdmin(PublishActionMixin, admin.ModelAdmin):
    list_display = ('name', 'institute', 'is_published', 'show_on_homepage', 'pub_date')
    fields = ['image', 'name', 'institute', 'pub_date','is_published', 'show_on_homepage']
    readonly_fields = ('pub_date',) 

admin.site.register(Faculty, FacultyAdmin)


class SlideBannerAdmin(PublishActionMixin, admin.ModelAdmin):
    list_display = ('title', 'description', 'is_published', 'pub_date')
    fields = ['image', 'title', 'description', 'pub_date','is_published']
    readonly_fields = ('pub_date',) 

admin.site.register(SlideBanner,SlideBannerAdmin)


class FranchiseeAdmin(PublishActionMixin, admin.ModelAdmin):
    list_display = ('name', 'is_published')
    fields = ['image', 'name', 'is_published']

admin.site.register(Franchisee,FranchiseeAdmin)


class FilterAdmin(PublishActionMixin, admin.ModelAdmin):
    list_display = ('faculty', 'subject', 'course', 'is_published')
    fields = ['faculty', 'subject', 'course', 'price', 'is_published']

admin.site.register(Filter,FilterAdmin)
