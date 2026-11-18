import hashlib
import hmac

from django.conf import settings

def hash_google_id(google_id):
    key = settings.GOOGLE_ID_HASH_KEY.encode("utf-8")
    return hmac.new(key, str(google_id).encode("utf-8"),
    hashlib.sha256).hexdigest()