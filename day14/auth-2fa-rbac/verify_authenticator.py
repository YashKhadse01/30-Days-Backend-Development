
from pathlib import Path

from auth_2fa_rbac.totp import verify_totp

secret = Path(".totp_test_secret").read_text(
    encoding="utf-8"
).strip()

otp = input("Enter Google Authenticator OTP: ").strip()

if verify_totp(secret, otp, window=1):
    print("SUCCESS: Google Authenticator verified!")
else:
    print("FAILED: Invalid or expired OTP.")
