# Chesapeake Community Connect

## Software Requirements Specification

**Version:** 2.0
**Date:** October 19, 2026
**Status:** Current project baseline
**Project:** ChesapeakeCommunityConnect

## Revision History

| Date | Version | Description | Author(s) |
| :---: | :---: | :--- | :--- |
| 11/29/23 | 1.0 | Initial draft | Chesapeake Community Connect capstone team |
| 01/24/24 | 1.1 | Revision started for 2024 | Chesapeake Community Connect team |
| 02/24/25 | 1.2 | Revision for Spring 2025 | Sophia Lin |
| 10/19/26 | 2.0 | Updated scope, requirements, technology stack, and delivery model for the current Django application | CDSpecCollab team |

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the current scope and externally observable requirements of the Chesapeake Community Connect (CCC) website. It is the baseline for implementation, quality assurance, deployment, and future maintenance. Requirements marked **Implemented** describe behavior represented in the current repository. Requirements marked **Planned** identify work that remains in scope but is not complete in the current application.

### 1.2 Scope

CCC is a browser-based Django application that helps communities share environmental projects, stories, and resources connected to the Chesapeake region. The application presents approved map posts on an interactive map and searchable list, supports contributor profiles and project submissions, and provides administrative tools for moderation, reports, tags, and account requests.

The current release includes:

* A Django 4.2 web application served through WSGI or ASGI.
* SQLite persistence in the current repository configuration, with Django migrations for the application models.
* Google Identity Services sign-in using verified Google ID tokens.
* Session-based member access and ranking values for member, trusted member, moderator, administrator, and banned states.
* Map posts with titles, descriptions, content, geocodes, tags, authors, timestamps, and visibility states.
* Search and tag filtering for visible map posts.
* Contributor profile management and account-creation requests.
* Administrative pages for messages, members, tags, reports, and moderation workflows.
* Static and uploaded media served through Django configuration.

The current release does not provide a completed public export endpoint, email approval notifications, arbitrary audio/video storage, or a production-safe externalized-secret configuration. Those items are documented as planned or operational requirements rather than claimed as completed functionality.

### 1.3 Definitions, Acronyms, and Abbreviations

| Term | Definition |
| --- | --- |
| CCC | Chesapeake Community Connect |
| SRS | Software Requirements Specification |
| SDD | Software Design Description |
| STP | Software Test Plan |
| Member | A CCC contributor profile stored by the application |
| Map post | A community project or environmental story displayed by the application |
| Map tag | A category associated with one or more map posts |
| Visibility | The publication state of a map post: pending, visible, or denied |
| Janitor | The application area containing administrative and moderation tools |
| Geocode | Location data used to place a map post on the map |
| Google Identity Services | The external Google service used for sign-in |

### 1.4 Document References

The following repository files define or support this baseline:

* Project overview: `README.md`
* Application dependencies: `cccSite/requirements.txt`
* Django configuration: `cccSite/cccSite/settings.py`
* Root routes: `cccSite/cccSite/urls.py`
* Map-post model and views: `cccSite/mapViewer/models.py` and `cccSite/mapViewer/views.py`
* Member model and account views: `cccSite/account/models.py` and `cccSite/account/views.py`
* Moderation models and views: `cccSite/Janitor/models.py` and `cccSite/Janitor/views.py`
* Deployment configuration: `cccSite/app.yaml`
* Developer and deployment guides: `docs/` and the repository setup guides

### 1.5 System Overview

CCC has four principal application areas:

1. **Map viewer:** Lists visible posts, filters them by text and tags, serializes them for the interactive map, and displays post details.
2. **Account:** Shows member information, permits profile edits, handles sign-in and sign-out, and records Google account associations.
3. **Boiler pages:** Provides About, Help, and Contact pages and stores submitted contact or help messages.
4. **Janitor administration:** Provides management pages for users, tags, reports, and contact messages.

