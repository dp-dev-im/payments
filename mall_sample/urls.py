from django.urls import path
from . import views


urlpatterns = [
    path("payment/request/", views.payment_request, name="payment_request"),
]
