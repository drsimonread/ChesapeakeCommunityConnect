# Secret rotation checklist (SEC-00)

Secrets that were committed to this repository stay in git history, so removing them from the code is not enough. Treat every old value as public and replace it.

## Steps

1. Open the Google Cloud console and create a new Maps API key.
2. Restrict the new browser key by HTTP referrer to the production domain, and to the Maps JavaScript, Places and Geocoding APIs.
3. Create a second key for server-side geocoding and restrict it by IP address (Google recommends separate browser and server keys; the code currently uses one key for both, so add a second setting before using two).
4. Delete the old key in the console.
5. Generate a new Django secret key with this command:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
   ```

6. Store the new key as `DJANGO_SECRET_KEY` in the hosting provider's secret store (and in your local `.env` file for development).
7. Store the new Google key as `GOOGLE_API_KEY` in the same places.
8. Change the passwords for the mailbox and manager accounts that were named in the removed documents (`Email Credentials` and `Manager Email and Password`).
9. Redeploy. Everyone is signed out, because sessions are signed with the secret key; this is expected.
10. Decide with the project owner whether to rewrite git history (for example with `git filter-repo`). This matters most if the repository is public.

## Notes

- Never commit `.env`; `.gitignore` already excludes it.
- `cccSite/.env.example` lists the variable names only.
- A browser Maps key is visible in the page source by design; the referrer restriction is what protects it.
