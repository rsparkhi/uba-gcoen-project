import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, DetailView
from users.models import *
from booking.models import *
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import *


class up(TemplateView):
    template_name = "user_profile.html"


class tp(TemplateView):
    template_name = "tailor_profile.html"


class Home(TemplateView):
    template_name = "home.html"
    context_object_name = "user"

    def get_queryset(self):
        return Users.objects.filter(user=self.request.user)


class Bookings(TemplateView):
    template_name = "bookings.html"
    extra_context = {"tailors": Tailors.objects.all()}


class TailorView(DetailView):

    model = Tailors
    template_name = "tailor.html"
    context_object_name = "tailor"

    work_hours = range(9, 21)

    extra_context = {"work_hours": work_hours}

    def get_object(self, queryset=None):
        return Tailors.objects.get(user__username=self.kwargs.get("username"))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        request = self.request
        tailor = Tailors.objects.get(user__username=self.kwargs.get("username"))
        user = Users.objects.get(pk=2)
        booking = Booking.objects.create(
            date=request.POST.get("date"),
            time=request.POST.get("hours") + ":" + request.POST.get("mins"),
            charges=tailor.booking_charges,
            balance=tailor.booking_charges,
            tailor=tailor,
            client=user,
            # client=request.user,
            client_address=request.POST.get("address"),
            client_contact="123456789",
            purpose=request.POST.get("purpose"),
        )
        # request.user.get("contact") or

        return redirect("home")


class TailorApproval(TemplateView):
    template_name = "tailor_approval.html"


@csrf_exempt
def CheckAvailability(request):
    data = json.loads(request.body.decode("utf-8"))
    date = data.get("date")
    hour = int(data.get("hours"))
    mins = int(data.get("mins"))
    tusername = data.get("tailor")

    qs = Booking.objects.filter(
        date=date, time__hour=hour, tailor__user__username=tusername
    )

    if qs.exists():
        return JsonResponse({"result": False})
    return JsonResponse({"result": True})


# @login_required
def TailorProfile(request):

    if request.method == "POST":
        data = request.POST
        tailor = Tailors.objects.get(user=request.user)
        form = TailorProfileForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return HttpResponseBadRequest(form.errors)

        tailor.user.first_name = data.get("first_name")
        tailor.user.last_name = data.get("last_name")
        tailor.user.contact = data.get("contact")
        tailor.user.save()
        tailor.save()

    # Requested, Accepted ongoing, history

    requested = Booking.objects.filter(
        state=1, status="requested", tailor__user=request.user
    )

    ongoing = Booking.objects.filter(
        state=2, status="ongoing", tailor__user=request.user
    )

    history = Booking.objects.filter(
        state=3, status="completed", tailor__user=request.user
    )

    context = {"requested": requested, "ongoing": ongoing, "history": history}

    return render(request, "tailor_profile.html", context=context)


# @login_required
def Userprofile(request):

    if request.method == "POST":

        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return HttpResponseBadRequest(form.errors)

    still_pending = Booking.objects.filter(
        client=request.user, state=1, status="requested"
    )
    accepted = Booking.objects.filter(client=request.user, state=2, status="accepted")
    history = Booking.objects.filter(client=request.user, state=3, status="completed")
    rejected = Booking.objects.filter(client=request.user, state=4, status="rejected")

    context = {
        "pending": still_pending,
        "accepted": accepted,
        "history": history,
        "rejected": rejected,
    }

    return render(request, "user_profile.html", context=context)


@login_required
def acceptView(request, bookingId):
    booking = Booking.objects.get(id=bookingId)

    if booking.tailor.user.username == request.user.username:
        booking.state = 2
        booking.status = "accepted"
        booking.save()
        return JsonResponse({"result": True})

    else:
        return JsonResponse({"result": False})


# @login_required
def rejectView(request, bookingId):
    booking = Booking.objects.get(id=bookingId)

    if booking.tailor.user.username == request.user.username:
        booking.state = 4
        booking.status = "rejected"
        booking.reason = request.GET.get("reason")
        booking.save()
        return JsonResponse({"result": True})

    else:
        return JsonResponse({"result": False})


@transaction.atomic
def registerUser(request):
    form = UserProfileForm(request.POST, request.FILES)
    return render(request, "user-register.html", {"form": form})
