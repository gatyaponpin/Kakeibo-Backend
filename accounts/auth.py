import os, jwt, datetime
from typing import Optional
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

APP_SECRET = os.getenv("APP_JWT_SECRET", "dev-secret")
ACCESS_MIN = int(os.getenv("APP_JWT_EXPIRES_MIN", "60")) 
REFRESH_DAYS = int(os.getenv("APP_REFRESH_EXPIRES_DAYS", "7"))

class SimpleUser:
    """Django User互換の軽量オブジェクト（DBクエリ無し）"""
    def __init__(self, account_user_id: int, email: Optional[str] = None):
        self.id = account_user_id
        self.email = email
        self.is_authenticated = True
    def __str__(self): return f"AccountUser<{self.id}>"

def issue_app_jwt(account_user_id: int, email=None):
    now = timezone.now()
    access_payload = {
        "sub": str(account_user_id),
        "account_user_id": account_user_id,
        "email": email,
        "iat": int(now.timestamp()),
        "exp": int((now + datetime.timedelta(minutes=ACCESS_MIN)).timestamp()),
        "type": "access",
    }
    refresh_payload = {
        "sub": str(account_user_id),
        "account_user_id": account_user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + datetime.timedelta(days=REFRESH_DAYS)).timestamp()),
        "type": "refresh",
    }
    return {
        "access": jwt.encode(access_payload, APP_SECRET, algorithm="HS256"),
        "refresh": jwt.encode(refresh_payload, APP_SECRET, algorithm="HS256"),
    }

def decode_jwt(token, expected_type="access"):
    try:
        payload = jwt.decode(token, APP_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed("Token expired")
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed("Invalid token")
    if payload.get("type") != expected_type:
        raise exceptions.AuthenticationFailed("Invalid token type")
    return payload


class AppJWTAuthentication(BaseAuthentication):
    keyword = "Bearer"
    def authenticate(self, request):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith(self.keyword + " "):
            return None
        token = auth.split(" ", 1)[1].strip()
        payload = decode_jwt(token, expected_type="access")
        return (SimpleUser(payload["account_user_id"], payload.get("email")), payload)