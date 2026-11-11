# Chesapeake Community Connect: clean-up, security, WCAG 2.1 AA and GDPR plan

Author: Simon Read (SMCM), with Claude. Branch: `plan-sread`, cut from `development`.

## 1. Purpose and how to read this plan

This plan describes how we take the `development` branch of Chesapeake Community Connect (CCC) from "working capstone prototype" to "safe to run in public". It covers four goals:

1. **Security:** close the holes that let anyone read, change or delete other people's data.
2. **WCAG 2.1 AA:** make every page usable with a keyboard, a screen reader, zoom and low vision.
3. **GDPR:** collect less personal data, say clearly what we do with it, and let people see, export and delete it.
4. **Clean-up:** tidy the CSS, remove dead code and comment what is left, so the next student team can read it.

Each task has an ID (for example `SEC-03`), so that we can turn it into a GitHub issue, a branch and a pull request. Work in the order of the phases in section 9; the phases are ordered by risk, not by effort.

Notice that this plan is the result of a read-through of the code, not of running a scanner. Section 10 lists the automated checks that will confirm or correct what we found.

## 2. The application at a glance

| Item | What we found |
| --- | --- |
| Framework | Django (Python), four apps: `account`, `mapViewer`, `boiler` (static pages and contact form), `Janitor` (moderator pages at `/admin/`) |
| Database | SQLite (`db.sqlite3`, git-ignored) |
| Third parties | Google Maps JavaScript API, Google Places and Geocoding, Google Sign-In (`accounts.google.com/gsi/client`), Boxicons from `unpkg.com` |
| Hosting | Two conflicting set-ups: Google App Engine (`app.yaml`, Python 3.9) and Azure Web App (GitHub Actions workflow, Python 3.9) |
| Personal data held | Names, email addresses, usernames, passwords, profile photos, "about" text, forum posts with street addresses, comments, contact messages, user reports |
| Front end | Hand-written CSS (about 6,400 lines in 12 files), server-rendered templates, small amounts of JavaScript |

## 3. Findings

Severity: **Critical** (fix before any further public use), **High**, **Medium**, **Low**.

### 3.1 Security findings

