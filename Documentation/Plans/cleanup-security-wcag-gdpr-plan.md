# Chesapeake Community Connect: plan for clean-up, security, WCAG 2.1 AA and GDPR

Authors: Simon Read (St. Mary's College of Maryland) and Claude Fable 5.2.

Branch: `plan-sread`, cut from `development`.

## 1. What this plan is for

Chesapeake Community Connect (CCC) is a working capstone prototype. This plan says how we turn it into a site that is safe to put in front of the public. There are four goals:

1. **Security.** Nobody can read, change or delete data that is not theirs.
2. **WCAG 2.1 AA.** Every page works with a keyboard, a screen reader, zoom and low vision.
3. **GDPR.** We collect less personal data, we say what we do with it, and people can see, export and delete their own.
4. **Clean-up.** The CSS is small and consistent, dead code is gone, and what remains is commented so that next semester's team can read it.

Think of it like taking over a second-hand car. Before we polish the paintwork (CSS), we check the brakes (who is allowed to do what) and make sure the doors lock (passwords and secrets). That is why the work is ordered by risk, not by how interesting it is.

The findings come from two sources: reading the code on `development`, and then running scanners against it and against a local copy of the site. Section 13 records what each scanner reported. Notice that the scanners confirmed some findings, corrected one (F-S1) and missed the most serious ones altogether; a clean scan report is not the same thing as a safe site.

### How to use this plan

1. Pick the next open task in the current phase (section 8).
2. Open a GitHub issue with the task ID in the title (for example "SEC-01 Protect the moderator pages").
3. Create a branch from `development` named in the team's usual style: issue number, a hyphen, your username (for example `101-sread`).
4. Write a test that fails because of the problem.
5. Fix the problem.
6. Check that the test passes and that the "Done when" column is true.
7. Open a pull request into `development` and ask for a review.

One task, one branch, one pull request. Small changes are easy to review and easy to undo.

## 2. The application as it stands

| Item | What we found |
| --- | --- |
| Framework | Django, with four apps: `account` (sign-up, sign-in, profiles, "Create Post"), `mapViewer` (map, posts, comments), `boiler` (About and Help pages, contact form), `Janitor` (moderator pages, served at `/admin/`). Django's own admin is at `/DJadmin/`. |
| Sign-in | Two home-made routes, neither using Django's `User` model: Google Sign-In (`authG`) and a username and password form backed by the `AccountCreation` table. The signed-in member's ID and rank are kept in the session. |
| Ranks | `Member.ranking`: -1 banned, 1 member, 2 trusted member, 98 moderator, 99 admin. |
| Database | SQLite file (`db.sqlite3`, ignored by git). |
| Third parties | Google Maps JavaScript, Places and Geocoding APIs; Google Sign-In; Boxicons loaded from `unpkg.com`. |
| Hosting | Two set-ups that disagree: Google App Engine (`app.yaml`, Python 3.9) and an Azure Web App workflow (Python 3.9, deploys on every push to `main`). |
| Personal data | Names, email addresses, usernames, passwords, profile photographs, "about" text, posts with street addresses and map coordinates, comments, contact messages, reports about posts and members. |
| Front end | Server-rendered templates; 6,144 lines of hand-written CSS in 13 files; a little JavaScript. |
| Tests | 38 test functions (28 in `account`, six in `boiler`, four in `mapViewer`, none in `Janitor`). 36 pass and two fail, because the pages changed and the tests did not. Nothing runs them automatically. |

## 3. Findings

Severity: **Critical** (fix before the site is used by the public again), **High**, **Medium**, **Low**.

### 3.1 Security

| ID | Severity | Finding | Where |
| --- | --- | --- | --- |
| F-S1 | Critical | **The moderator pages have no lock on the door.** No view in `Janitor/views.py` checks who is asking; the only check is in the template (`AdminBase.html` shows the page body when the rank is above 1). So a signed-out visitor sees an empty page, but the view still *acts* on anything they send. Confirmed on a local copy: without signing in, we added a tag, cleared the reports on a post and created a new member with rank 99 (admin) through `/admin/member/1`. The template check also lets a "trusted member" (rank 2) read every contact message, with names and email addresses, and reach "Manage Users" by typing its address. Hiding content in a template is not access control. | `Janitor/views.py`, `Janitor/forms.py` |
| F-S2 | Critical | **Passwords are stored as plain text.** `AccountCreation.password` holds the password exactly as typed, `confirmpassword` holds a second copy, sign-in compares with `!=`, and Django's admin shows both fields to staff. Anyone who obtains the database (or a backup) has every member's password, and people reuse passwords. | `account/models.py`, `account/views.py`, `account/admin.py` |
| F-S3 | Critical | **Secrets are in the repository.** The Django `SECRET_KEY` is in `settings.py`; a Google API key is typed into `mapViewer/forms.py` and three templates; three documentation files hold email and manager credentials. Git remembers everything, so these stay exposed even after the lines are deleted. (Status: branch `sec-00-secrets` already removes them from the code; the keys still need rotating. See SEC-00.) | `settings.py`, `forms.py`, templates, `Documentation/` |
| F-S4 | Critical | **`DEBUG = True`** in the only settings file. On a live site, any error page then shows source code, settings and request data to the visitor. | `settings.py` |
| F-S5 | High | **Stored cross-site scripting (XSS) on the map.** The post `title` and `description` are pasted into the map pop-up as HTML (`<h3>${title}</h3>`). A post titled `<img src=x onerror=...>` would run the attacker's script in every visitor's browser. Django's templates escape text for us; a JavaScript template string does not. | `mapViewer/static/mapViewer/map-script.js` |
| F-S6 | High | **A banned member still counts as signed in.** Views treat `rank == 0` as "signed out", so a rank of -1 passes. The rank is also copied into the session at sign-in, so banning or demoting someone does nothing until their session ends. | `account/views.py`, `mapViewer/views.py` |
| F-S7 | High | **Accounts are joined by email address alone.** Password sign-in runs `Member.objects.get_or_create(email=...)`, sign-up does not prove that the person owns the address, and Google sign-in does not check `email_verified`. An approved sign-up that uses someone else's email is handed that person's `Member` record. | `account/views.py` |
| F-S8 | High | **Several moderator and API views are broken** (confirmed: `/admin/member/` and `/api/get-posts-and-tags/` both answer 500). `member_manage` writes `form.is_valid` without brackets (always true) and builds the form without `instance=`, so it would create a new member instead of editing one. `memberList` and `pendingPostList` filter on `isVisible`, and `get_posts_and_tags` on `visiblity`; neither field exists (it is `visibility`). `reportList` trusts the `pk` it is sent and prints report data to the log. | `Janitor/views.py`, `mapViewer/views.py` |
| F-S20 | High | **Known vulnerabilities in pinned packages.** `pip-audit` reports 87 advisories across seven of the 17 pinned packages: Pillow 12.1.1 (58), urllib3 2.2.3 (eight), pyasn1 0.5.0 (eight), sqlparse 0.5.3 (six), requests 2.31.0 (three), certifi 2023.7.22 (two) and idna 3.4 (two). Pillow matters most, because it opens images that strangers upload. `python-dotenv` is not pinned at all. | `requirements.txt` |
| F-S21 | High | **A signed-out visitor can make the server call Google.** A POST to the map page runs the form's geocoding (with the hard-coded key) before anything checks who is asking, then crashes with a 500. Each call can cost money and uses up quota. The scan also showed that Google currently refuses the key ("You must enable Billing"), so creating a post through this route cannot work for anyone. | `mapViewer/views.py`, `mapViewer/forms.py` |
| F-S9 | High | **The pinned Django cannot run on the configured Python.** `requirements.txt` pins Django 5.2, which needs Python 3.10 or later; `app.yaml` and the Azure workflow both ask for 3.9. A whole virtual environment (5,381 files, with Django 4.2.6 inside) is committed too, so it is unclear which Django anyone is really running. | `requirements.txt`, `app.yaml`, workflow, `cccSite/venv/` |
| F-S10 | High | **Data will not survive on the planned host.** SQLite and uploaded photographs are written to the local disk. App Engine's disk is read-only apart from a temporary folder, and both hosts can replace the machine at any time. Members' data would vanish, with no backup. | `settings.py`, `app.yaml` |
| F-S11 | Medium | **Hidden posts still accept actions.** In `post_detail`, the report and comment code runs before the visibility check, so anyone who guesses an ID can comment on or report a pending or denied post. The report form also trusts a hidden `post` field, so a report can be filed against any post ID. | `mapViewer/views.py`, `Janitor/forms.py` |
| F-S12 | Medium | **`MakePostForm` is faulty.** It declares a model `ImageField` inside a form (it does nothing), reads `cleaned_data['media_file']` (which does not exist), leaves `geoResult` unset when the browser supplies one, overrides Django's private `_clean_form`, and prints the geocoder's answer to the log. A map POST from a signed-out visitor crashes on `request.session['user']`. Any JSON the browser sends as `geoResult` is stored as the post's location. | `mapViewer/forms.py`, `mapViewer/views.py` |
| F-S13 | Medium | **No protection against guessing.** Sign-in, sign-up, contact and report forms have no rate limit or lock-out. Sign-up accepts any password (Django's password validators are configured but never called). | `account/views.py` |
| F-S14 | Medium | **Browser protections are missing.** No Content-Security-Policy, no HSTS, no `Secure` flag on cookies, and the Google sign-in address is hard-coded as `http://localhost:8080/account/authG/`. `SECURE_REFERRER_POLICY` is set to `same-origin-no-downgrade`, which is not a real value; Django's deployment check reports it as an error and browsers ignore the header. The CSRF cookie lasts a year. | `settings.py`, `signin.html` |
| F-S15 | Medium | **Uploads are lightly checked.** No size limit; the profile photograph keeps the file extension the browser sent; photographs keep their EXIF data (which can include GPS position); `file1` to `file4` on "Create Post" are accepted and then silently dropped; `MEDIA_URL` has no leading slash; uploaded files are served by a helper that only works in debug mode. | `account/models.py`, `account/forms.py`, `settings.py`, `urls.py` |
| F-S16 | Medium | **Sessions.** The session key is not changed at sign-in (session fixation), there is no idle time-out, and the sign-in link carries a `?next=` value that nothing reads (when we do read it, it must be checked, or it becomes an open redirect). | `account/views.py` |
| F-S17 | Medium | **The Google sign-in view is `csrf_exempt`.** The double-submit check it performs is the right idea, but it has no tests, answers failures with bare strings, and the client ID is typed into the view and the template. | `account/views.py` |
| F-S18 | Low | **Django admin search is broken** (`author__username` and `author__displayname` do not exist on `Member`), and the admin sits at a guessable address with no two-step sign-in. | `mapViewer/admin.py`, `urls.py` |
| F-S19 | Low | **No audit trail, no dependency scanning, no `security.txt`.** The Azure workflow uses old action versions (`checkout@v2`, `setup-python@v1`) and deploys without running tests. | repository |

### 3.2 Accessibility (WCAG 2.1 AA)

The repository already holds `CCC ADA Compliance Report Working Document.md` (in the FA24 documentation). We start from it, but re-test every page, because the templates have changed a great deal since.

| ID | WCAG criterion | Finding |
| --- | --- | --- |
| F-A1 | 3.1.1 Language of Page | `<html>` has no `lang` attribute. |
| F-A2 | 1.4.10 Reflow, 1.4.4 Resize Text | No `<meta name="viewport">` in `base.html`, so phones show a shrunken desktop page. There are 22 media queries, but they cannot work properly without it. |
| F-A3 | 2.4.1 Bypass Blocks | No "Skip to main content" link. |
| F-A4 | 1.3.1 Info and Relationships | No `<main>` in the base template; some pages add `<div role="main">`, others have no main landmark at all. `<nav>` has no name. `id="smcm-logo"` is used twice on every page. Some pages have two `<h1>` headings (sign-in), and the post page builds its layout from `<br>` tags. |
| F-A5 | 2.4.2 Page Titled | `<title>` is supplied page by page through the `head` block, so any page that forgets has none; the post page is titled "Map". |
| F-A6 | 1.1.1 Non-text Content | The header image's text alternative says "SMCM Logo" but the image is the College seal. The map has no text alternative announced as such (there is a helpful "Upload descriptions" list under it, which we keep and improve). Icons on the map page lack `aria-hidden`. |
| F-A7 | 1.2.2 Captions (Prerecorded) | The tutorial video on the Help page has no captions and no transcript. |
| F-A8 | 1.4.3 Contrast, 1.4.11 Non-text Contrast | Not yet measured. The stylesheets use 74 different hex colours and 249 `rgb()`/`rgba()` values, many of them greys and translucent layers over gradients, where contrast cannot be guaranteed. The College standard is stricter than WCAG: 4.5:1 for all text, with no large-text exception. |
| F-A9 | 2.4.7 Focus Visible | Seven rules remove the focus outline (`outline: none`); each needs a visible replacement. |
| F-A10 | 2.1.1 Keyboard, 2.4.3 Focus Order | The account menu (`<details>`), the comment and report panels, the accordions on "My Forums" and the five-step "Create Post" wizard all need keyboard testing. The wizard must move focus to each new step. Map pins must be reachable by keyboard. |
| F-A11 | 3.3.1 Error Identification, 3.3.3 Error Suggestion, 4.1.3 Status Messages | Errors appear as a plain paragraph (`<p class="help is-danger">`) that is not announced and not tied to a field. |
| F-A12 | 1.3.5 Identify Input Purpose | The sign-up form sets `autocomplete="off"` on email, username and display name. Fields that ask for personal data must carry the correct `autocomplete` value so that browsers and assistive tools can fill them in. |
| F-A13 | 3.3.2 Labels or Instructions | The comment box has an empty label (`label=""`) and relies on placeholder text; the map search box relies on a placeholder. Placeholders vanish as you type and usually fail contrast. |
| F-A14 | 1.4.1 Use of Colour | The current page in the menu is marked by colour alone (an inline gold background). Post status (visible, pending, denied) must not depend on colour. |
| F-A15 | 2.3.3, 2.2.2 Motion | 46 animation or transition rules, with only two `prefers-reduced-motion` blocks. |
| F-A16 | 1.4.12 Text Spacing, 1.4.4 | 32 font sizes are fixed in pixels; text should scale with the reader's settings (`rem`). |
| F-A18 | 4.1.1 Parsing, 4.1.2 Name, Role, Value, 1.3.1 | Found by axe-core: five form controls on the map page have no label (rated critical); the About page has no `<title>`; the profile page has a malformed definition list; the Reports page nests one interactive control inside another; the post page repeats the ID of a focusable control when signed in. axe could not decide colour contrast for between six and 35 elements on every page (text over gradients and translucent layers), which supports F-A8. |
| F-A17 | 2.4.4 Link Purpose | Links such as "See More" in map pop-ups mean nothing out of context. An emoji (⚠️) is used as an icon and is read aloud. |

### 3.3 Privacy (GDPR)

GDPR applies when we handle personal data of people who are in the EU or the UK. Whether CCC legally falls under it is a question for the College's counsel. This plan builds to the GDPR standard anyway; it is good practice, and it is far cheaper to build in now than to bolt on later.

| ID | Finding |
| --- | --- |
| F-G1 | **No privacy notice.** Nothing tells people who is responsible for their data, why we collect it, how long we keep it, who else receives it, or what their rights are (Articles 12 to 14). |
| F-G2 | **No recorded lawful basis** for any of the processing (Article 6), and no record of processing activities (Article 30). |
| F-G3 | **Visitors' data goes to third parties before they do anything** (confirmed: loading the map page contacted `unpkg.com`, `maps.googleapis.com` and `maps.gstatic.com`, and a Google cookie, `g_state`, appeared beside our own `csrftoken`). Every page loads Boxicons from `unpkg.com`; the map, post list and sign-in pages load Google scripts. Each sends the visitor's IP address and browser details to a US company, without notice or consent. |
| F-G4 | **We collect more than we need** (Article 5). We store the password twice. "Create Post" asks for first name, last name and a full street address, then discards the names. The whole of Google's geocoding answer is stored for each post. A post may pin someone's home on a public map. |
| F-G5 | **People cannot exercise their rights.** No "download my data" (Articles 15 and 20; `exportData` says "Not implemented yet"). No "delete my account" (Article 17). No way to hide oneself from the public Contributors list or to object (Article 21). |
| F-G6 | **Nothing is ever deleted.** Rejected sign-up requests (with their plain-text passwords), contact messages, reports, denied posts and old sessions are kept for ever. There is no retention schedule. |
| F-G7 | **Personal data is committed to the repository.** A member's profile photographs (`cccSite/cccSite/media/users/1/`), audio recordings of client meetings (`.m4a` files) and meeting notes that name individuals are all in git. |
| F-G8 | **Profile pages are public.** `/account/view/<id>` shows a member's name, photograph and "about" text to anyone, signed in or not, although the Contributors list asks visitors to sign in first. Members are not told this at sign-up. |
| F-G9 | **Personal data is written to logs** (`print(uList)`, `print(geoResult)`), and debug error pages would display it. |
| F-G10 | **No breach procedure** (Articles 33 and 34), no data-protection impact assessment, no processor agreements with Google or the host, and the hosting region is undecided (international transfers, Chapter V). |
| F-G11 | **No consent record or age check at sign-up.** |
| F-G12 | **Security of processing (Article 32)** fails on the findings in 3.1, above all F-S1 and F-S2. A plain-text password table is a reportable breach waiting to happen. |

Cookies: Django's session cookie and CSRF cookie are "strictly necessary", so they need a clear notice but not consent. Google's scripts may set their own; GDPR-03 deals with that.

### 3.4 Code and CSS health

| ID | Finding |
| --- | --- |
| F-C1 | **Generated and personal files are committed.** `cccSite/venv/` (5,381 files); `cccSite/static/` (the output of `collectstatic`, including all of Django admin's files and a second copy of every stylesheet); `assets 2/`; an empty directory `cccSite/ChesapeakeCommunityConnect/`; an editor cache in `.vscode/`. |
| F-C2 | **Unused files.** No view renders `viewForum.html`, `post_form.html`, `signedout.html` or `signout.html`; `forumview.js` is loaded only by `viewForum.html`; no template loads `map-script2.js`. Confirm each, then delete. |
| F-C3 | **Duplicates.** `accordian.css` (misspelt) exists twice with identical content. `MessageForm` is defined in two apps with different meanings. The `help` and `contact` views are copies. Posts are created by two separate code paths (`viewMap` and `create_forum`). `Documentation/` holds two copies of many files. |
| F-C4 | **CSS is large and inconsistent.** `accountBasestyle.css` is 2,431 lines and is loaded on every account page; `create_forumstyle.css` is 1,189 lines. There are 74 distinct hex colours, 58 gradients, 249 `rgb()`/`rgba()` values, 37 `!important` declarations, 15 inline `style="..."` attributes and seven `<style>` blocks inside templates. Three naming styles are mixed (`nameField`, `containerS1`, `dir-search__bar`). An off-brand orange (`#e67e22`) is used for hover. Baskerville is set as a web font. |
| F-C5 | **Branding.** The header uses the College seal, which the brand rules reserve; gradients conflict with the "solid colours only" rule; the footer reads "SMCM Capstone Website". |
| F-C6 | **Python style.** Star imports (`from .models import *`) hide where names come from. There are unused imports, forms defined in `models.py`, a form class that cannot work (`CreateAccountForm` passes `user=` to a model with no such field), leftover `print` calls, commented-out code, and `get_absolute_url` declared as a property (Django expects a method). Comments exist and many are helpful, but they are fragments rather than docstrings, and some record guesses ("initializes (?) the google API"). |
| F-C7 | **Names that mislead.** `AccountCreation` is really a sign-up request that doubles as the password store. `Janitor` is the moderator area and lives at `/admin/`, while the real Django admin lives at `/DJadmin/`. `boiler` holds the About and Help pages. "Forum", "post" and "upload" all mean the same thing. Being honest about this in comments (and renaming where cheap) will save the next team hours. |
| F-C8 | **Set-up documents overlap and disagree** (`README.md`, `CCCSetupInstructions.md`, `RUN_DEV_SERVER.md`, `GoogleCloudAndVSCodeInstructions.md`, several guides under `Documentation/`). `update_maptags.py` is a loose script that should be a data migration. |

## 4. Security work

Simon says: don't write your own sign-in or password code, even though you'll see it done here; you'll mess it up. Django already has a tested `User` model, password hashing, sign-in, sign-out, password reset and permission checks. Wherever a task below offers a choice, prefer Django's own tool.

### Phase 0: emergency (before anything else)

| ID | Task | Done when |
| --- | --- | --- |
| SEC-00 | **Rotate every exposed secret.** Merge branch `sec-00-secrets` (it moves the Django key and the Maps key to environment variables, deletes the credential documents and adds `Documentation/Security/secret-rotation-checklist.md`). Then follow that checklist: new restricted Google keys, delete the old key, new `DJANGO_SECRET_KEY`, change the mailbox and manager passwords. Decide whether to rewrite git history. | The old keys and passwords no longer work. `git grep AIza` finds nothing. |
| SEC-01 | **Lock the moderator pages.** Write one decorator, `moderator_required`, that loads the signed-in `Member` from the database (not the session's copy of the rank) and refuses anyone below rank 98. Put it on every view in `Janitor/views.py`. Remove `ranking` from the member form for moderators; only an admin (99) may change a rank. | Tests show that a signed-out visitor, a member and a banned member each get a refusal from every `/admin/...` address, for both GET and POST. |
| SEC-02 | **Turn debug off by default.** Read `DEBUG`, `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` from environment variables; `DEBUG` is false unless a developer sets it. Add friendly 403, 404 and 500 pages. | `python manage.py check --deploy` passes with production settings. |
| SEC-03 | **Fix the map XSS.** Build the pop-up with DOM calls (`document.createElement`, `textContent`) instead of an HTML string. | A test post titled `<script>alert(1)</script>` shows as text on the map, the post page and the list. |
| SEC-04 | **Take the site out of public use until SEC-00 to SEC-03 and SEC-10 are merged,** if it is currently deployed anywhere. | Project owner confirms. |

### Phase 1: accounts and permissions

| ID | Task | Done when |
| --- | --- | --- |
| SEC-10 | **Hash passwords.** Preferred: move members to Django's `User` model (link `Member` to `User` one-to-one) and use `authenticate()` and `login()`. Minimum: store `make_password()` output and compare with `check_password()`. Either way: delete the `confirmpassword` column; write a migration that hashes or discards every stored password; make every password-account holder choose a new password; hide the field in Django admin; call `validate_password()` at sign-up and on change (minimum 12 characters). | No readable password in the database. Tests cover sign-up, sign-in, wrong password and change password. |
| SEC-11 | **One helper decides who is signed in.** `current_member(request)` returns the live `Member`, or `None` when nobody is signed in or the member is banned. Add `member_required` beside `moderator_required`. Replace every `request.session.get('rank', 0)` test. Stop storing the rank and name in the session. | A banned or demoted member loses access on their next request (test). |
| SEC-12 | **Stop joining accounts by email.** Create the `Member` when a sign-up is approved and link it by ID. Send a confirmation link to prove the address at sign-up. Require `email_verified` from Google. Link a Google identity to an existing member only after that member signs in with their password. Make usernames and emails unique in the database. | Signing up with a stranger's email gives no access to the stranger's account (test). |
| SEC-13 | **Check visibility first.** In `post_detail`, return "not found" for pending or denied posts unless the visitor is the author or a moderator, before handling any POST. Take the post ID for a report from the URL, not from a hidden field. Use `get_object_or_404`. | Tests for visible, pending and denied posts as visitor, author and moderator. |
| SEC-14 | **One way to create a post.** Remove post creation from `viewMap` (this also closes F-S21; do that part in phase 0); keep `create_forum`. Rewrite `MakePostForm`'s geocoding as a normal `clean()` or delete the form. Geocode on the server and store only latitude, longitude and a display label. Trusted members (rank 2 and above) are auto-approved in one place. | Posting works only when signed in; malformed location data is rejected (tests). |
| SEC-15 | **Repair the moderator views** listed in F-S8, add a real pending-post queue (approve or deny, with a reason), and delete the `print` calls. Fix the Django admin search fields. | Every moderator view has at least one passing test. |
| SEC-16 | **Sessions.** Call `request.session.cycle_key()` at sign-in (Django's `login()` does this for us), set an idle time-out, honour `?next=` only after `url_has_allowed_host_and_scheme()` approves it. | Session ID changes at sign-in; `?next=https://evil.example` is ignored (tests). |
| SEC-17 | **Slow down guessing.** Add `django-axes` (or `django-ratelimit`) to sign-in, and rate limits plus a hidden "honeypot" field to sign-up, contact, comment and report forms. | The sixth wrong password within a minute is refused (test). |
| SEC-18 | **Audit log.** Record who did what and when for: sign-in, failed sign-in, rank change, post approval or denial, deletion, data export. No message text, no passwords. | Entries appear for each event; retention set by GDPR-06. |

### Phase 2: hardening and operations

| ID | Task | Done when |
| --- | --- | --- |
| SEC-20 | **One host, one Python.** Choose App Engine or Azure and delete the other's configuration. Use Python 3.12 everywhere (host, workflow, local). Deploy only from `main`, only after tests pass, with current action versions and secrets in the host's secret store. | A written, repeatable deployment that a new student can follow. |
| SEC-21 | **A real database and file store.** PostgreSQL (managed by the host) for data; a storage bucket (through `django-storages`) for uploads; automatic encrypted backups; a restore rehearsed and written down. Choose the hosting region with GDPR-02 in mind. | Data and photographs survive a redeploy; a restore has been practised. |
| SEC-22 | **Transport and cookies.** `SECURE_SSL_REDIRECT`, HSTS (start with one hour, then raise), `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SameSite=Lax`, `X_FRAME_OPTIONS = "DENY"`, `SECURE_REFERRER_POLICY = "same-origin"`, a `Permissions-Policy` header. Set the Google sign-in address from settings. Remove the stray `global_settings` import. | Mozilla Observatory grade of A or better. |
| SEC-23 | **Content-Security-Policy** with `django-csp`: our own origin plus the Google hosts we need, no inline script or style. This depends on CSS-08 (moving inline code out of templates). Run it in report-only mode first. | A full test run produces no violations; then switch to enforcing. |
| SEC-24 | **Uploads.** Limit size (2 MB for photographs); open each image with Pillow and save a fresh copy (this validates it and strips EXIF); give files random names; either build `file1` to `file4` properly with an allow-list of types or remove them from the form. | Tests: a script renamed `.jpg`, an oversized file and a photograph with GPS data. |
| SEC-25 | **Dependencies.** Remove `cccSite/venv/` from git (CLN-01). Pin exact versions with hashes (`pip-compile`), including `python-dotenv`. Update the seven packages in F-S20 to at least: Pillow 13.0.0, urllib3 2.8.0, pyasn1 0.6.5, sqlparse 0.6.0, requests 2.33.0, certifi 2026.10.18, idna 3.15. Run the tests afterwards. Turn on Dependabot and add `pip-audit` to the checks. Do the Pillow update in phase 0. | `pip-audit` reports nothing. |
| SEC-26 | **Google sign-in.** Client ID from settings; tests with a fake token verifier for: no cookie, mismatched token, invalid token, unverified email, success; errors logged and shown on a proper page. | Five passing tests. |
| SEC-27 | **Django admin.** Limit staff accounts to named people, add two-step sign-in (`django-otp`), and document how an admin account is created. | Reviewed by the project owner. |
| SEC-28 | **Scan and report.** `bandit`, `ruff` security rules, `manage.py check --deploy`, and an OWASP ZAP baseline scan against a staging copy. Add `/.well-known/security.txt` and a "Reporting a vulnerability" section to the README. | Reports stored under `Documentation/Security/`; no High findings open. |

## 5. Accessibility work

Target: every page, signed in or not, conforms to WCAG 2.1 level AA, and all text meets 4.5:1 contrast. Automated tools find perhaps a third of accessibility problems. A person with a keyboard and a screen reader finds the rest; do both.

| ID | Task | Criteria | Done when |
| --- | --- | --- | --- |
| A11Y-01 | **Rebuild `base.html`.** `lang="en"`; viewport meta tag; a `{% block title %}` inside a `<title>` that always ends "Chesapeake Community Connect"; a skip link as the first focusable element; `<header>`, `<nav aria-label="Main">`, one `<main id="main">` around the content block, `<footer>`; no duplicate IDs. Remove `role="main"` from child templates. Make `AdminBase.html` and `accountBase.html` extend it properly. | 1.3.1, 2.4.1, 2.4.2, 3.1.1, 1.4.10 | axe reports no landmark, title, language or duplicate-ID problems on any page. |
| A11Y-02 | **Give every page a unique title and one `<h1>`**, with headings in order (no jumping from `h1` to `h3`). Replace layout `<br>` tags with real structure (paragraphs, lists, a "Topics" list for tags). | 1.3.1, 2.4.2, 2.4.6 | Heading outline checked for each page. |
| A11Y-03 | **Colour and contrast.** Build the palette as tokens (CSS-02), then write a small script that checks every text and background pair in the tokens. Remove text over gradients and translucent layers. Text: 4.5:1 at every size. Borders of inputs, icons that carry meaning and focus rings: 3:1. Never dark grey on white, nor red or dark grey on navy. | 1.4.3, 1.4.11 | Contrast report saved in `Documentation/Accessibility/`; no failures. |
| A11Y-04 | **Visible focus.** One global `:focus-visible` style (a 3 px ring that contrasts with both navy and white). Delete the seven `outline: none` rules or pair each with a replacement. | 2.4.7 | Every interactive element shows focus when reached with Tab. |
| A11Y-05 | **Navigation.** Mark the current page with `aria-current="page"` and style that attribute with more than colour (an underline or bar). Make the account menu work with Enter, Space and Escape, and close when focus leaves it. Make the menu usable at 320 px width. | 1.4.1, 2.1.1, 4.1.2 | Keyboard and screen-reader check. |
| A11Y-06 | **Forms.** Render every form through one shared field template: a visible `<label>`, a hint, the error text linked with `aria-describedby`, `aria-invalid` when wrong, "required" stated in words. Show an error summary with `role="alert"` at the top and move focus to it. Use correct `autocomplete` values (`email`, `username`, `name`, `current-password`, `new-password`); remove `autocomplete="off"`. No placeholder-only labels (comment box, map search). | 1.3.1, 1.3.5, 3.3.1, 3.3.2, 3.3.3, 4.1.3 | Each form completed with NVDA and with VoiceOver. |
| A11Y-07 | **The map.** Label the map region; keep the text list of posts beside it and make each entry a link to its post; add a "Skip the map" link; make pins keyboard-operable (`gmpClickable` on Advanced Markers) with a named pop-up whose link reads "Read more about {title}"; announce the number of results after filtering in a polite live region. | 1.1.1, 2.1.1, 2.4.4, 4.1.3 | Every post can be found and opened without using the map. |
| A11Y-08 | **"Create Post" wizard.** `<fieldset>` and `<legend>` for each radio or checkbox group; "Step 2 of 5" announced; focus moves to the step heading; Back keeps what was typed; errors take the user to the right step; address autocomplete usable by keyboard; a review step before submitting. | 1.3.1, 2.4.3, 3.3.4, 4.1.3 | A post created start to finish with the keyboard only, and again with a screen reader. |
| A11Y-09 | **Posts and comments.** Proper buttons for "Comment", "Reply" and "Report"; a labelled comment box; nested replies marked up as nested lists; dates as text ("Oct. 22, 2026") rather than only "3 days ago"; status messages announced. | 1.3.1, 4.1.2, 4.1.3 | Screen-reader check of a threaded discussion. |
| A11Y-10 | **Video.** Captions (`<track kind="captions">` with a WebVTT file) and a transcript for the tutorial video; no autoplay. Any video members may add later needs the same rule. | 1.2.2, 1.2.3, 1.2.5 | Captions match the audio. |
| A11Y-11 | **Images and icons.** Real text alternatives; `alt=""` for decoration; `aria-hidden="true"` on every icon, with visible text or an accessible name beside it; no emoji as icons; replace the seal with the official College logo file and describe it as "St. Mary's College of Maryland". | 1.1.1 | No `<img>` without `alt`; icon audit complete. |
| A11Y-12 | **Zoom, reflow and spacing.** Sizes in `rem`; no horizontal scrolling at 320 px wide; nothing lost at 200% zoom or with the WCAG text-spacing settings; tap targets at least 24 by 24 px (aim for 44). | 1.4.4, 1.4.10, 1.4.12 | Checked at 320, 768 and 1280 px. |
| A11Y-13 | **Motion.** One `prefers-reduced-motion` rule that switches off all animation and transitions; nothing moves for more than five seconds without a pause control. | 2.2.2 | Checked with the operating system's "reduce motion" setting. |
| A11Y-14 | **Moderator pages too.** Tables with header cells and captions; confirmation before destructive actions; the same base template. Staff have the same right to an accessible tool. | all | Same checks as public pages. |
| A11Y-15 | **Automatic checks.** Add axe-core (through Playwright) to the checks, visiting every address both signed out and signed in; fail the build on any violation. Keep a short manual script (keyboard, NVDA, VoiceOver, zoom) for each release. | all | The check runs on every pull request. |
| A11Y-16 | **Accessibility statement** page: the standard we meet, known gaps, how to report a problem, and how quickly we answer. Linked from the footer. | n/a | Published. |

## 6. Privacy work (GDPR)

The College is the "controller" (the organisation that decides why and how data is used). The team prepares the features and the evidence; the College's privacy officer or counsel approves the decisions. Tasks marked (decision) need that approval before code is written.

| ID | Task | Done when |
| --- | --- | --- |
| GDPR-01 | **Data map.** One table listing every piece of personal data: where it is stored, why we need it, who can see it, where it is sent, how long we keep it. Include logs, backups, the host and Google. | `Documentation/Privacy/data-map.md` approved. |
| GDPR-02 | **Lawful basis and records (decision).** Record a basis for each purpose (likely "contract" for accounts and posts, "legitimate interests" for moderation, security logs and the contact form, "consent" for optional third-party content). Write the Article 30 record. Carry out a data-protection impact assessment, because we publish locations linked to named people. Choose the hosting region and the transfer safeguard. Sign processor terms with the host and Google. | Signed-off documents in `Documentation/Privacy/`. |
| GDPR-03 | **No third-party requests without a choice.** Serve Boxicons (or better, a handful of inline SVG icons) from our own site. Show the map behind a "Show the map (loads Google Maps)" button, remembered for the session, with the text list always available. Load the Google sign-in script only when the visitor chooses "Sign in with Google". | Loading any page makes no request to another company until the visitor clicks (checked in the browser's network panel and by a test). |
| GDPR-04 | **Privacy notice and cookie notice.** Plain-language pages linked from the footer and from every form that collects data: who we are and how to contact us, what we collect and why, the lawful basis, who receives it, transfers abroad, how long we keep it, each right and how to use it, how to complain to a supervisory authority. List the two necessary cookies. Keep a version number. | Published; approved. |
| GDPR-05 | **Collect less.** Drop `confirmpassword` (SEC-10). Remove first and last name from "Create Post". Ask for a place name or organisation address, warn against entering a home address, and offer "show approximate location". Store latitude, longitude and a label only. Make "about" and the photograph clearly optional and clearly public. Ask whether the contact form needs a name at all. | Forms, models and data map updated; old extra data deleted by migration. |
| GDPR-06 | **Retention, enforced by code (decision on the numbers).** Proposed: rejected sign-up requests, 30 days; approved requests, deleted once the account exists; contact messages, 12 months; resolved reports, 12 months; denied posts, 90 days; audit log, 12 months; server logs, 30 days; backups, 35 days; expired sessions, cleared nightly; accounts unused for three years, warned by email and then deleted. Implement as a management command run daily. | The command is tested and scheduled; the numbers appear in the privacy notice. |
| GDPR-07 | **Download my data.** A button on the account page that produces a ZIP of JSON files (profile, posts, comments, consent record) plus the photograph. Replace the `exportData` stub. | A member can download everything we hold about them (test). |
| GDPR-08 | **Delete my account.** Re-enter the password (or re-confirm with Google), read a clear warning, confirm. Delete the member, their sign-in records, photograph file, sessions and reports about them. Decide (decision) whether their posts and comments are deleted or kept under "former member"; replies by other people should survive either way. Write down how a moderator handles a request that arrives by email, and the one-month deadline. | An end-to-end test finds no trace of the member in the database or the file store. |
| GDPR-09 | **Control over visibility.** Profile pages follow the same rule as the Contributors list (signed-in members only, unless the College decides otherwise). Add "Show me in the Contributors list" (off until chosen). Say at sign-up exactly what will be public. | Settings exist and are tested. |
| GDPR-10 | **Sign-up record.** An unticked box, "I have read the privacy notice", with a link; store the date and the notice version. Add an age statement if counsel asks for one. Tell existing members when the notice changes. | Sign-up is impossible without it (test). |
| GDPR-11 | **Clean the repository.** Remove members' photographs, meeting recordings and any notes that name private individuals from git (and from history if the repository is public); keep such material in the College's access-controlled storage. Add `media/` to `.gitignore`. | `git ls-files` shows no personal files. |
| GDPR-12 | **Clean logs.** No names, emails, addresses, message text or tokens in logs. Replace `print` with the `logging` module. Log member IDs, not emails. | Log review passed. |
| GDPR-13 | **Breach procedure.** One page: how to recognise a breach, who to tell at once, how to contain it, who decides on notifying the authority (within 72 hours) and the people affected, where it is recorded. Practise it once. | Approved; rehearsal noted. |
| GDPR-14 | **Moderation transparency.** Tell members that reports about them are stored, how long for, and that they can ask to see the substance. Give the reason when a post is denied. | In the notice and the moderator guide. |

## 7. Clean-up work

### 7.1 Repository

| ID | Task | Done when |
| --- | --- | --- |
| CLN-01 | Remove `cccSite/venv/` from git (`git rm -r --cached`); it is already in `.gitignore`. Each developer creates their own virtual environment. | No `venv` path in `git ls-files`. |
| CLN-02 | Stop committing `collectstatic` output. Set `STATIC_ROOT = BASE_DIR / "staticfiles"`, ignore it, delete the tracked `cccSite/static/`, remove the duplicate `STATICFILES_DIRS` lines, and serve static files with WhiteNoise. | Exactly one copy of each stylesheet in git. |
| CLN-03 | Delete `assets 2/`, the empty `cccSite/ChesapeakeCommunityConnect/`, `.github/workflows/.gitignore`, `Issue branch Instructions.txt` (after merging it into the contributing guide) and the unused templates and scripts from F-C2. | Tree reviewed. |
| CLN-04 | **One set of instructions.** A single `README.md`: what the project is, how to run it, how to test it, how to deploy it, where the documents are. Merge the other set-up files into it and delete them. Write for a beginner: numbered steps, one action per step. Remove the duplicate `Documentation/Google Drive/` tree after checking that `Sorted Documents (SP25)/` has everything. | A new student gets the site running from the README alone, timed. |
| CLN-05 | **Tooling.** `pyproject.toml` (ruff and black), Stylelint, ESLint (a config already exists), djLint for templates, `pre-commit`, `.editorconfig`, and a `CONTRIBUTING.md` that holds the conventions in this plan. | `pre-commit run --all-files` passes. |
| CLN-06 | **Continuous integration.** A GitHub Actions workflow on every pull request: install, `manage.py check`, migrations check, tests with coverage, linters, `pip-audit`, axe. Protect `main` and `development` so that a pull request cannot merge while the checks fail. | A red check blocks merging. |

### 7.2 CSS

A stylesheet is like a shared wardrobe. Today everyone has stuffed clothes in wherever there was room, in 74 slightly different shades. We are going to sort it into labelled drawers, so that the next person can find the socks.

Palette (solid colours only): SMCM Blue `#00205C` (primary); gold `#F3C10D` and white (secondary); red `#D0343A`, light blue `#59B7E2`, dark grey `#847870`, light grey `#D6D1CA` (tertiary, only beside blue or gold). Font: Arial, with a system sans-serif fallback.

| ID | Task | Done when |
| --- | --- | --- |
| CSS-01 | **Take stock before changing anything.** Screenshot every page in every state (signed out, signed in, errors, empty lists) at 320, 768 and 1280 px with Playwright; these are the "before" pictures. List which templates load which stylesheet. Use the browser's Coverage tool to list selectors that never match. | `Documentation/Css/inventory.md` and a screenshot set exist. |
| CSS-02 | **Tokens.** Create `tokens.css` holding CSS custom properties: the palette, then meaningful names built on it (`--color-text`, `--color-surface`, `--color-link`, `--color-focus`, `--color-danger`), the font stack, a type scale and a spacing scale in `rem`, radii, and the breakpoints (written in a comment, since custom properties cannot be used in media queries). Replace every colour literal with a token. Replace gradients and translucent overlays with solid colours. Remove `#e67e22` and the other off-palette colours. | A search for `#` colours, `rgb(` and `gradient` finds them only in `tokens.css` (and no gradients at all). |
| CSS-03 | **Structure.** In `cccSite/cccSite/static/base/`, loaded in this order: `tokens.css`, `reset.css`, `base.css` (plain elements), `layout.css` (header, menu, footer, page width), then `components/` (button, form, card, hero, accordion, pager, alert, comment, wizard), then `pages/` for anything truly unique to one page. Split the two giant files along these lines. A page loads only what it uses. | No stylesheet over about 300 lines; `accountBasestyle.css` and `create_forumstyle.css` are gone. |
| CSS-04 | **One naming rule.** BEM in lower-case with hyphens: `block`, `block__element`, `block--modifier` (the newer code already does this: `dir-search__bar`). Rename `containerS1`, `wrapperS1`, `nameField` and friends. Style classes only; never style an `id`. Classes that exist for JavaScript start with `js-` and carry no styles. Change the template and the CSS in the same commit. | Stylelint's class-name pattern passes. |
| CSS-05 | **No `!important`.** Remove all 37 by fixing the order and weight of selectors. BEWARE: `!important` is usually a sign that two rules are fighting; find the other rule rather than shouting louder. | Stylelint's `declaration-no-important` passes. |
| CSS-06 | **Remove duplicates and dead rules.** One `accordion.css` (spelt correctly). Merge repeated blocks (three different "hero" patterns, several button styles) into single components. Delete selectors that the inventory shows are unused, checking each state first. | Total CSS falls from 6,144 lines to a target of under 2,500. |
| CSS-07 | **Mobile first.** Base rules suit a narrow screen; `min-width` media queries add columns for wider ones. Use flexbox and grid rather than fixed widths and margins. | Passes A11Y-12. |
| CSS-08 | **Nothing inline.** Move all 15 `style="..."` attributes, seven `<style>` blocks and every inline `<script>` into files. The active menu link becomes a CSS rule on `[aria-current="page"]`. | A search of the templates for `style=`, `<style` and inline scripts finds nothing; SEC-23 can then be enforced. |
| CSS-09 | **Accessibility built in.** Global focus style, reduced-motion rule, a check in Windows High Contrast (`forced-colors`), minimum target sizes, no text in images. | Passes A11Y-04 and A11Y-13. |
| CSS-10 | **Comment the CSS** (see 7.4). | Review. |
| CSS-11 | **Prove nothing broke.** After each CSS pull request, take the screenshots again and attach the differences. Changes should be the ones we intended. | Before-and-after pictures on every CSS pull request. |

Critical Thinking: should we adopt a CSS framework instead? The documents mention Bulma, and a few Bulma class names survive (`help is-danger`, `field`, `label`). A framework would give us tested, accessible components quickly, but it would also mean restyling every page and overriding its colours to match the brand. Simon says: keep the hand-written CSS and tidy it; the pages are few, and learning how the cascade works is worth more to you than learning one framework's class names. Record the decision in `CONTRIBUTING.md` either way, so that the next team does not half-adopt a second approach.

### 7.3 Python, templates and JavaScript

| ID | Task | Done when |
| --- | --- | --- |
| CLN-10 | **Imports and dead code.** Replace every star import with named imports. Delete unused imports, `CreateAccountForm`, the second `MessageForm`, the `pendingPostList` and `exportData` stubs (until they are built properly), commented-out code and every `print`. | `ruff check` passes with the unused-code rules on. |
| CLN-11 | **Put things where Django expects them.** Forms in `forms.py`, not `models.py`. Permission helpers in one module. Queries that are repeated become model methods or managers (`MapPost.objects.visible()`, `MapPost.objects.search(text, tags)`; the search code is currently written twice). `get_absolute_url` becomes a method. `update_maptags.py` becomes a data migration. | Each view reads as a short story: check permission, get data, render. |
| CLN-12 | **Honest names.** Rename with migrations, one mechanical pull request each, after the security fixes are merged: `AccountCreation` to `SignupRequest`; app `Janitor` to `moderation`, served at `/moderation/`; app `boiler` to `pages`; settle on "post" (not "forum" or "upload") in code, addresses and on screen; Django admin moves from `/DJadmin/` to `/django-admin/`. | No behaviour changes in these pull requests; tests still pass. |
| CLN-13 | **Fewer database queries.** `memberList` runs three queries per member and `reportList` one per item; use `annotate()` and `prefetch_related()`. Add pagination to moderator lists and to the map's post list. Add indexes for the fields we filter on. | Query counts stay constant as data grows (a test with `assertNumQueries`). |
| CLN-14 | **Templates.** Shared pieces become includes (hero banner, form field, pager, alert, post card). Every link uses `{% url %}`. Decisions belong in views, not templates (the long `if '/about/' not in request.path and ...` test in the menu becomes a simple comparison). | No repeated markup blocks. |
| CLN-15 | **JavaScript.** One file per feature (`map.js`, `wizard.js`, `accordion.js`), loaded with `defer`, no global variables, no inline handlers, data passed with `json_script`. ESLint in the checks. | ESLint passes. |
| CLN-16 | **Tests.** First repair the two failing tests (`test_manage_view_shows_current_profile_image` and `test_signed_out_contributor_page_has_only_menu_sign_in`): decide whether the page or the test is right. Then reach at least 80% line coverage, and 100% of permission rules: for every address, a test for signed-out, member, banned, moderator and admin. Add factories for test data. | Coverage report in the checks. |

### 7.4 Commenting standard

A comment is a note to the next mechanic who opens the bonnet. They can already see *what* the engine does by looking; tell them *why* it was built this way, and what will break if they change it.

These rules go into `CONTRIBUTING.md` and apply to every file we touch.

1. **Python modules, classes and functions get a docstring.** One line that says what it does; then, if it is not obvious, the arguments, the return value, what it changes and who is allowed to call it.

   ```python
   def moderator_required(view):
       """Allow the view only for moderators and admins.

       Looks the member up in the database on every request, so that a
       demotion or ban takes effect at once. Sends signed-out visitors to
       the sign-in page and answers everyone else with 403 Forbidden.
       """
   ```

2. **Explain every "magic" value where it is defined.** The ranks (-1, 1, 2, 98, 99) and visibility codes (-1, 0, 1) become named constants (`Rank.MODERATOR`, `Visibility.PENDING`) with a comment on what each permits.
3. **Inline comments say why, not what.** `# hash the password` above `make_password()` is noise. `# Google posts from its own origin, so Django's CSRF check cannot apply; we verify Google's double-submit token instead` is worth its line.
4. **Be honest.** If a name is poor or an approach is a compromise, say so and say what the better fix would be. Never leave a guess in a comment ("initializes (?)"); find out, then write the answer.
5. **Templates** start with a Django comment naming the view that renders them and the variables they expect. Use `{# ... #}`, not `<!-- ... -->`; HTML comments are sent to every visitor.

   ```django
   {# Rendered by mapViewer.views.post_detail. Expects: post, comments, comment_form, report_form. #}
   ```

6. **JavaScript functions get JSDoc** (`/** ... */`), including which element IDs the script needs on the page.
7. **CSS files** start with a header (what the file styles, which templates use it). Sections get a banner comment. Comment any value that looks arbitrary (a `z-index`, a fixed width), any browser workaround, and the contrast ratio of each text and background token pair.
8. **Delete, don't comment out.** Git keeps the old version.
9. **No dates, names or change notes in files.** The commit records who changed what, when and why; write a good commit message instead.
10. **British spelling in prose;** identifiers that CSS or Python define (`color`, `center`) keep their own spelling.

Replace the old `Uncommented Code Tracker.md` with a checklist issue: one tick per file, ticked in the pull request that brings the file up to standard.

## 8. Order of work

Sizes: S is under half a day, M is one or two days, L is three days or more, for one student. Turn phases into dated milestones once the team size and semester calendar are known.

| Phase | What | Tasks | Size | Move on when |
| --- | --- | --- | --- | --- |
| 0 | Emergency | SEC-00 to SEC-04, the Pillow update from SEC-25, the `viewMap` part of SEC-14, GDPR-11 | M | Moderator pages locked; secrets rotated; debug off; map XSS fixed; no personal files in git. |
| 1 | Foundations | CLN-01 to CLN-06, SEC-20, SEC-25 | M | One Python, one host chosen, checks run on every pull request. |
| 2 | Accounts and permissions | SEC-10 to SEC-18, CLN-16 (permission tests) | L | Every Critical and High finding in 3.1 is closed, each with a test. |
| 3 | Front-end base | A11Y-01, A11Y-03, A11Y-04, A11Y-15, CSS-01 to CSS-03, CSS-08 | L | New base template, tokens and file structure merged; axe runs in the checks. |
| 4 | Page by page | For each group of pages in turn (public pages; sign-in and sign-up; account; "Create Post"; map and posts; moderator): the remaining A11Y and CSS tasks, CLN-10, CLN-11, CLN-14, CLN-15, and the commenting standard | L, repeated six times | The group passes axe and the manual script, has no dead CSS, and every file is ticked on the commenting checklist. |
| 5 | Privacy features | GDPR-03, GDPR-05 to GDPR-10, GDPR-12, SEC-21 to SEC-24, SEC-26, SEC-27 | L | Export, deletion and retention pass end-to-end tests; the CSP is enforcing; data survives a redeploy. |
| 6 | Privacy paperwork | GDPR-01, GDPR-02, GDPR-04, GDPR-13, GDPR-14, A11Y-16 | M | Approved by the College. (Start the decisions in phase 1; approval takes time.) |
| 7 | Renames and tidy | CLN-12, CLN-13, CSS-06 final pass | M | Names match what things are. |
| 8 | Verify and hand over | SEC-28, a full manual WCAG audit by someone who did not build the pages, a restore rehearsal, final README | M | Reports filed; project owner signs off. |

Why this order? Phases 0 to 2 stop harm. Phase 3 comes before the page-by-page work because every page inherits from the base template and the tokens; fix those once and every page improves. Renames come late on purpose: they touch many files, and doing them while security fixes are in flight guarantees merge conflicts.

## 9. How we check the work

1. **On every pull request (automatic):** `manage.py check --deploy`; `makemigrations --check`; tests with coverage; `ruff`; `black --check`; `bandit`; `pip-audit`; Stylelint; ESLint; djLint; axe-core on every address, signed out and signed in.
2. **Before each release (by hand):** keyboard-only pass; NVDA with Firefox on Windows; VoiceOver with Safari on macOS and on an iPhone; 200% zoom; 320 px width; Windows High Contrast; reduced motion.
3. **From outside:** OWASP ZAP baseline scan; Mozilla Observatory; SSL Labs; Lighthouse.
4. **Privacy evidence:** approved data map, records and notices; passing tests for export, deletion and retention; processor terms on file; breach rehearsal noted.

## 10. Decisions we need from other people

| Question | Who decides | Why it matters |
| --- | --- | --- |
| Is the site deployed anywhere now? Is the repository public? | Project owner | Sets how urgent phase 0 is, and whether history must be rewritten. |
| App Engine or Azure? Which region? | Project owner, College IT | Fixes the Python version, database, file store, backups and the GDPR transfer question. |
| Does GDPR apply in law, and what are the lawful bases and retention periods? | College privacy officer or counsel | Shapes the notices, consent and GDPR-06. |
| May a post show a private home address? May profiles be public? | Client | Shapes GDPR-05 and GDPR-09 and the impact assessment. |
| Django's `User` model, or hashed passwords on the existing tables? | Team lead | `User` is safer and brings password reset for free, but needs a careful migration. |
| When a member leaves, do their posts go too? | Client and counsel | GDPR-08. |
| Branding: logo in place of the seal, footer wording, and approval of public pages | Office of Integrated Marketing & Communications | The seal may not be used here; a public site in the College's name should follow the web style guide. |
| Who performs the final accessibility audit? | Project owner | It should not be the people who built the pages. |

## 11. Risks

| Risk | What we do about it |
| --- | --- |
| A migration (password hashing, renames, `User` model) loses data. | Back up first; rehearse every migration on a copy of real data; keep migrations small. |
| Tidying the CSS quietly breaks a page. | Before-and-after screenshots on every CSS pull request (CSS-11). |
| The Content-Security-Policy blocks something we need. | Report-only mode first (SEC-23). |
| Students leave at the end of the semester with work half-merged. | One task per pull request; nothing lives on a branch for more than a week; the README and this plan stay current. |
| Paperwork waits for approvals. | Ask the questions in section 10 in the first week. |
| Rotating the Django secret key signs everyone out. | Expected and harmless; warn members if the site is live. |

## 12. Definition of done

1. No Critical or High finding is open; each Medium finding is fixed or accepted in writing by the project owner.
2. Every page passes the automatic and manual WCAG 2.1 AA checks, with 4.5:1 contrast for all text.
3. The privacy notice, data map, records, retention job, export and deletion features and breach procedure exist and are approved.
4. The CSS uses tokens, has no `!important`, no inline styles, no dead rules and no gradients, and every file meets the commenting standard.
5. A new student can clone the repository, follow the README and have a running, tested site within an hour.

That last point is the practical payoff of the whole exercise: a project that the next team can pick up without fear, and that the College can put its name to.

## 13. Scanner results

We ran these scanners against commit `5bd8d0c9` (the tip of `development`), and against a copy of the site running on a developer's machine with a throwaway database and made-up test data. No live site and no real personal data were touched.

A scanner is like the warning lights on a dashboard: worth having, quick to read, and silent about a great many faults. Read the last column of the first table before you trust a green light.

### 13.1 What was run

| Scanner | What it looks for | Result | What it tells us |
| --- | --- | --- | --- |
| `bandit` 1.9.4 | Risky patterns in Python source | Seven findings, all Low: six are false alarms (words such as "password" in tests and messages); one is the hard-coded `SECRET_KEY`. | BEWARE: bandit reported no High or Medium issue. It did not notice plain-text passwords (F-S2) or the missing access checks (F-S1), because those are faults of design, not of syntax. |
| `pip-audit` 2.10.1 | Known vulnerabilities in pinned packages | 87 advisories in seven of 17 packages (see F-S20). It refused to read `requirements.txt` directly, because `python-dotenv` has no version. | New finding F-S20; task SEC-25 now lists the versions to move to. |
| `manage.py check --deploy` (Django 5.2.18) | Unsafe deployment settings | One error (invalid `SECURE_REFERRER_POLICY`) and six warnings: no HSTS, no HTTPS redirect, weak `SECRET_KEY`, session cookie not `Secure`, CSRF cookie not `Secure`, `DEBUG` on. | Confirms F-S3, F-S4 and F-S14. |
| `manage.py makemigrations --check` | Model changes with no migration | None. | Models and migrations agree. |
| `manage.py test` | The project's own tests | 38 run, 36 pass, two fail. | See CLN-16. |
| `ruff` 0.17.4 | Python errors and style | 62 findings with default rules; 64 with the error, bug and security rules, of which 38 are names that arrive through star imports, ten unused imports, seven star imports, two redefinitions and two unused variables. | Confirms F-C6; 37 can be fixed automatically. |
| `detect-secrets` 1.5.0 | Committed secrets | Nine candidates in six files, including `settings.py` and the editor cache in `.vscode/`. | BEWARE: it did **not** flag the Google API key in `forms.py` and the three templates, nor the credential documents. We found those by reading. Add `gitleaks` to the checks as a second opinion, and keep reviewing by eye. |
| `djlint` 1.50.0 | Template problems | 214 findings in 29 templates: 129 are spacing inside template tags (T001); 17 inline styles (H021); 15 unneeded `type` attributes on scripts and styles (H024); 14 stray spaces round `=` in attributes (H012); 12 others about attribute and tag form. | Mostly formatting; `djlint --reformat` clears the bulk. Supports CSS-08. |
| HTTP probe (`curl`) of 25 addresses, signed out | Status codes, headers, cookies | Two addresses answer 500 (F-S8). The 404 page is Django's debug page and lists every URL pattern (F-S4). Moderator pages answer 200 with an empty body. `X-Frame-Options: DENY` and `X-Content-Type-Options: nosniff` are present; Content-Security-Policy, HSTS and Permissions-Policy are absent. `/account/view/1` (a profile) answers 200 to a signed-out visitor (F-G8). `/post/2` (a pending post) redirects, as it should. | Confirms F-S4, F-S8, F-S14 and F-G8. |
| Signed-out POST tests (`curl`) | Whether actions need permission | Add a tag: accepted. Clear a post's reports: accepted. Create a rank-99 member: accepted. Report a hidden post: accepted. POST to the map: 500 after calling Google. | Confirms and sharpens F-S1; confirms F-S11; new finding F-S21. |
| `axe-core` 4.4.3, WCAG 2.0 and 2.1 A and AA rules, 21 page views (ten signed out, six as a member, five as an admin) | Accessibility faults a machine can detect | See 13.2. | Confirms F-A1, F-A4, F-A5; adds F-A18. |
| Browser resource list on the map page | Third-party requests and cookies | Requests to `unpkg.com`, `maps.googleapis.com` and `maps.gstatic.com`; cookies `csrftoken` and Google's `g_state`. | Confirms F-G3. |

### 13.2 axe-core results by rule

| axe rule | Impact | Pages affected | Finding |
| --- | --- | --- | --- |
| `html-has-lang` | Serious | All 21 | F-A1 |
| `duplicate-id` | Minor | All 21 | F-A4 |
| `label` | Critical | Map page (five controls) | F-A18, F-A13 |
| `document-title` | Serious | About page | F-A5 |
| `definition-list` | Serious | Member profile page | F-A18 |
| `nested-interactive` | Serious | Moderator Reports page | F-A18 |
| `duplicate-id-active` | Serious | Post page when signed in | F-A18 |
| `color-contrast` | Needs a person to check | All 21 (six to 35 elements each) | F-A8 |
| `video-caption` | Needs a person to check | Help page | F-A7 |
| Landmark rules (best-practice set, run on seven pages) | Advisory | Missing or duplicated `main` and `banner` landmarks; content outside any landmark | F-A4 |

Obviously, a page with only two axe violations is not a page with only two accessibility problems. axe cannot tell whether a label makes sense, whether focus goes somewhere sensible, or whether the wizard can be completed by keyboard. The manual checks in section 9 still have to be done.

### 13.3 What was not run, and why

| Check | Why not | Where it sits in the plan |
| --- | --- | --- |
| Stylelint, ESLint | Node.js was not installed on the machine used. | CLN-05 |
| OWASP ZAP (attack scan), Mozilla Observatory, SSL Labs | They need Docker or a deployed HTTPS site; neither was available. | SEC-28 |
| Screen reader, keyboard, zoom and reflow checks | They need a person. | Section 9 |
| Measured colour contrast | axe could not decide; needs the token work first. | A11Y-03 |
| Map pop-up XSS in a browser | The map needs a working Google key. The fault is plain in the code (F-S5). | SEC-03 |
| Git history secret scan (`gitleaks`) | Not installed. | SEC-00, SEC-28 |

Two notes on method. The axe-core copy used (4.4.3) is an older release; the continuous-integration check (A11Y-15) should use the current one, which has more rules. And one of the POST tests caused the local server to send a single geocoding request (for the made-up address "x") to Google with the key that is committed in the code; Google refused it.

---

Plan prepared with Claude Fable 5.2 (Anthropic).
