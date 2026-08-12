from django.urls import path

from .views import SecurityReviewView, health_check

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("security/review/", SecurityReviewView.as_view(), name="security-review"),
]
