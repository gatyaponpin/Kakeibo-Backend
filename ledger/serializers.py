from rest_framework import serializers
from .models import Category, Expense, Budget

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "__all__"
    def validate(self, attrs):
        t = attrs.get("type", getattr(self.instance, "type", None))
        category = attrs.get("category", getattr(self.instance, "category", None))
        if t == Expense.EXPENSE and category is None:
            raise serializers.ValidationError("支出のときは category を指定してください。")
        return attrs

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = "__all__"
