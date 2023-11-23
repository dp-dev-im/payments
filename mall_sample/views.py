from django.shortcuts import render


def payment_request(request):
    return render(request, "mall_sample/payment_form.html")
