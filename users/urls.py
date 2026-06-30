from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register),
    path("login", views.login),
    path("refresh", views.token_refresh),
    path("logout", views.logout),
    path("profile", views.profile),
    path("change-password", views.change_password),

    # ── Email verification ──────────────────────────────────────────────────
    path("send-verification", views.send_verification),
    path("verify-email", views.verify_email),
]