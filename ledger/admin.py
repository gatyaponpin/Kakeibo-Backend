from django.contrib import admin
from .models import Category, Expense, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "balance")
    list_filter = ("balance",)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "name", "amount", "occur_date")
    list_filter = ("type", "occur_date")

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "amount", "memo")