| ID | Severity | Finding | Where |
| --- | --- | --- | --- |
| F-S1 | Critical | **Passwords are stored and compared in plain text.** `AccountCreation.password` holds the raw password, `confirmpassword` stores a second copy, and sign-in uses `account.password != password`. | `account/models.py`, `account/views.py` |
| F-S2 | Critical | **The moderator pages have no access control.** Nothing in `Janitor/views.py` checks who is asking, so anyone who types `/admin/member/1` can open them. The member form includes the `ranking` field, so an anonymous visitor could make themselves an admin. The pages also list every contact message (names and emails). | `Janitor/views.py`, `Janitor/forms.py` |
| F-S3 | Critical | **Secrets are in the repository.** `SECRET_KEY` is hard-coded; a Google API key is hard-coded in `mapViewer/forms.py` and three templates; three documentation files named `Email Credentials` and `Manager Email and Password` are committed. Anything in git history must be treated as public. | `settings.py`, `forms.py`, templates, `Documentation/` |
| F-S4 | Critical | **`DEBUG = True`** in the only settings file. In production this shows source code, settings and SQL to anyone who triggers an error. | `settings.py` |
| F-S5 | High | **Stored cross-site scripting (XSS) on the map.** Post `title` and `description` are placed into an `InfoWindow` HTML string with a template literal, so a post titled `<img src=x onerror=...>` runs script in every visitor's browser. | `mapViewer/static/mapViewer/map-script.js` |
| F-S6 | High | **Banned users can still sign in and act.** Views test `session['rank'] == 0` to mean "signed out", so a rank of `-1` (banned) counts as signed in. The rank is also copied into the session at sign-in, so a demotion does not take effect until the session ends. | `account/views.py`, `mapViewer/views.py` |
| F-S7 | High | **Possible account takeover through email matching.** Password sign-in does `Member.get_or_create(email=...)`, and Google sign-in trusts the email without checking `email_verified`. Whoever registers an approved account with someone else's email gets that person's `Member`. | `account/views.py` |
| F-S8 | High | **Broken moderation code.** `member_manage` writes `form.is_valid` (no brackets, so it is always true) and builds the form without `instance=`, so saving creates a new `Member` instead of editing one. `pendingPostList` and `memberList` use a field `isVisible` that does not exist (the field is `visibility`). `get_posts_and_tags` uses the misspelt field `visiblity`. `reportList` does `Member.objects.get(pk=...)` on unchecked input and calls `print` on report data. | `Janitor/views.py`, `mapViewer/views.py` |
| F-S9 | High | **Dependency and runtime mismatch.** `requirements.txt` pins Django 5.2 (needs Python 3.10 or later) while `app.yaml` and the GitHub workflow use Python 3.9. A virtual environment (`cccSite/venv/`, over 5,000 files, Django 4.2.6) is committed. Several pins (`requests`, `urllib3`, `certifi`) are old. | `requirements.txt`, `app.yaml`, workflow, `venv/` |
| F-S10 | Medium | **No brute-force protection.** Sign-in and sign-up have no rate limit, lock-out or CAPTCHA. Sign-up accepts any password (Django's validators are not used) and any email. | `account/views.py` |
| F-S11 | Medium | **Missing browser protections.** No `Content-Security-Policy`, no HSTS, no secure or `SameSite` settings on session and CSRF cookies, `SECURE_*` imported from `global_settings` instead of being set, `X-Content-Type-Options` and `Permissions-Policy` not configured. | `settings.py` |
| F-S12 | Medium | **Hidden posts accept actions.** In `post_detail` the report and comment handlers run before the visibility check, so pending or denied posts can be commented on or reported by anyone who guesses the ID. | `mapViewer/views.py` |
| F-S13 | Medium | **`viewMap` POST crashes for anonymous users** (`request.session['user']` raises `KeyError`) and trusts `geoResult[0]`. | `mapViewer/views.py` |
| F-S14 | Medium | **Uploads are weakly controlled.** No size limit; the profile image name uses the client's file extension; EXIF metadata (including GPS position) is not removed; `file1` to `file4` on the forum form are accepted but never saved or checked; `MEDIA_URL` lacks a leading slash and media is served through `static()`, which only works in debug. | `account/models.py`, `account/forms.py`, `settings.py` |
| F-S15 | Medium | **Google sign-in endpoint is `csrf_exempt`** and returns plain `HttpResponse` strings for failures. The double-submit check is correct in principle; it needs tests and a proper error page. The OAuth client ID is hard-coded. | `account/views.py` |
| F-S16 | Medium | **Sessions use Django defaults** with no idle time-out, and `signin` does not rotate the session key (session fixation). | `account/views.py` |
| F-S17 | Low | **No security logging or monitoring**, no `security.txt`, no dependency scanning in CI. | repository |
| F-S18 | Low | **Two deployment targets** (App Engine and Azure) with different secrets handling; the Azure workflow uses `actions/checkout@v2` and `setup-python@v1`, both old. | `app.yaml`, workflow |

### 3.2 WCAG 2.1 AA findings

The repository already has a working document, `Documentation/Sorted Documents (SP25)/FA24 Documentation/CCC ADA Compliance Report Working Document.md`. We start from it and re-test, because the templates have changed since.

| ID | WCAG criterion | Finding |
| --- | --- | --- |
| F-A1 | 3.1.1 Language of Page | `base.html` has `<html>` with no `lang`. |
| F-A2 | 1.4.10 Reflow, 1.4.4 Resize Text | No `<meta name="viewport">` in the base template; layouts need testing at 320 CSS pixels and 200% zoom. |
| F-A3 | 2.4.1 Bypass Blocks | No "Skip to main content" link. |
| F-A4 | 1.3.1 Info and Relationships, 4.1.2 Name, Role, Value | Pages use `<div role="main">` rather than one `<main>`; the base template has no `<main>`, so a block lands outside any landmark. `<nav>` has no accessible name; the footer logo and header logo share `id="smcm-logo"` (duplicate ID). |
| F-A5 | 2.4.2 Page Titled | The base template has no `<title>`; check that each page sets a unique one. |
| F-A6 | 1.1.1 Non-text Content | The header image is described as "SMCM Logo" although it is the College seal; decorative images need `alt=""`; map markers and the map itself need a text alternative (the list page at `/search/` can serve as one, but must be linked clearly). |
| F-A7 | 1.2.2 Captions, 1.2.1 Audio-only and Video-only | `tutorial-video.mp4` (Help page) and the `<video>` in `viewForum.html` have no `<track>` captions or transcript. |
| F-A8 | 1.4.3 Contrast (Minimum), 1.4.11 Non-text Contrast | Not yet measured. The College rule is stricter than WCAG: 4.5:1 for all text with no large-text exception. Check gold, light blue, red and grey combinations, placeholder text, disabled states, focus rings and form borders. |
| F-A9 | 2.4.7 Focus Visible, 2.4.3 Focus Order | `details`/`summary` account menu and the five-step "Create Post" wizard need keyboard and focus testing; the wizard must move focus to the new step's heading and announce progress. |
| F-A10 | 3.3.1 Error Identification, 3.3.3 Error Suggestion, 3.3.2 Labels | Server-side errors (`error` variable in sign-in and sign-up) are plain text; they need `role="alert"` and `aria-describedby` links to the field. Check that every field has a visible `<label>`. |
| F-A11 | 1.3.5 Identify Input Purpose | Sign-in, sign-up and contact fields need `autocomplete` values (`username`, `current-password`, `new-password`, `email`, `name`). |
| F-A12 | 1.4.1 Use of Colour, 1.3.3 Sensory Characteristics | Status (visible, pending, denied) and active navigation link are shown by colour alone in places; the emoji in text (`⚠️`) is read aloud as "warning sign". |
| F-A13 | 2.1.1 Keyboard, 2.5.3 Label in Name | Google Maps markers, the `InfoWindow` and the Places autocomplete must be reachable and operable by keyboard; icon-only buttons need a name. |
| F-A14 | 4.1.3 Status Messages | Success and error messages (post created, password changed, "map failed to load") need live regions. |
| F-A15 | 2.4.4 Link Purpose, 2.4.6 Headings and Labels | Links such as "See More" need context; check for one `<h1>` per page and no skipped heading levels. |

### 3.3 GDPR findings

GDPR applies whenever we handle personal data of people in the EU or UK, or monitor their behaviour. The College should confirm with its counsel whether CCC counts as "offering services" to people there; the safe course, and the one this plan follows, is to build to the standard anyway.

| ID | Finding |
| --- | --- |
| F-G1 | **No privacy notice** (Articles 12 to 14): nothing says who the controller is, why we collect data, the lawful basis, how long we keep it, who receives it, or how to complain. |
| F-G2 | **No lawful basis recorded.** Sign-up, posting and contact messages most likely rest on "contract" or "legitimate interests"; Google sign-in and map embedding may need consent. We must decide and write it down. |
| F-G3 | **Third-party data transfers happen without notice or consent.** Loading Google Maps, Google Sign-In and `unpkg.com` sends each visitor's IP address and browser details to US companies before they have done anything. |
| F-G4 | **Data minimisation (Article 5(1)(c)).** `confirmpassword` is stored; the forum form asks for first and last name and a full street address, which may be a home address; contact messages keep name and email indefinitely. |
| F-G5 | **No way to exercise rights.** Access and portability (Articles 15 and 20): `exportData` returns "Not implemented yet". Erasure (Article 17): no self-service deletion; `on_delete=CASCADE` would remove a member's posts and comments but nothing handles backups, media files or reports. Rectification (Article 16) exists only for name, email and about text. |
| F-G6 | **No retention schedule.** Rejected sign-ups, denied posts, resolved reports, contact messages, session rows and uploaded files are kept forever. |
| F-G7 | **Hidden personal data in files.** Profile photos keep EXIF metadata; the uploaded originals are overwritten but not scrubbed. |
| F-G8 | **No records of processing (Article 30), no data-protection impact assessment, no breach procedure (Articles 33 and 34), no processor agreements** with Google or the hosting provider. |
| F-G9 | **Public exposure of members.** The Contributors list and profile pages show name, photo and about text; `account_view` has no sign-in check on the profile URL. Members need to know and be able to limit this. |
| F-G10 | **Logging of personal data.** `print(uList)` writes report data to server logs; debug pages expose request data. |
| F-G11 | **Cookies.** Django's session and CSRF cookies are strictly necessary and need only to be disclosed. Google's scripts may set their own cookies; consent or a click-to-load map is needed unless we decide they are essential (see GDPR-03). |

### 3.4 Clean-up findings

| ID | Finding |
| --- | --- |
| F-C1 | **Committed noise:** `cccSite/venv/` (5,381 tracked files), `cccSite/static/` (output of `collectstatic`, including all of Django admin), a second copy of every app stylesheet under `cccSite/static/`, an empty `cccSite/ChesapeakeCommunityConnect/` directory, `assets 2/`, `.vscode/PythonImportHelper-v2-Completion.json`, `.github/workflows/.gitignore`. |
| F-C2 | **Duplicate files:** `accordian.css` (misspelt) exists in `Janitor` and `account` with the same content; `map-script.js` and `map-script2.js` overlap; `Documentation/` contains two copies of many documents (`Google Drive/` and `Sorted Documents (SP25)/`). |
| F-C3 | **CSS size and structure:** `accountBasestyle.css` is 2,431 lines and `create_forumstyle.css` 1,189 lines. 37 uses of `!important`. Colours repeated as hex literals instead of variables. Inline `style="background-color: #f3c10d; ..."` in `base.html`. The base stylesheet has no table of contents. Class names mix `camelCase`, `kebab-case` and BEM (`dir-search__bar`). Page-specific CSS is loaded for pages that do not use it. |
| F-C4 | **Python:** `from .models import *` and `from .forms import *` hide where names come from; unused imports (`HttpResponse`, `serializers`, `datetime`, `googlemaps`); unused or broken classes (`CreateAccountForm` calls `Member.objects.create(user=...)` but `Member` has no `user`; `MessageForm` is defined in both `account/models.py` and `boiler/models.py`); `contact` and `help` views are near copies; forms defined inside `models.py`; `update_maptags.py` and `main.py` at the project root have no explanation. Helpful comments exist in places but are lower-case sentence fragments, not docstrings. |
| F-C5 | **Tests:** the four `tests.py` files total about 450 lines but do not cover sign-in, permissions, uploads or moderation. There is no continuous integration for tests. |
| F-C6 | **Documentation:** `README.md`, `CCCSetupInstructions.md`, `RUN_DEV_SERVER.md` and the Documentation folders overlap and disagree on how to run the site. |

## 4. Principles for the work

1. **Fix the permissions first.** Nothing else matters while anyone can open the moderator pages.
2. **One task, one branch, one pull request.** Small changes are easy to review and easy to undo.
3. **Write a test before you fix a bug** (or at least with it), so that the bug cannot return.
4. **Use Django's own tools** (`login_required`-style decorators, `django.contrib.auth` password hashing, form validation, the template engine's auto-escaping) in preference to home-made ones. Simon says: don't write your own password code, even though this project did once; you'll get it wrong.
5. **Never put a secret in git.** Secrets live in environment variables or the hosting provider's secret store; `.env.example` shows the names only.
6. **Comment the "why", not the "what".** `x = x + 1  # add one to x` helps nobody.

