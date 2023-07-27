from django.contrib import admin
from .models import Lesson, RecordsLesson

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'track', 'lesson_format',
        'lesson_date', 'lesson_time', 'theme',
        'status', 'audience', 'teacher', 'place', 
        'required_items', 'count_seats'
    )
    list_filter = (
        'track',
    )

    search_fields = (
        'theme', 'name'
    )
    

@admin.register(RecordsLesson)
class RecordsLessonAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'lesson', 'user'
    )