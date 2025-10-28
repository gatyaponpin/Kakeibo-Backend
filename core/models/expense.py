from django.db import models
from datetime import date

class Expense(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_group = models.ForeignKey(
        "core.UserGroup",
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="expenses"
    )
    category = models.ForeignKey(
        "core.Category",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="expenses"
    )
    balance_kind = models.SmallIntegerField(default=0)
    balance_name = models.CharField(max_length=20, null=True, blank=True)
    amount = models.IntegerField(default=0)
    memo = models.CharField(max_length=256, null=True, blank=True)
    occur_date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "expenses"
        indexes = [
            models.Index(fields=["user_group"], name="idx_expense_user_group_id"),
            models.Index(fields=["category"], name="idx_expense_category_id"),
            models.Index(fields=["occur_date"], name="idx_expense_occur_date"),
        ]

    def __str__(self):
        return f"{self.occur_date} {self.balance_name or ''} {self.amount}"