## 5. Security work

### Phase 0: stop the bleeding (do this before anything else)

| ID | Task | Done when |
| --- | --- | --- |
| SEC-00 | **Rotate every exposed secret.** Create a new Django `SECRET_KEY`. Create a new Google Maps key restricted to the production domain and to the three APIs we use; delete the old key in the Google Cloud console. Change the mailbox and manager passwords named in the three credential documents. Remove those documents (`git rm`) and, if the repository is or will be public, remove them from history with `git filter-repo` after the team agrees. | Old keys no longer work; no secret appears in `git grep`. |
| SEC-01 | **Protect the moderator pages.** Add one decorator (for example `moderator_required`) that checks the signed-in `Member` in the database (not the session copy) and returns 403 or a redirect to sign-in. Apply it to every view in `Janitor/views.py`. Make `ranking` read-only for anyone below admin (rank 99) and log every rank change. | An anonymous request and a rank-1 request to each `/admin/...` URL are refused (tests). |
| SEC-02 | **Turn off debug.** Split settings into environment-driven values: `DEBUG` defaults to `False`; `ALLOWED_HOSTS`, `SECRET_KEY`, `CSRF_TRUSTED_ORIGINS` and the database come from environment variables. | `python manage.py check --deploy` reports no warnings in production mode. |
| SEC-03 | **Hash passwords.** Move sign-in to Django's `User` model and `authenticate()`/`login()`, or at minimum call `make_password()` and `check_password()` on `AccountCreation.password`. Remove the `confirmpassword` column. Write a data migration that forces a password reset for every existing account (we cannot hash what we do not know, and the plain-text copies must be deleted). Use `AUTH_PASSWORD_VALIDATORS` on sign-up and change-password forms, with a minimum of 12 characters. | No password-like value is readable in the database; a test proves the old plain-text path is gone. |
| SEC-04 | **Fix the map XSS.** Build the `InfoWindow` with DOM calls (`textContent`, `setAttribute`) instead of a template literal; keep `json_script` for the data. Add a regression test with a post titled `<script>alert(1)</script>`. | The title appears as text, never as markup. |

