from django.contrib import admin
from django.urls import path
from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", core_views.health),
    path("me/", core_views.me),
]