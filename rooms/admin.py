from django.contrib import admin
# Local imports
from .models import Room, Request

# Register your models here.
admin.site.register(Room)
admin.site.register(Request)