### Phase 1: access control and sessions

| ID | Task | Done when |
| --- | --- | --- |
| SEC-10 | Replace `session['rank'] == 0` checks with a helper `current_member(request)` that returns the live `Member` or `None`, and treats rank `-1` as signed out. One place, used everywhere. | Banned user is refused on every view (tests). |
| SEC-11 | `session.cycle_key()` on sign-in; `SESSION_COOKIE_AGE` of 2 weeks or less; `SESSION_EXPIRE_AT_BROWSER_CLOSE` decided and documented. | Session id changes after sign-in (test). |
| SEC-12 | Stop linking accounts by email alone. A `Member` is created at sign-up and linked to the credential record by primary key. Google sign-in requires `email_verified` and links to an existing member only after that member confirms with their password. | Registering with a stranger's email gives no access to the stranger's data (test). |
| SEC-13 | Run the visibility check in `post_detail` before any POST handling. Pending and denied posts are visible only to their author and to moderators; comments and reports on them are refused. | Tests for each of the three visibility states. |
| SEC-14 | Fix `viewMap` POST for anonymous users (redirect to sign-in), validate `geoResult`, and merge duplicated post-creation code with `account.views.create_forum`. | Anonymous POST returns a redirect, not a 500. |
| SEC-15 | Repair the broken moderation views listed in F-S8 (`is_valid()`, `instance=`, `visibility`, `visiblity`, `get_object_or_404`, remove `print`). | Each view has a passing test. |
| SEC-16 | Rate-limit sign-in, sign-up, contact and report forms (`django-axes` or `django-ratelimit`); add a honeypot field or CAPTCHA on public forms. | Sixth wrong password in a minute is refused (test). |
| SEC-17 | Add an audit log table (who, what, when, from which IP hash) for sign-ins, rank changes, post approvals and deletions. Keep it for a fixed, documented time (see GDPR-06). | Entries appear for each listed event. |

### Phase 2: hardening

| ID | Task | Done when |
| --- | --- | --- |
| SEC-20 | Set `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS` (start small, then raise), `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SAMESITE`, `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_REFERRER_POLICY`, `X_FRAME_OPTIONS = "DENY"`, and a `Permissions-Policy` header. Remove the `global_settings` imports. | Mozilla Observatory grade A or better. |
| SEC-21 | Add a `Content-Security-Policy` (`django-csp`). This needs the inline `style=` attributes and any inline `<script>` blocks removed first (see CSS-10); allow only our origin, Google Maps and Google Sign-In. Start in report-only mode. | No violations in report-only mode for a full test run; then enforce. |
| SEC-22 | Upload hardening: limit size (for example 2 MB for photos), check content with Pillow and `python-magic` (already in `requirements.txt`), re-encode images to strip EXIF, generate random file names, store outside the web root or in a bucket, serve through the web server or a signed URL, and fix `MEDIA_URL`. Either implement `file1` to `file4` with the same checks or remove them. | Test uploads of a script renamed `.jpg`, an oversized file and a photo with GPS data. |
| SEC-23 | Pin and update dependencies with exact versions and hashes (`pip-compile`); update `requests`, `urllib3`, `certifi`, `google-auth`; choose one Python version (3.12) for `app.yaml`, the workflow and local development. Add Dependabot and `pip-audit` to CI. | `pip-audit` clean; CI and host use the same Python. |
| SEC-24 | Pick one deployment target and delete the other's config. Update the workflow actions to current versions; store secrets in the host's secret store; deploy only from a protected `main` after tests pass. | One documented deployment path. |
| SEC-25 | Move to PostgreSQL (or Cloud SQL / Azure Database) for production; encrypt backups; document restore. | A restore test is written in the runbook. |
| SEC-26 | Replace `HttpResponse("Something went wrong...")` strings in `authG` with logged errors and a friendly template; read the client ID from settings; add tests with a mocked token verifier. | Tests cover missing cookie, mismatched token, bad token and success. |
| SEC-27 | Add `/.well-known/security.txt`, a short "Report a vulnerability" section in `README.md`, and structured logging with no personal data in messages. | File served; log review done. |
| SEC-28 | Run `bandit`, `ruff --select S`, `python manage.py check --deploy`, OWASP ZAP baseline scan and fix what they find. | Reports attached to the pull request. |

## 6. WCAG 2.1 AA work

Target: every public page and every signed-in page conforms to WCAG 2.1 AA, with the College's stricter contrast rule (4.5:1 for all text).