The project uses Django URL routing, templates, forms, models, migrations, sessions, and the Google Maps/Google Identity integrations. The browser supplies the presentation layer; no native desktop or mobile client is required.

---

## 2. Functional Requirements

### 2.1 Map and Project Discovery

* **FR-MAP-01 — Implemented:** The system shall provide a homepage containing the map viewer.
* **FR-MAP-02 — Implemented:** The system shall display map posts whose visibility is set to visible.
* **FR-MAP-03 — Implemented:** Each visible map post shall provide a title, description, author, geocode, creation timestamp, and associated tags where available.
* **FR-MAP-04 — Implemented:** The system shall provide a list view of visible map posts.
* **FR-MAP-05 — Implemented:** Users shall be able to filter visible posts by text matching against the title or content.
* **FR-MAP-06 — Implemented:** Users shall be able to filter visible posts by one or more map tags.
* **FR-MAP-07 — Implemented:** The system shall provide a detail page for an individual map post.
* **FR-MAP-08 — Implemented:** The system shall prevent a visitor from viewing a non-visible post unless the visitor is its author or has an elevated session rank.
* **FR-MAP-09 — Planned:** The map shall provide an explicit user-facing filter panel for project type, organization or individual, and project status.
* **FR-MAP-10 — Planned:** The map shall provide a user-facing full-screen mode and a consistent legend for tag or project-type presentation.

### 2.2 Project Submission

* **FR-SUBMIT-01 — Implemented:** The system shall provide a submission form for a map-post title, content, geocoded location, and optional tags.
* **FR-SUBMIT-02 — Implemented:** A submitted post shall be associated with the currently signed-in member.
* **FR-SUBMIT-03 — Implemented:** A post submitted by a member with rank 1 shall initially be pending.
* **FR-SUBMIT-04 — Implemented:** A post submitted by a member with rank greater than 1 shall initially be visible.
* **FR-SUBMIT-05 — Implemented:** The system shall store the post’s title, content, description preview, geocode, author, tags, creation time, and visibility.
* **FR-SUBMIT-06 — Implemented:** The system shall allow contributors to submit written environmental project or community information.
* **FR-SUBMIT-07 — Planned:** The submission form shall accept validated image, audio, or video resources with documented size, type, and storage limits.
* **FR-SUBMIT-08 — Planned:** The application shall provide a complete contributor submission review status page.

### 2.3 Accounts and Contributors

* **FR-ACCOUNT-01 — Implemented:** The system shall provide sign-in, sign-out, and a member account page.
* **FR-ACCOUNT-02 — Implemented:** The system shall support Google Identity Services sign-in and verify the returned Google ID token before creating or loading the associated member.
* **FR-ACCOUNT-03 — Implemented:** The system shall retain the association between a verified Google identifier and a CCC member.
* **FR-ACCOUNT-04 — Implemented:** A signed-in member shall be able to edit their profile name, email, picture, and About text through the account management form.
* **FR-ACCOUNT-05 — Implemented:** The system shall support member ranking states for banned, member, trusted member, moderator, and administrator accounts.
* **FR-ACCOUNT-06 — Implemented:** The system shall provide a contributor account-creation request model with pending, accepted, and rejected states.
* **FR-ACCOUNT-07 — Planned:** The system shall provide a public contributor directory with search, alphabetical navigation, and contributor profile links.
* **FR-ACCOUNT-08 — Planned:** Account creation requests shall validate password confirmation and shall never store raw passwords.

### 2.4 Administration and Moderation

