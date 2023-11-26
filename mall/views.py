from django.shortcuts import render
from django.views.generic import ListView

from mall.models import Product


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
    queryset = Product.objects.all().select_related("category")
    template_name = "mall/product_list.html"
    context_object_name = "product_list"
    paginate_by = 4


product_list = ProductListView.as_view()
