"""
Email utilities for DrugSpot using Brevo SMTP relay.

Add these to your .env:
  BREVO_SMTP_LOGIN     = affe2c001@smtp-brevo.com
  BREVO_SMTP_PASSWORD  = your-smtp-key (the value ending in 1xkSfi)
  BREVO_SENDER_EMAIL   = no-reply@yourdomain.com   (must be verified in Brevo)
  BREVO_SENDER_NAME    = DrugSpot
"""

import os
import random
import string
import logging
from datetime import timedelta

from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

logger = logging.getLogger(__name__)

BREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL", "no-reply@drugspot.com")
BREVO_SENDER_NAME  = os.environ.get("BREVO_SENDER_NAME", "DrugSpot")

OTP_LENGTH         = 6
OTP_EXPIRY_MINUTES = 15


def generate_otp() -> str:
    return "".join(random.choices(string.digits, k=OTP_LENGTH))


def send_verification_email(user) -> bool:
    """
    Generate a new OTP, persist it on the user record, then send via Brevo SMTP.
    Returns True on success, False on failure.
    """
    otp = generate_otp()
    user.email_otp = otp
    user.email_otp_expires_at = timezone.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    user.is_email_verified = False
    user.save(update_fields=["email_otp", "email_otp_expires_at", "is_email_verified"])

    subject    = "Verify your DrugSpot account"
    from_email = f"{BREVO_SENDER_NAME} <{BREVO_SENDER_EMAIL}>"
    text_body  = (
        f"Hi {user.username},\n\n"
        f"Your DrugSpot verification code is: {otp}\n\n"
        f"It expires in {OTP_EXPIRY_MINUTES} minutes.\n\n"
        "If you did not create an account, ignore this email."
    )
    html_body = _build_email_html(user.username, otp)

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=from_email,
            to=[user.email],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
        logger.info("Verification email sent to %s", user.email)
        return True
    except Exception as exc:
        logger.error("Failed to send verification email: %s", exc)
        return False


def _build_email_html(username: str, otp: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Verify your DrugSpot account</title>
</head>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f9;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="480" cellpadding="0" cellspacing="0"
               style="background:#ffffff;border-radius:12px;overflow:hidden;
                      box-shadow:0 2px 8px rgba(0,0,0,.08);">
          <tr>
            <td style="background:#1a7bbb;padding:28px 32px;text-align:center;">
              <h1 style="margin:0;color:#ffffff;font-size:22px;letter-spacing:.5px;">
                💊 DrugSpot
              </h1>
            </td>
          </tr>
          <tr>
            <td style="padding:36px 32px 24px;">
              <p style="margin:0 0 8px;font-size:16px;color:#333;">
                Hi <strong>{username}</strong>,
              </p>
              <p style="margin:0 0 28px;font-size:15px;color:#555;line-height:1.6;">
                Thanks for signing up! Use the code below to verify your email address.
                The code expires in <strong>{OTP_EXPIRY_MINUTES} minutes</strong>.
              </p>
              <div style="text-align:center;margin:0 0 32px;">
                <span style="display:inline-block;padding:18px 40px;
                             background:#f0f7ff;border:2px dashed #1a7bbb;
                             border-radius:10px;font-size:36px;font-weight:bold;
                             letter-spacing:10px;color:#1a7bbb;">
                  {otp}
                </span>
              </div>
              <p style="margin:0;font-size:13px;color:#999;line-height:1.6;">
                If you didn't create a DrugSpot account, you can safely ignore this email.
              </p>
            </td>
          </tr>
          <tr>
            <td style="background:#f9f9f9;padding:16px 32px;text-align:center;
                       border-top:1px solid #eee;">
              <p style="margin:0;font-size:12px;color:#aaa;">
                © 2026 DrugSpot. All rights reserved.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""