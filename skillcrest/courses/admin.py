from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'duration', 'is_active', 'trainer')
    list_filter = ('category', 'level', 'is_active')
    search_fields = ('title',)


