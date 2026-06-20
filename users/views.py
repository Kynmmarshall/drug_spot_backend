from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
)


def _token_pair(user):
    """Return access + refresh tokens and basic user info."""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "bio": user.bio,
            "avatar_path": user.avatar_path,
            "user_type": user.user_type,
        },
    }


# ─── Register ────────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    POST /api/register
    Body: { username, email, phone, password, user_type, bio?, avatar_path? }
    Returns: { access, refresh, user }
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(_token_pair(user), status=status.HTTP_201_CREATED)


# ─── Login ───────────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    POST /api/login
    Body: { username, password }
    Returns: { access, refresh, user }
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(
        username=serializer.validated_data["username"],
        password=serializer.validated_data["password"],
    )
    if not user:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_active:
        return Response(
            {"error": "Account is disabled"},
            status=status.HTTP_403_FORBIDDEN,
        )

    return Response(_token_pair(user))


# ─── Token Refresh ───────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
def token_refresh(request):
    """
    POST /api/refresh
    Body: { refresh }
    Returns: { access }
    """
    refresh_token = request.data.get("refresh")
    if not refresh_token:
        return Response(
            {"error": "refresh token required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        token = RefreshToken(refresh_token)
        return Response({"access": str(token.access_token)})
    except TokenError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_401_UNAUTHORIZED)


# ─── Logout ──────────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    POST /api/logout
    Body: { refresh }   – blacklists the refresh token (requires simplejwt blacklist app)
    Returns: { success: true }

    If token blacklisting is not enabled the endpoint still returns 200
    so the Flutter client can safely delete its stored tokens.
    """
    refresh_token = request.data.get("refresh")
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            # Blacklist app not installed or token already invalid – ignore
            pass
    return Response({"success": True})


# ─── Profile ─────────────────────────────────────────────────────────────────

@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    GET  /api/profile  → Returns current user profile
    PUT  /api/profile  → Partial update (email, phone, bio, avatar_path)
    """
    if request.method == "GET":
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    serializer = ProfileSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(ProfileSerializer(request.user).data)


# ─── Change Password ──────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    POST /api/change-password
    Body: { old_password, new_password }
    Returns: { success: true }
    """
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user
    if not user.check_password(serializer.validated_data["old_password"]):
        return Response(
            {"error": "Current password is incorrect"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(serializer.validated_data["new_password"])
    user.save()
    # Issue new tokens so the client doesn't get logged out
    return Response({"success": True, **_token_pair(user)})
