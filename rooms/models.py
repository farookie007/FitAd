import string
import random
from django.db import models
from django.contrib.auth import get_user_model



def generate_code(length=6):
    """
    Generates and returns a code of `length` numbers
    which is a mixture of uppercase letters and digits.
    Params:
        :params length: the length of the code required.

    Returns:
        : the code as a string
    """
    seq = string.ascii_uppercase + string.digits
    while True:
        code = "".join(random.choices(seq, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break
    return code


class Room(models.Model):
    title = models.CharField(max_length=20, unique=False)
    code = models.CharField(max_length=10, default=generate_code, unique=True)
    host = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="rooms")


class Member(models.Model):
    username = models.CharField(max_length=20, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="members")
    room_code = models.CharField(max_length=10)
