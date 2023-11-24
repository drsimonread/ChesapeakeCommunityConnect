# ChesapeakeCommunityConnect
when you make a venv, to get the log in to work locally must go to .venv/lib/python3.11/site-packages/django/conf/global_settings.py and change 
SECURE_CROSS_ORIGIN_OPENER_POLICY to "same-origin-allow-popups"
SECURE_REFERRER_POLICY to "same-origin-no-downgrade"
because we're in production mode according to google only approved emails can log in with google. once site is closer to finished we can apply to change that
