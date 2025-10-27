from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ledger.views import CategoryViewSet, ExpenseViewSet, BudgetViewSet
from django.http import HttpResponse
from accounts.views import DevLoginView, LineLoginView, RefreshTokenView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'budgets', BudgetViewSet, basename='budget')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/dev-login", DevLoginView.as_view()),
    path("api/auth/line-login", LineLoginView.as_view()), 
    path("api/auth/refresh", RefreshTokenView.as_view()),
]