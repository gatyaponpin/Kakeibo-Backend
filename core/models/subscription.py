from django.db import models

class Subscription(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_group = models.ForeignKey(
        "core.UserGroup",
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="subscriptions"
    )
    category = models.ForeignKey(
        "core.Category",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="subscriptions"
    )
    balance_kind = models.SmallIntegerField(default=0)
    balance_name = models.CharField(max_length=20, null=True, blank=True)
    billing_day = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "subscriptions"
        indexes = [
            models.Index(fields=["user_group"], name="idx_subscription_user_group_id"),
            models.Index(fields=["category"], name="idx_subscription_category_id"),
        ]

    def __str__(self):
        return self.balance_name or f"subscription:{self.pk}"
