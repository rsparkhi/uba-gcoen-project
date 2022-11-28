from random import choices
from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

GENDERS = [("M", "Male"), ("F", "Female"), ("O", "Other")]


class Users(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    gender = models.CharField(max_length=1, choices=GENDERS)
    contact = models.CharField(max_length=10, blank=True, null=True)
    isTailor = models.BooleanField(default=False)
    displayPicture = models.ImageField(upload_to="user-images", null=True)

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.username

    def as_dict(self):
        return self.__dict__


class Tailors(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.DO_NOTHING)
    address = models.TextField(blank=True, null=True)
    specialities = ArrayField(models.CharField(max_length=255, blank=True, null=True))
    about = models.TextField(blank=True, null=True)
    booking_charges = models.FloatField(blank=True, null=True)

    pictures = ArrayField(
        models.ImageField(upload_to="tailor-pictures", blank=True, null=True),
        blank=True,
        null=True,
    )
    ratings = ArrayField(models.JSONField(blank=True, null=True), blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tailors"

    def __str__(self) -> str:
        return self.user.username

    def as_dict(self):
        return self.__dict__
