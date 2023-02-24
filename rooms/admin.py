from django.contrib import admin
# Local imports
from .models import Room, Requests

# Register your models here.
admin.site.register(Room)
admin.site.register(Requests)