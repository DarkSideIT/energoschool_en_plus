from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'status',
        'last_name', 'first_name',
        'score', 'phone', 'educational_institution',
        'class_number'
    )

    list_filter = (
        'is_staff',
    )

    search_fields = (
        'last_name', 'username'
    )