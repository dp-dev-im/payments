from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint, QuerySet

from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "product categorization"


class Product(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "a", "정상"
        SOLD_OUT = "s", "품절"
        OBSOLETE = "o", "단종"
        INACTIVE = "i", "비활성화"

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_constraint=False,
    )

    name = models.CharField(max_length=80, db_index=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(
        validators=[MinValueValidator(100, message="minimum: 100")]
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.INACTIVE,
    )
    photo = models.ImageField(upload_to="mall/product/photo/%Y/%m/%d/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<{self.pk}> {self.name}"

    class Meta:
        verbose_name = verbose_name_plural = "product"
        ordering = ["-pk"]


class CartProduct(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name="cart_product_set",
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_product_set"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
        ],
    )

    def __str__(self):
        return f"<{self.pk}> {self.product.name}: {self.quantity}"

    @property
    def amount(self) -> int:
        return self.product.price * self.quantity

    class Meta:
        verbose_name = verbose_name_plural = "cart product"
        constraints = [
            UniqueConstraint(fields=["user", "product"], name="unique_user_and_product")
        ]


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        REQUESTED = "requested", "주문요청"
        FAILED_PAYMENT = "failed_payment", "결제실패"
        PAID = "paid", "결제 완료"
        PREPARED_PRODUCT = "prepared_product", "상품준비중"
        SHIPPED = "shipped", "배송중"
        DELIVERED = "delivered", "배송완료"
        CANCELED = "canceled", "주문취소"

    uid = models.UUIDField(default=uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    total_amount = models.PositiveIntegerField("결제금액")
    status = models.CharField(
        "진행상태",
        max_length=18,
        choices=StatusChoices.choices,
        default=StatusChoices.REQUESTED,
        db_index=True,
    )
    product_set = models.ManyToManyField(
        Product,
        through="OrderedProduct",
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_form_cart(
        cls, user: User, cart_product_qs: QuerySet[CartProduct]
    ) -> "Order":
        # 캐싱
        cart_product_list = list(cart_product_qs)

        total_amount = sum(cart_product.amount for cart_product in cart_product_list)
        print(total_amount)

        order = cls.objects.create(user=user, total_amount=total_amount)

        order_product_list = []
        for cart_product in cart_product_list:
            product = cart_product.product
            ordered_product = OrderedProduct(
                order=order,
                product=product,
                name=product.name,
                price=product.price,
                quantity=cart_product.quantity,
            )
            order_product_list.append(ordered_product)
        OrderedProduct.objects.bulk_create(order_product_list)

        return order


class OrderedProduct(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    name = models.CharField("상품명", max_length=90, help_text="주문 시점 상품명 저장")
    price = models.PositiveIntegerField(
        "상품가격",
        help_text="주문 시점 상품 가격",
        validators=[MinValueValidator(100, message="minimum: 100")],
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="1")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
