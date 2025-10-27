import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from .auth import issue_app_jwt

LINE_VERIFY_URL = "https://api.line.me/oauth2/v2.1/verify"

@method_decorator(csrf_exempt, name='dispatch')
class DevLoginView(APIView):
    authentication_classes = [] 
    permission_classes = [AllowAny]  
    """
    開発用の簡易ログイン: email/username をPOSTすると
    accounts.User を upsert し、アプリJWTを返す
    """
    @transaction.atomic
    def post(self, request):
        email = request.data.get("email")
        username = request.data.get("username") or (email.split("@")[0] if email else "user")
        if not email:
            return Response({"detail":"email is required"}, status=400)
        user, _ = User.objects.get_or_create(email=email, defaults={"username": username, "password": ""})
        token = issue_app_jwt(account_user_id=user.id, email=user.email)
        return Response({"access": token})
    
@method_decorator(csrf_exempt, name='dispatch')
class LineLoginView(APIView):
    """LIFF からの id_token を受け取り、LINEで検証してJWTを返す"""
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        id_token = request.data.get("id_token")
        channel_id = getattr(settings, "LINE_CHANNEL_ID", None)
        if not id_token or not channel_id:
            return Response({"detail": "id_token and LINE_CHANNEL_ID required"}, status=400)

        # LINE公式のverify APIでトークン検証
        res = requests.post(LINE_VERIFY_URL, data={
            "id_token": id_token,
            "client_id": channel_id,
        })
        if res.status_code != 200:
            return Response({"detail": "LINE verify failed", "response": res.text}, status=400)

        payload = res.json()
        line_uid = payload.get("sub")
        email = payload.get("email")
        name = payload.get("name") or "LINE User"

        if not line_uid:
            return Response({"detail": "Invalid LINE response"}, status=400)

        # User Upsert
        user, _ = User.objects.get_or_create(
            email=email or f"{line_uid}@line.local",
            defaults={"username": name, "password": ""}
        )

        token = issue_app_jwt(account_user_id=user.id, email=user.email)
        return Response({"access": token})
    
@method_decorator(csrf_exempt, name='dispatch')
class RefreshTokenView(APIView):
    """リフレッシュトークンから新しいアクセスJWTを再発行"""
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("refresh")
        if not token:
            return Response({"detail": "refresh token required"}, status=400)
        try:
            payload = decode_jwt(token, expected_type="refresh")
        except Exception as e:
            return Response({"detail": str(e)}, status=401)
        uid = payload.get("account_user_id")
        email = payload.get("email")
        tokens = issue_app_jwt(uid, email)
        return Response(tokens, status=200)