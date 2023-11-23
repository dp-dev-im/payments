from django.urls import path
from . import views


urlpatterns = [
    path("payment/request/", views.payment_request, name="payment_request"),
    path("payment/<int:pk>/pay/", views.payment_pay, name="payment_pay"),
    path("payment/<int:pk>/check/", views.payment_check, name="payment_check"),
]
