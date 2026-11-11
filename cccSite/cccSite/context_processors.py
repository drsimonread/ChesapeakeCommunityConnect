"""Context processors that make site-wide settings available to every template."""

from django.conf import settings


def google_maps(request):
    """Expose the Google Maps browser key to templates as GOOGLE_MAPS_API_KEY.

    The key is read from the environment (see settings.py), never from source
    code. A browser key is visible in the page source by design, so it must be
    restricted by HTTP referrer in the Google Cloud console.
    """
    return {"GOOGLE_MAPS_API_KEY": settings.GOOGLE_API_KEY}