| ID | Task | Criteria | Done when |
| --- | --- | --- | --- |
| A11Y-01 | **Base template.** Add `lang="en"`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, a `{% block title %}` that every page fills with a unique title, a "Skip to main content" link (first focusable element), one `<main id="main">`, `aria-label` on each `<nav>`, a `<footer>` landmark, and unique IDs (use a class for the logo). Remove every `role="main"` from child templates. | 1.3.1, 2.4.1, 2.4.2, 3.1.1, 4.1.1 | axe reports no landmark, language or duplicate-ID issues. |
| A11Y-02 | **Colour tokens and contrast.** Define the palette once as CSS custom properties (see CSS-02). Measure every text and background pair with a script; remove any pair under 4.5:1, any non-text component (borders, icons, focus ring) under 3:1. Do not use dark grey or red text on white or navy where the College rule forbids it. | 1.4.3, 1.4.11 | Contrast report committed under `Documentation/Accessibility/`. |
| A11Y-03 | **Focus.** Visible focus ring on every interactive element (never `outline: none` without a replacement); logical tab order; the account `details` menu closes on Escape and returns focus to its summary; wizard step changes move focus to the step heading. | 2.1.1, 2.4.3, 2.4.7 | Keyboard-only walk-through of each page recorded as a checklist. |
| A11Y-04 | **Active navigation state.** Replace inline gold styles with `aria-current="page"` plus a CSS rule that also adds a non-colour cue (underline or bar). | 1.4.1, 4.1.2 | Screen reader announces "current page". |
| A11Y-05 | **Forms.** Every control has a programmatically linked `<label>`; required fields marked in text and with `required`/`aria-required`; `autocomplete` tokens on personal-data fields; errors shown in a summary with `role="alert"`, each linked to its field by `aria-describedby`; do not rely on placeholder text as a label. | 1.3.1, 1.3.5, 3.3.1, 3.3.2, 3.3.3 | Test with NVDA and VoiceOver. |
| A11Y-06 | **Map.** Give the map region a heading, an `aria-label` and a visible "View these posts as a list" link to `/search/`; ensure markers and the `InfoWindow` are keyboard-operable (Advanced Markers support this when given a click handler and `gmpClickable`); make sure the list view carries the same information as the map. | 1.1.1, 2.1.1, 4.1.2 | Every post can be found, read and opened without the map. |
| A11Y-07 | **Create Post wizard.** Use real `<fieldset>`/`<legend>` for radio groups, announce "Step 2 of 5" in a polite live region, keep entered data when moving back, and make draft saving (`cf-draft-line`) announce its state. | 1.3.1, 3.3.4, 4.1.3 | Complete a post using only the keyboard. |
| A11Y-08 | **Media.** Add captions (WebVTT `<track kind="captions">`) and a text transcript for `tutorial-video.mp4` and any user-supplied video; no autoplay. | 1.2.2, 1.2.3 | Captions load and match the audio. |
| A11Y-09 | **Images and icons.** Meaningful `alt` text; `alt=""` for decoration; icon fonts hidden with `aria-hidden="true"` and paired with visible text or an accessible name; replace emoji used as icons with CSS or SVG icons; correct the alt text on the header image. Replace the College seal with the official logo file (the seal is not for general use). | 1.1.1, 1.4.5 | No image without an `alt` attribute. |
| A11Y-10 | **Responsive and zoom.** No horizontal scrolling at 320 CSS pixels (except maps and tables with their own scroll region); layout survives 200% text zoom and user-set text spacing; touch targets at least 24 by 24 CSS pixels (aim for 44). | 1.4.4, 1.4.10, 1.4.12 | Manual checks at 320, 768 and 1280 pixels. |
| A11Y-11 | **Status messages and motion.** Live regions for success and error messages; honour `prefers-reduced-motion`; nothing flashes more than three times a second. | 2.3.1, 4.1.3 | Reviewed. |
| A11Y-12 | **Content.** One `<h1>` per page and no skipped heading levels; link text that makes sense out of context ("Read the post: {title}" instead of "See More"); plain, sentence-case wording; fonts Arial or a system font stack. | 2.4.4, 2.4.6 | Heading outline checked per page. |
| A11Y-13 | **Tooling and regression.** Add `axe-core` (through `pytest-playwright` or `pa11y-ci`) to CI against every URL; run Lighthouse accessibility; keep a manual test script for screen reader and keyboard checks. | all | CI fails on any new axe violation. |
| A11Y-14 | **Accessibility statement.** Publish a page that states the conformance level, known gaps, a contact address and a feedback process. | n/a | Linked from the footer. |

## 7. GDPR work

Owner for GDPR decisions: the College (the controller). The student team prepares the evidence; the College's privacy officer or counsel signs it off.

