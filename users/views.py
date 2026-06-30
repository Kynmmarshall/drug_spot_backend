from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django.utils import timezone

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
)
from .email_utils import send_verification_email


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
            "is_email_verified": user.is_email_verified,
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

    After registration the account is created but is_email_verified=False.
    A verification OTP is sent automatically to the provided email.
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    # Fire verification email – non-blocking (we still return 201 even if it fails)
    email_sent = send_verification_email(user)

    data = _token_pair(user)
    data["email_sent"] = email_sent
    return Response(data, status=status.HTTP_201_CREATED)


# ─── Login ───────────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    POST /api/login
    Body: { username, password }
    Returns: { access, refresh, user }

    If the account's email is not yet verified the response still succeeds
    but user.is_email_verified will be False so the Flutter app can redirect
    to the verification screen.
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


# ─── Send / Resend Verification Email ────────────────────────────────────────

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_verification(request):
    """
    POST /api/send-verification
    Requires: Bearer token (user must be logged in)

    Generates a new OTP and sends a verification email.
    Returns: { success: true, email: "...@..." }
    """
    user = request.user

    if user.is_email_verified:
        return Response(
            {"error": "Email is already verified"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not user.email:
        return Response(
            {"error": "No email address associated with this account"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    sent = send_verification_email(user)
    if not sent:
        return Response(
            {"error": "Failed to send verification email. Please try again later."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # Mask the email for privacy: e.g. j***@example.com
    parts = user.email.split("@")
    masked = parts[0][0] + "***@" + parts[1] if len(parts) == 2 else user.email

    return Response({"success": True, "email": masked})


# ─── Verify Email ─────────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_email(request):
    """
    POST /api/verify-email
    Body: { otp: "123456" }
    Requires: Bearer token

    Returns: { success: true, user: { ..., is_email_verified: true } }
    """
    user = request.user

    if user.is_email_verified:
        return Response(
            {"error": "Email is already verified"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    otp = request.data.get("otp", "").strip()
    if not otp:
        return Response(
            {"error": "OTP is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check expiry
    if not user.email_otp_expires_at or timezone.now() > user.email_otp_expires_at:
        return Response(
            {"error": "OTP has expired. Please request a new one."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check OTP match
    if otp != user.email_otp:
        return Response(
            {"error": "Invalid OTP"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Mark verified and clear OTP fields
    user.is_email_verified = True
    user.email_otp = ""
    user.email_otp_expires_at = None
    user.save(update_fields=["is_email_verified", "email_otp", "email_otp_expires_at"])

    return Response({"success": True, "user": _token_pair(user)["user"]})


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
    Body: { refresh }
    Returns: { success: true }
    """
    refresh_token = request.data.get("refresh")
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
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
    return Response({"success": True, **_token_pair(user)})