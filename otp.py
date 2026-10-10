"""OTP delivery + verification.

OTPProvider is an interface so you can swap SMS vendors without touching the
auth routes. Codes are stored in Redis with a TTL and a max-attempt counter.
Falls back to an in-memory dict if Redis is unreachable (dev only).
"""
import hashlib
import secrets
import time
from abc import ABC, abstractmethod

from .config import settings

OTP_TTL_SECONDS = 300
MAX_ATTEMPTS = 5
RESEND_COOLDOWN_SECONDS = 30

try:
    import redis
    _redis = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    _redis.ping()
except Exception:  # dev fallback
    _redis = None
_memory: dict[str, dict] = {}


class OTPProvider(ABC):
    @abstractmethod
    def send(self, mobile: str, code: str) -> None: ...


class ConsoleOTPProvider(OTPProvider):
    """Development only: prints the code to the server log."""
    def send(self, mobile: str, code: str) -> None:
        print(f"[OTP] {mobile} -> {code}")


class TwilioOTPProvider(OTPProvider):
    def send(self, mobile: str, code: str) -> None:
        from twilio.rest import Client
        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        client.messages.create(
            to=mobile, from_=settings.twilio_from_number,
            body=f"Your InterioX verification code is {code}. It expires in 5 minutes.",
        )


def get_provider() -> OTPProvider:
    return TwilioOTPProvider() if settings.otp_provider == "twilio" else ConsoleOTPProvider()


def _hash(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


def issue_otp(mobile: str) -> None:
    now = time.time()
    last = _get(mobile)
    if last and now - last["issued_at"] < RESEND_COOLDOWN_SECONDS:
        raise ValueError("Please wait before requesting another code.")
    code = f"{secrets.randbelow(900000) + 100000}"
    _set(mobile, {"hash": _hash(code), "issued_at": now, "attempts": 0})
    get_provider().send(mobile, code)


def check_otp(mobile: str, code: str) -> bool:
    rec = _get(mobile)
    if not rec or time.time() - rec["issued_at"] > OTP_TTL_SECONDS:
        return False
    if rec["attempts"] >= MAX_ATTEMPTS:
        return False
    rec["attempts"] += 1
    _set(mobile, rec)
    ok = secrets.compare_digest(rec["hash"], _hash(code))
    if ok:
        _delete(mobile)
    return ok


def _get(mobile):
    if _redis:
        import json
        raw = _redis.get(f"otp:{mobile}")
        return json.loads(raw) if raw else None
    return _memory.get(mobile)


def _set(mobile, rec):
    if _redis:
        import json
        _redis.setex(f"otp:{mobile}", OTP_TTL_SECONDS, json.dumps(rec))
    else:
        _memory[mobile] = rec


def _delete(mobile):
    if _redis:
        _redis.delete(f"otp:{mobile}")
    else:
        _memory.pop(mobile, None)