| ID | Task | Done when |
| --- | --- | --- |
| GDPR-01 | **Data map.** List every field we store (table, column, purpose, source, who can see it, where it goes, retention). Start from the models in section 2; add logs, backups and the hosting provider. | `Documentation/Privacy/data-map.md` reviewed by the College. |
| GDPR-02 | **Lawful basis and records (Article 30).** For each purpose pick and record a basis: account and posting ("contract" or "legitimate interests"), contact form ("legitimate interests"), Google sign-in and map embed (consent or legitimate interests, decided with counsel). Write the record of processing. Decide whether a data-protection impact assessment is needed (public postings with addresses suggest yes). | Signed-off record and DPIA decision. |
| GDPR-03 | **Third parties and consent.** Self-host Boxicons (or replace with inline SVG) and any fonts. For Google Maps and Google Sign-In, show a "Load map" / "Sign in with Google" button that loads the script only after the visitor clicks (or after consent in a cookie banner if counsel requires it), with a plain description of what is sent. Sign data-processing terms with Google and the host. | No request to a third-party host before a user action (network log). |
| GDPR-04 | **Privacy notice and cookie notice.** Write a clear notice linked from the footer and from every form: controller and contact, purposes and bases, recipients (Google, host), transfers outside the EU and the safeguard used, retention periods, the rights below, the right to complain to a supervisory authority. A cookie notice lists the session and CSRF cookies (strictly necessary) and anything else we find. | Pages published and linked. |
| GDPR-05 | **Minimise.** Delete `confirmpassword` (SEC-03); drop first and last name from the post form unless they are needed; replace the full street address with a place, intersection or rounded coordinates by default and warn that home addresses should not be entered; make `about` optional and clearly public; make the contact form's email optional if a reply is not needed. Check `geoCode` JSON for extra fields from Google and store only latitude, longitude and a label. | Updated forms and migrations; data map updated. |
| GDPR-06 | **Retention schedule and automatic clean-up.** Proposed: rejected sign-ups 30 days; unacknowledged contact messages 12 months and acknowledged ones 6 months after closing; resolved reports 12 months; audit log 12 months; denied posts 90 days; server logs 30 days; backups 35 days; inactive members (no sign-in for 3 years) are warned and then deleted. Implement as a management command run by a scheduler, with tests. The College confirms the numbers. | Command runs in CI against test data. |
| GDPR-07 | **Right of access and portability (Articles 15 and 20).** Implement "Download my data" in the account page: a ZIP of JSON (and the profile photo) with the member's profile, posts, comments, reports about them (as allowed) and consent records. Replace the `exportData` stub or delete it. | Member can download within one minute (test). |
| GDPR-08 | **Right to erasure and restriction (Articles 17 and 18).** Add "Delete my account" with a re-authentication step and a confirmation page. Decide the rule for posts and comments: delete, or anonymise ("former member") when other people's comments depend on them. Remove the profile photo file, linked `GLogIn` rows, sessions and reports about the member. Provide a moderator-run path for requests that arrive by email, and document the one-month response deadline. | End-to-end test leaves no personal data (database or media). |
| GDPR-09 | **Right to rectification and objection.** Let members edit every field we hold about them; add a "hide me from the Contributors list" setting; make profile pages and the Contributors list visible only to signed-in members or according to that setting, and tell members which it is at sign-up. | Settings page and tests. |
| GDPR-10 | **Sign-up consent and age.** Add an unticked checkbox "I have read the privacy notice" (linked) and, if counsel requires, an age statement (16 or over, or the lower national age of consent). Store the time and version of the notice accepted. | Cannot register without ticking. |
| GDPR-11 | **Security of processing (Article 32)** is delivered by section 5; record it in the data map and keep the evidence (scan reports). | Cross-referenced. |
| GDPR-12 | **Breach procedure (Articles 33 and 34).** One page: who decides, how to contain, 72-hour notification to the supervisory authority, how to tell affected members, where to log it. Name the contacts. | Procedure approved; run a table-top exercise. |
| GDPR-13 | **Logs and debugging.** No names, emails, passwords, tokens or addresses in logs; remove `print` calls; hash or truncate IP addresses in the audit log; short log retention. | Log review complete. |
| GDPR-14 | **Moderation transparency.** Tell members that reports and moderator notes about them are kept, for how long, and how to ask about them. | Text in the privacy notice. |

## 8. Clean-up work (CSS, code and comments)

### 8.1 Repository hygiene

| ID | Task | Done when |
| --- | --- | --- |
| CLN-01 | `git rm -r --cached cccSite/venv` and rely on `.gitignore` (it already lists `venv/`); update docs to say "create your own virtual environment". | `git ls-files` shows no `venv`. |
| CLN-02 | Stop committing `cccSite/static/` (generated by `collectstatic`); keep sources in each app's `static/` folder and in `cccSite/cccSite/static/`; run `collectstatic` at deploy time; set `STATIC_ROOT` to a path outside the source tree (for example `BASE_DIR / "staticfiles"`) and use WhiteNoise or the host's static handler. Delete the duplicated copies. | One copy of each stylesheet. |
| CLN-03 | Remove the empty `cccSite/ChesapeakeCommunityConnect/` directory, `assets 2/`, `.vscode/PythonImportHelper-v2-Completion.json`, `.github/workflows/.gitignore`; rename directories without spaces (the project rule: CamelCase directory names, lower-case hyphenated file names). | Tree reviewed. |
| CLN-04 | Consolidate documentation: one `README.md` (what it is, how to run, how to test, how to deploy, how to contribute), one `Documentation/` tree without duplicate copies of the same file, and move meeting notes to the wiki or a `Documentation/Archive/` folder. Delete `RUN_DEV_SERVER.md`, `CCCSetupInstructions.md` and `GoogleCloudAndVSCodeInstructions.md` after merging their useful steps. Write instructions for a beginner: numbered steps, one action per step. | New student runs the site from the README alone. |
| CLN-05 | Add `.editorconfig`, `pyproject.toml` (ruff, black), `.pre-commit-config.yaml`, `.stylelintrc.json`, `.djlintrc`, and a `CONTRIBUTING.md`. | Pre-commit passes on a clean checkout. |

### 8.2 CSS clean-up

Goal: smaller, predictable, themeable CSS that meets the College palette and the contrast rule. Colours (solid only): SMCM Blue `#00205C` (primary), gold `#F3C10D` and white (secondary), red `#D0343A`, light blue `#59B7E2`, dark grey `#847870`, light grey `#D6D1CA` (tertiary, only alongside blue or gold).

