from django.contrib import admin
from .models import Category, Product, CartProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]
    list_display_links = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["pk", "category", "name", "price", "status"]
    list_display_links = ["name"]
    search_fields = ["name"]
    list_filter = ["category", "status", "created_at", "updated_at"]
    date_hierarchy = "updated_at"
    actions = ["make_active"]

    @admin.display(description=f"지정된 상품을 {Product.Status.ACTIVE.label} 상태로 변경")
    def make_active(self, request, queryset):
        count = queryset.update(status=Product.Status.ACTIVE)
        self.message_user(
            request, f"{count}개의 상품을 {Product.Status.ACTIVE.label} 상태로 변경 완료"
        )


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity"]
    list_display_links = ["product"]
