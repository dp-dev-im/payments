from django.core.validators import MinValueValidator
from django.db import models


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
