from django.db import models
from accounts.models import User, UserGroup, TimeStampedSoftDelete

class Category(TimeStampedSoftDelete):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=100)
    # True: 支出カテゴリ / False: 収入カテゴリ
    balance = models.BooleanField(default=True)
    class Meta:
        db_table = "categories"
        indexes = [models.Index(fields=["user", "user_group"])]

class Expense(TimeStampedSoftDelete):
    INCOME = 1
    EXPENSE = 2
    TYPE_CHOICES = ((INCOME, "INCOME"), (EXPENSE, "EXPENSE"))

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # 収入時はNULL可
    type = models.SmallIntegerField(choices=TYPE_CHOICES)
    name = models.CharField(max_length=20)
    amount = models.IntegerField()
    memo = models.CharField(max_length=256, blank=True)
    occur_date = models.DateField()
    class Meta:
        db_table = "expenses"
        indexes = [
            models.Index(fields=["user", "occur_date"]),
            models.Index(fields=["user_group"]),
            models.Index(fields=["type", "category"]),
        ]

class Budget(TimeStampedSoftDelete):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.IntegerField()
    memo = models.CharField(max_length=256, blank=True)
    class Meta:
        db_table = "budgets"
        indexes = [models.Index(fields=["user","category"])]