* **FR-ADMIN-01 — Implemented:** The system shall provide an administration area for authorized moderators or administrators.
* **FR-ADMIN-02 — Implemented:** Administrators shall be able to view contact and help messages.
* **FR-ADMIN-03 — Implemented:** Administrators shall be able to view member records and access member management forms.
* **FR-ADMIN-04 — Implemented:** Administrators shall be able to add and remove map tags.
* **FR-ADMIN-05 — Implemented:** The system shall provide post-report and user-report records.
* **FR-ADMIN-06 — Implemented:** Administrators shall be able to review reports and clear report records.
* **FR-ADMIN-07 — Implemented:** The system shall represent post moderation with pending, visible, and denied visibility states.
* **FR-ADMIN-08 — Planned:** The administration area shall provide a completed pending-post queue with explicit approve and reject actions.
* **FR-ADMIN-09 — Planned:** Administrators shall be able to search, edit, approve, reject, and delete member accounts through a completed workflow.
* **FR-ADMIN-10 — Planned:** The system shall send a notification to a submitter when an administrator approves or rejects a post.
* **FR-ADMIN-11 — Planned:** The administration area shall provide a working data export operation. The current export view is not implemented.

### 2.5 Help, About, and Contact

* **FR-CONTENT-01 — Implemented:** The system shall provide an About page describing the project.
* **FR-CONTENT-02 — Implemented:** The system shall provide Help and Contact pages with forms for name, email, username, display name, and message information where applicable.
* **FR-CONTENT-03 — Implemented:** Valid contact or help form submissions shall be stored as application messages.
* **FR-CONTENT-04 — Planned:** The Help page shall provide a complete tutorial and frequently asked questions for map browsing, filtering, account access, and submissions.
* **FR-CONTENT-05 — Planned:** The site shall provide consistent branding and navigation on all public and authenticated pages.

### 2.6 External Integrations

* **FR-INTEGRATION-01 — Implemented:** The system shall use Google Maps-related configuration to support map presentation and geocoded locations.
* **FR-INTEGRATION-02 — Implemented:** The system shall use Google Identity Services for the configured sign-in flow.
* **FR-INTEGRATION-03 — Planned:** External API credentials shall be configurable per deployment and shall not be committed to source control.
* **FR-INTEGRATION-04 — Planned:** The application shall define behavior when an external map or identity service is unavailable.

---

## 3. Non-Functional Requirements

### 3.1 Security and Privacy

* **NFR-SEC-01:** Production deployments shall run with `DEBUG` disabled and a restricted `ALLOWED_HOSTS` list.
* **NFR-SEC-02:** Production deployments shall load Django secrets, Google credentials, API keys, and database credentials from protected configuration rather than source code.
* **NFR-SEC-03:** The application shall use Django CSRF protection for ordinary state-changing forms.
* **NFR-SEC-04:** Google sign-in requests shall validate the Google CSRF token and verify the ID token before creating a session.
* **NFR-SEC-05:** Administrative and moderation operations shall require an authenticated session with an appropriate rank.
* **NFR-SEC-06:** The application shall not store raw passwords. Existing account-request fields containing password values shall be replaced or removed before production use.
* **NFR-SEC-07:** User reports and contact submissions shall be accessible only to authorized administrative users.

### 3.2 Compatibility and Usability

* **NFR-USE-01:** The application shall be usable in a current desktop or mobile browser with JavaScript enabled.
* **NFR-USE-02:** The interface shall support responsive layouts for desktop and mobile screens.
* **NFR-USE-03:** Forms shall display validation feedback when submitted data is invalid.
* **NFR-USE-04:** Public users shall be able to browse visible map content without creating an account.
* **NFR-USE-05:** The interface shall use accessible labels, meaningful link text, keyboard navigation, and sufficient contrast for core workflows.

### 3.3 Maintainability

* **NFR-MAINT-01:** The application shall target Python dependencies declared in `cccSite/requirements.txt`, including Django 4.2.6.
* **NFR-MAINT-02:** Database schema changes shall be represented by Django migrations.
* **NFR-MAINT-03:** New behavior shall include automated tests for affected views, forms, models, permissions, and integrations where practical.
* **NFR-MAINT-04:** Requirements, design, test, deployment, and training documents shall identify the same current scope and technology stack.

### 3.4 Reliability and Performance

