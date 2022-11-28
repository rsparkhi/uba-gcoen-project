from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("bookings/", views.Bookings.as_view(), name="bookings"),
    # path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("tailors/<slug:username>", views.TailorView.as_view()),
    path("check-availability/", views.CheckAvailability),
    path("user-profile", views.up.as_view(), name="user-profile"),
    path("tailor-profile", views.tp.as_view(), name="tailor-profile"),
    path("user-register/", views.registerUser),
]
