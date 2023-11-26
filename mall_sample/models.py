import logging
from uuid import uuid4

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.http import Http404
from iamport import Iamport


logger = logging.getLogger("portone")


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        READY = "ready", "미결제"
        PAID = "paid", "결제완료"
        CANCELLED = "cancelled", "결제취소"
        FAILED = "failed", "결제실패"

    uid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=50)
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="give me the money(than 1)"),
        ]
    )
    # ready, paid, cancelled, failed
    status = models.CharField(
        max_length=10,
        default=StatusChoices.READY,
        choices=StatusChoices.choices,
        db_index=True,
    )
    is_paid_ok = models.BooleanField(default=False, editable=False, db_index=True)

    @property
    def merchant_uid(self):
        return str(self.uid)

    def portone_check(self, commit=True):
        api = Iamport(
            imp_key=settings.PORTONE_API_KEY, imp_secret=settings.PORTONE_API_SECRET
        )

        print(api)
        try:
            meta = api.find(merchant_uid=self.merchant_uid)
        except (Iamport.ResponseError, Iamport.HttpError) as e:
            logger.error(str(e), exc_info=e)
            raise Http404(str(e))

        print(meta["status"])
        print(meta["amount"])

        self.status = meta["status"]
        self.is_paid_ok = meta["status"] == "paid" and meta["amount"] == self.amount

        if commit:
            self.save()
