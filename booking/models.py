from django.db import models

from users.models import Users, Tailors


class Booking(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    charges = models.FloatField(blank=True, null=True)
    balance = models.FloatField(default=0)
    purpose = models.CharField(max_length=255, blank=True, null=True)
    booked_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    state = models.IntegerField(default=1)
    status = models.CharField(max_length=255, default="requested")

    tailor = models.ForeignKey(
        Tailors, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    client = models.ForeignKey(
        Users, on_delete=models.DO_NOTHING, blank=True, null=True
    )

    client_address = models.CharField(max_length=255, blank=True, null=True)
    client_contact = models.CharField(max_length=255, blank=True, null=True)

    reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "bookings"
