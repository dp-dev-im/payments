from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from mall.forms import CartProductForm
from mall.models import Product, CartProduct, Order


# Create your views here.
# def product_list(request):
#     product_qs = Product.objects.all().select_related("category")
#     return render(
#         request,
#         "mall/product_list.html",
#         {
#             "product_list": product_qs,
#         },
#     )


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.filter(status=Product.Status.ACTIVE).select_related(
        "category"
    )
    template_name = "mall/product_list.html"
    context_object_name = "product_list"
    paginate_by = 4


product_list = ProductListView.as_view()


@login_required
@require_POST
def add_to_cart(request, product_pk):
    product_qs = Product.objects.filter(
        status=Product.Status.ACTIVE,
    )
    product = get_object_or_404(product_qs, pk=product_pk)

    quantify = int(request.GET.get("quantity", 1))

    cart_product, is_created = CartProduct.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": quantify},
    )

    if not is_created:
        cart_product.quantity += quantify
        cart_product.save()

    return HttpResponse("ok")


@login_required
def cart_detail(request):
    cart_product_qs = (
        CartProduct.objects.filter(
            user=request.user,
        )
        .select_related("product")
        .order_by("product__name")
    )

    CartProductFormSet = modelformset_factory(
        model=CartProduct, form=CartProductForm, can_delete=True, extra=0
    )

    if request.method == "POST":
        formset = CartProductFormSet(
            data=request.POST,
            queryset=cart_product_qs,
        )
        if formset.is_valid():
            formset.save()
            messages.success(request, "updated cart")
            return redirect("cart_detail")
    else:
        formset = CartProductFormSet(
            queryset=cart_product_qs,
        )

    return render(
        request,
        "mall/cart_detail.html",
        {
            "formset": formset,
        },
    )


@login_required()
def order_new(request):
    cart_product_qs = CartProduct.objects.filter(user=request.user)

    order = Order.create_form_cart(request.user, cart_product_qs)
    cart_product_qs.delete()

    return redirect("order_pay", order.pk)


@login_required()
def order_pay(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    return render(
        request,
        "mall/order_pay.html",
        {
            "order": order,
        },
    )
