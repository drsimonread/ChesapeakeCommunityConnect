import hashlib
import hmac

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def hash_google_id(google_id):
    """
    Create a deterministic HMAC-SHA256 hash of a Google user ID.
    """
    key = getattr(settings, "GOOGLE_ID_HASH_KEY", "")

    if not key:
        raise ImproperlyConfigured(
            "GOOGLE_ID_HASH_KEY must be configured."
        )

    if not google_id:
        raise ValueError("Google ID cannot be empty.")

    return hmac.new(
        key.encode("utf-8"),
        google_id.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
