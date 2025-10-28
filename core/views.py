# core/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from core.models import User
from core.serializers.user import SimpleUserSerializer

@api_view(["GET"])
@permission_classes([AllowAny])   # 疎通確認なので無条件許可
def demo_user(request):
    user = User.objects.order_by("id").first()
    if not user:
        return Response({"detail": "no user exists"}, status=404)
    print(SimpleUserSerializer(user).data)
    return Response(SimpleUserSerializer(user).data)