| ID | Task | Done when |
| --- | --- | --- |
| CSS-01 | **Inventory.** Record, for each stylesheet, which templates load it and which selectors are unused (Chrome DevTools Coverage or `purgecss --rejected`). Delete dead rules after checking each template and each state (hover, focus, error, empty list, logged-in and logged-out). | Inventory table in `Documentation/Css/inventory.md`; size drops. |
| CSS-02 | **Design tokens.** Create `static/base/tokens.css` with `:root` custom properties: palette (`--color-smcm-blue`, `--color-gold`, ...), semantic colours (`--color-text`, `--color-surface`, `--color-focus`), font stack (`Arial, Helvetica, sans-serif`), spacing scale, radii, breakpoints documented in comments. Replace every hex literal. Solid colours only; no gradients. | `grep -E '#[0-9a-fA-F]{3,6}'` finds hex only in `tokens.css`. |
| CSS-03 | **Structure.** Adopt one layout, loaded in this order: `tokens.css`, `reset.css`, `base.css` (elements), `layout.css` (header, nav, footer, page grid), `components/*.css` (button, card, form, accordion, pager, hero, wizard), `pages/*.css` (only what is truly page-specific). Split `accountBasestyle.css` and `create_forumstyle.css` along these lines; do not load a page's CSS on other pages. | No file longer than about 400 lines. |
| CSS-04 | **Naming.** Use BEM (`block__element--modifier`) in kebab-case throughout; rename `nameField`, `emailField` and similar; prefix JavaScript hooks with `js-` and never style them. Update templates in the same commit as the CSS. | Stylelint selector-class-pattern passes. |
| CSS-05 | **Specificity.** Remove all 37 `!important` declarations by fixing selector order and specificity; forbid new ones in Stylelint (`declaration-no-important`). | Zero `!important` (except documented print/reduced-motion rules). |
| CSS-06 | **Duplicates.** Merge the two `accordian.css` files into `components/accordion.css` (and fix the spelling); remove duplicated media queries by grouping them under each component. | One accordion stylesheet. |
| CSS-07 | **Responsive.** Mobile first: base rules for small screens, `min-width` media queries for larger ones; use `rem` for text, `clamp()` sparingly, logical properties where easy; test at 320, 768 and 1280 pixels. | Passes A11Y-10. |
| CSS-08 | **Accessibility in CSS.** Global `:focus-visible` style from a token; `prefers-reduced-motion` block that disables transitions; `forced-colors` check for Windows High Contrast; minimum target sizes. | Passes A11Y-03 and A11Y-11. |
| CSS-09 | **Comments.** Each file starts with a header comment (purpose, which templates use it, dependencies). Each section has a banner comment (`/* ===== Navigation ===== */`). Comment every non-obvious value (why `z-index: 1000`, why a magic `margin-top`), every browser workaround and every colour pair that was chosen for contrast (with the ratio). Do not comment the obvious. Do not put dates or change notes in files; git records those. | Stylelint rule `comment-empty-line-before` plus review. |
| CSS-10 | **Remove inline styles and scripts.** Move every `style="..."` and inline `<script>` from templates into stylesheets and `.js` files (needed for the CSP in SEC-21). | `grep 'style="'` in templates returns nothing. |
| CSS-11 | **Tooling.** Add Stylelint with `stylelint-config-standard`, Prettier for CSS, and a visual regression check (Playwright screenshots) for the ten main pages before and after each CSS change. | CI job green; before-and-after screenshots attached to the pull request. |

### 8.3 Python, template and JavaScript clean-up

| ID | Task | Done when |
| --- | --- | --- |
| CLN-10 | Replace star imports with explicit imports; remove unused imports and variables (`ruff --select F`); delete dead or broken code (`CreateAccountForm`, duplicate `MessageForm`, `pendingPostList` stub, commented-out blocks, unused `map-script2.js` after checking which map script each page loads). | `ruff check` clean. |
| CLN-11 | Move forms out of `models.py` into `forms.py`; one `MessageForm`; merge `help` and `contact` views; rename `AccountCreation` to something that says what it is (`SignupRequest`) with a migration; fix naming (`Janitor` to `moderation`, `accordian` to `accordion`, `boiler` to `pages`) in one dedicated, mechanical pull request after the behaviour fixes are merged. | Renames reviewed alone. |
| CLN-12 | Use Django's `LoginRequiredMixin`-style helpers or decorators so that "is signed in" is not repeated in every view; keep views short; move query logic into model methods or managers (for example `MapPost.objects.visible()`). | No view longer than about 40 lines. |
| CLN-13 | Add `select_related`/`prefetch_related` where lists are built (`memberList` runs several queries per member; `reportList` runs one query per item). Add pagination to the moderator lists. | Django Debug Toolbar shows constant query counts. |
| CLN-14 | Database: add `unique` constraints and indexes where the code assumes them (username, email on `AccountCreation` for pending requests; `MapPost.visibility`); review `on_delete` choices together with GDPR-08. | Migrations reviewed. |
| CLN-15 | Template clean-up: use `{% include %}` for repeated blocks (hero, pager, form field), `{% url %}` for every link, no logic in templates beyond display. | Repeated markup removed. |
| CLN-16 | JavaScript: `const`/`let` only, modules or an IIFE, no globals; one map script; `defer` on every script; ESLint (a `.eslintrc.json` already exists) wired to CI. | `eslint` clean. |

### 8.4 Commenting standard

Apply these rules to everything we touch, and add them to `CONTRIBUTING.md`.

