from django.forms import ModelForm
from booking.models import *
from users.models import *


class TailorProfileForm(ModelForm):
    class Meta:
        model = Tailors
        fields = ["address", "specialities", "about", "booking_charges", "pictures"]


class UserProfileForm(ModelForm):
    class Meta:
        model = Users
        fields = [
            "first_name",
            "last_name",
            "email",
            "contact",
            "displayPicture",
            "username",
            "gender",
        ]
