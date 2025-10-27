from datetime import date
from calendar import monthrange
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Category, Expense, Budget
from .serializers import CategorySerializer, ExpenseSerializer, BudgetSerializer

def month_bounds(yyyy_mm: str):
    """'2025-10' → (2025-10-01, 2025-11-01) のように期間を返す"""
    y, m = map(int, yyyy_mm.split("-"))
    last = monthrange(y, m)[1]
    start = date(y, m, 1)
    if m == 12:
        end = date(y + 1, 1, 1)
    else:
        end = date(y, m + 1, 1)
    return start, end

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("id")
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        qs = Expense.objects.filter(user_id=self.request.user.id).order_by("-occur_date","-id")
        # 既存の month/type フィルタはこのまま
        month = self.request.query_params.get("month")
        t = self.request.query_params.get("type")
        if month:
            start, end = month_bounds(month); qs = qs.filter(occur_date__gte=start, occur_date__lt=end)
        if t in ("1","2"):
            qs = qs.filter(type=int(t))
        return qs

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    def get_queryset(self):
        return Budget.objects.filter(user_id=self.request.user.id).order_by("-id")
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