1. **Python:** every module, class and public function has a docstring (PEP 257): one summary line, then arguments, return value and side effects when they are not obvious. Use type hints on new code. Inline comments explain *why*. Keep the helpful comments the team already wrote (the Google sign-in explanation, for example) but rewrite them as full sentences.
2. **Models:** comment every field whose meaning is not clear from its name (`ranking`, `visibility`, `geoCode`), listing the allowed values and what each does.
3. **Templates:** a Django comment `{# ... #}` at the top of each file says which view renders it and which context variables it expects; mark the start of each `{% block %}` section. Use `{# #}`, not HTML comments, so that comments are not sent to the browser.
4. **JavaScript:** JSDoc (`/** ... */`) for every function; say what the page must contain (element IDs) for the script to work.
5. **CSS:** see CSS-09.
6. **Remove, do not comment out.** Dead code goes; git remembers it.
7. **Track progress** with a checklist in the pull request replacing the older `Uncommented Code Tracker.md`.
8. Comments are in British English, with no personal names, dates or "fixed bug" notes.

## 9. Order of work

Assume a team of four to six students over two semesters; adjust the dates when the schedule is known. "S" is under half a day, "M" is one to two days, "L" is three days or more.

| Phase | Tasks | Size | Gate to move on |
| --- | --- | --- | --- |
| **0. Emergency** | SEC-00, SEC-01, SEC-02, SEC-04, CLN-01 | S to M | Moderator pages locked, no secrets in the repo, debug off |
| **1. Foundation** | CLN-02 to CLN-05 (tooling), SEC-23, SEC-24, SEC-03, SEC-10, SEC-11, test scaffold and CI | M to L | CI runs tests, ruff, bandit and pip-audit on every push |
| **2. Security fixes** | SEC-12 to SEC-17, SEC-22, SEC-26 | L | All Critical and High findings closed, each with a test |
| **3. Front-end base** | A11Y-01, A11Y-02, CSS-01, CSS-02, CSS-03, CSS-10, A11Y-13 | L | New base template and token file merged; axe runs in CI |
| **4. Page-by-page** | For each page group (public pages, sign-in and sign-up, account, create post, map and posts, moderator): A11Y-03 to A11Y-12, CSS-04 to CSS-09, CLN-10 to CLN-16, commenting standard | L (repeat) | Page passes axe, manual keyboard and screen reader tests, and has no unused CSS |
| **5. GDPR build** | GDPR-03, GDPR-05 to GDPR-10, GDPR-13 (code), SEC-20, SEC-21, SEC-25 | L | Export, delete and retention features pass end-to-end tests; CSP enforced |
| **6. GDPR paperwork** | GDPR-01, GDPR-02, GDPR-04, GDPR-12, GDPR-14, A11Y-14 | M | College privacy officer approves notices and records |
| **7. Verify and hand over** | SEC-27, SEC-28, full WCAG audit (automated plus manual, ideally by someone who did not build it), penetration test of the staging site, final README and runbook | M | Reports filed in `Documentation/`; sign-off from the project owner |

## 10. Verification

We do not call a task done until its check passes.

1. **Automated, on every push (continuous integration):** `python manage.py check --deploy`, `python manage.py makemigrations --check`, `pytest` (unit, permission and regression tests), `ruff check`, `black --check`, `bandit -r`, `pip-audit`, `stylelint`, `eslint`, `djlint --lint`, axe-core against every URL, Playwright screenshots on the main pages.
2. **Manual, before each release:** keyboard-only walk-through; NVDA with Firefox or Chrome on Windows; VoiceOver with Safari on macOS and iOS; 200% zoom and 320-pixel width; Windows High Contrast; colour-blindness simulation.
3. **External:** OWASP ZAP baseline scan; Mozilla Observatory; SSL Labs; WebAIM contrast checker for any new pair; Google Lighthouse (accessibility and best practices).
4. **GDPR evidence:** data map and records of processing reviewed; privacy notice live; test results for export, deletion and retention; processor agreements filed; breach procedure rehearsed.

## 11. Risks and decisions needed

| Decision | Who | Why it matters |
| --- | --- | --- |
| Is the repository public, and was any secret ever exposed there? | Project owner | If yes, rotate everything (SEC-00) and consider rewriting history. |
| Which host: Google App Engine or Azure? | Project owner and IT | Fixes the Python version, secrets store, database and backups (SEC-24, SEC-25). |
| Does GDPR apply, and under which basis does each purpose run? | College privacy officer or counsel | Drives the notice, consent and retention numbers. |
| Does the public map show home addresses? | Client | If yes, a DPIA is needed and GDPR-05 becomes mandatory. |
| Move to Django's `User` model or keep the custom `Member` plus hashed passwords? | Team lead | `User` is safer and lets us reuse password reset and lockout tools; it needs a careful data migration. |
| Official branding: remove the College seal from the header and use the approved logo | Marketing (Office of Integrated Marketing & Communications) | The brand rules do not allow the seal here. Public pages carrying the College name should also be checked against the web style guide. |
| Who owns accessibility sign-off? | Project owner | WCAG conformance needs an independent final check. |

Risks: schema changes (password hashing, renames) can lose data, so back up the database and rehearse every migration on a copy; changing CSS class names and templates together can break pages quietly, which is why we take before-and-after screenshots; moving to a CSP can break inline code, which is why we begin in report-only mode.

## 12. Definition of done (whole project)

1. No Critical or High finding is open; Medium findings are fixed or accepted in writing.
2. Every public and signed-in page passes automated and manual WCAG 2.1 AA checks, with 4.5:1 contrast for all text.
3. Privacy notice, data map, records of processing, retention job, export and erasure features, and breach procedure exist and are approved.
4. CSS is tokenised, split, free of `!important`, free of dead rules and commented; Python, templates and JavaScript are commented to the standard in section 8.4.
5. A new student can clone the repository, follow the README and have a running, tested site.

---

Plan written with Claude Sonnet 5.5 (Anthropic).