* **NFR-PERF-01:** The application shall return an explicit response when a requested post, member, report, or external service is unavailable.
* **NFR-PERF-02:** Map and list views shall query only visible posts for public discovery.
* **NFR-PERF-03 — Planned:** Production deployment shall define supported post counts, media-size limits, and response-time targets for homepage, list, detail, and submission workflows.
* **NFR-PERF-04 — Planned:** Operators shall define database backup, restore, migration, and media-file retention procedures.

---

## 4. External Interfaces

### 4.1 User Interface

The application shall provide:

* The public map homepage and visible-post list.
* A map-post detail view.
* Account sign-in, sign-out, profile, and profile-management pages.
* About, Help, and Contact pages.
* Contributor submission and account-request forms.
* Administrative pages for members, tags, reports, contact messages, and moderation.

### 4.2 Map and Geolocation Interface

Map posts store a JSON geocode and are serialized for map rendering. The application uses Google Maps-related configuration for the map interface and location presentation. The exact provider limits, key restrictions, and failure behavior must be documented for each production deployment.

### 4.3 Authentication Interface

Google Identity Services posts a credential to the account authentication endpoint. The application validates the Google CSRF cookie and request value, verifies the ID token, associates the verified Google identifier with a `Member`, and stores the member identity and rank in the session.

### 4.4 Database and Media Interface

The application uses Django’s ORM, models, and migrations. The current repository configuration uses SQLite at `cccSite/db.sqlite3`. Member profile images are stored under the configured media root using an overwrite storage helper. Production deployments shall select a persistent database and media-storage strategy appropriate for the deployment.

### 4.5 Administrative Interface

Administrative routes are exposed under the project’s configured administration paths. Access to these routes shall be restricted by authentication and rank checks before production release.

---

## 5. System and Deployment Requirements

### 5.1 Server

The deployment shall provide:

* A supported Python runtime and the pinned packages in `cccSite/requirements.txt`.
* A WSGI- or ASGI-compatible application server.
* Persistent database storage.
* Persistent media storage for member images and future post media.
* HTTPS and a configured production hostname.
* Restricted Google Maps and Google Identity credentials.

### 5.2 Client

The client shall provide:

* A current desktop or mobile browser.
* JavaScript enabled for map and Google sign-in features.
* Network access to the deployed application and configured external services.

The project is a web application and does not require a locally installed desktop client or database for ordinary user access.

### 5.3 Configuration

Before production release, operators shall configure the Django secret key, debug setting, allowed hosts, database, media and static-file serving, Google Maps API key, Google OAuth client identifier, HTTPS settings, and backup policy without exposing secrets in the repository.

---

## 6. Delivery and Acceptance

An iteration satisfies this SRS baseline when:

1. Implemented requirements remain available through the documented routes.
2. Public discovery shows only visible map posts.
3. A signed-in member can submit a map post with a title, content, location, and tags.
4. The map and list views support text and tag filtering.
5. Google sign-in validates the identity token before establishing a member session.
6. Administrative users can review the implemented messages, tags, reports, and member workflows.
7. Automated tests pass for changed behavior.
8. Deployment documentation identifies all required services and configuration values.
9. Any unimplemented or changed requirement is labeled Planned or updated in this document before release.

---

## 7. Out of Scope for the Current Baseline

The following are not completed requirements of the current implementation:

* A native Windows, macOS, Linux, iOS, or Android application.
* Direct control of environmental sensors or other field equipment.
* Automatic scientific or environmental analysis of submitted content.
* A completed public audio/video hosting and transcoding service.
* Email approval or rejection notifications.
* A completed public contributor directory and alphabetical search.
* A completed administrator data-export workflow.
* Unrestricted public access to pending, denied, or private records.

---

## 8. Related Documentation

This SRS should remain synchronized with the Software Design Description, Software Test Plan, traceability matrix, README, deployment guides, and training documents. When implementation changes affect routes, permissions, data fields, dependencies, external services, or deployment configuration, the corresponding documentation and requirement status shall be reviewed in the same change.
