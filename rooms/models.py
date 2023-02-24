import string
import random
from django.db import models
from django.urls import reverse


def generate_code(length=6):
    """Generates and returns a code of length `length`
    which is a mixture of uppercase letters and digits.
    
    Args:
        length(int): the length of the code required.
        
    Returns:
        (str): the code as a string.
    """
    seq = string.ascii_uppercase + string.digits
    while True:
        code = "".join(random.choices(seq, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break
    return code


class Room(models.Model):
    """A model representation of a room."""
    code = models.CharField(max_length=8, default=generate_code, unique=True)
    host = models.CharField(max_length=255, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("rooms:display_room", args=[self.pk, self.code])


class Requests(models.Model):
    song_title = models.CharField(max_length=255)
    artiste = models.CharField(max_length=255)
    sender_ID = models.CharField(max_length=255)
    # sender_IP = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="user_requests")
    timestamp = models.DateTimeField(auto_now_add=True)

