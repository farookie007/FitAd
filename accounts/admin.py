from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = [
        'email',
        'username',
        'is_staff',
    ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': (
            ),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': (
                'email',
                'first_name',
                'last_name',
            )
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
