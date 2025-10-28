from django.urls import path
from core import views as core_views
from core.views import demo_user 

urlpatterns = [
    path("api/demo/user", demo_user), 
]