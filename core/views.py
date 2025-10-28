from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def health(request):
    return JsonResponse({"status": "ok"})

@login_required
def me(request):
    user = request.user
    return JsonResponse({"id": user.id, "username": user.username})