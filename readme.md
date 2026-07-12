# Radiology Task & Annotation App - Backend

A powerful and secure REST API server designed to handle user authentication, task status management, and image polygon annotation storage. Built with Django and Django REST Framework.

## 🚀 Live Demo
- **Backend API:** [https://radiology-backend-do2p.onrender.com](https://radiology-backend-do2p.onrender.com)
- **Frontend App:** [https://radiology-tawny.vercel.app](https://radiology-tawny.vercel.app)

## 📂 Repository

- **Backend:** https://github.com/mohiuddinshanto/radiology_backend
- **Frontend:** https://github.com/mohiuddinshanto/radiology

## 🎥 Demo Video

https://drive.google.com/file/d/1Qs03IAEXAUDsWBLtu_I2n995-sOK-Psq/view?usp=sharing

## 🔑 Demo Login

- **Email:** `demo@404project.io`
- **Password:** `demo1234`

---

## 🛡️ Challenges Faced & Solutions

### 1. Ephemeral Storage on Render's Free Tier
**Challenge:** Everything worked fine locally with SQLite, but after deploying to Render, accounts and tasks created during one session would vanish after the app sat idle for a while — login would suddenly start returning 401 for a user that definitely existed minutes earlier.
**Solution:** Render's free web services don't have persistent disk. When the instance spins down from inactivity and spins back up on the next request, it's a fresh container — and the SQLite file went with it every time. Migrated the backend from SQLite to a managed PostgreSQL instance (also on Render's free tier) using `dj-database-url`, with a fallback to SQLite when `DATABASE_URL` isn't set so local development is unaffected. The database now lives outside the app container and survives restarts/redeploys.

### 2. A Postgres Driver That Wouldn't Import
**Challenge:** The Postgres migration was otherwise ready, but every deploy started failing at build time with `django.core.exceptions.ImproperlyConfigured: Error loading psycopg2 or psycopg module`.
**Solution:** Render had picked up a very recent Python version that didn't have a pre-built wheel available yet for `psycopg2-binary` — the install step reported success, but the actual import failed at runtime. Pinned the Python version explicitly (`PYTHON_VERSION` env var on Render, plus a `.python-version` file for local consistency) and switched from `psycopg2-binary` to the newer `psycopg[binary]` (Psycopg 3), which has much better support for current Python releases.

### 3. Creating a Demo Superuser Without Shell Access
**Challenge:** Render's free tier doesn't provide Shell access or one-off job runs, which is normally how you'd run `createsuperuser` right after a deploy.
**Solution:** Hooked superuser creation into Django's `post_migrate` signal, gated behind an environment variable (`RESET_SUPERUSER_PASSWORD`), so it runs automatically as part of the `migrate` step that's already in the build command — no manual shell access needed at all. (Also caught a subtle bug while wiring this up: the signal file existed but was never actually imported anywhere in the app, so the logic silently never ran until it was registered in `AppConfig.ready()`.)

### 4. Enforcing Per-User Data Ownership at the API Layer
**Challenge:** With JWT auth in place, any authenticated user could technically read or modify any other user's tasks, uploaded images, and polygon annotations — the ViewSets weren't scoping querysets to the requesting user at all.
**Solution:** Added an `owner` ForeignKey to `Task`, `UploadedImage`, and `AnnotationPolygon`, overrode `get_queryset()` on each ViewSet to filter by `request.user`, and set the owner automatically in `perform_create()` rather than trusting it from the request payload — so a user can never see, edit, or attach data to another user's records.

---

## 🛠️ Tech Stack & Architecture (Why & Where)

### Core Backend & API Framework
- **Django 5.2.15 & Python 3.12.7:**
  - *Where:* Core framework of the backend server application.
  - *Why:* Django is a mature, batteries-included web framework. It provides robust built-in security (SQL injection protection, CSRF, etc.) and an automatic admin interface right out of the box. Python 3.12.7 is pinned explicitly (via `PYTHON_VERSION` on Render and `.python-version` locally) for stable, well-supported compatibility with the Postgres driver — see Challenge #2 above.
- **Django REST Framework (DRF):**
  - *Where:* Serializers, ViewSets, and API routing (`api/`).
  - *Why:* Allows rapid development of clean, standards-compliant RESTful APIs. It handles the serialization of complex client JSON objects (like polygon vertex points) directly into relational database records.

### Authentication & Security
- **djangorestframework-simplejwt (JWT):**
  - *Where:* User login, token refresh, and request validation endpoints.
  - *Why:* Provides industry-standard JSON Web Token authentication, securing all database operations per user session.
- **django-cors-headers:**
  - *Where:* Middleware settings.
  - *Why:* Enabled cross-origin resource sharing (CORS) between the frontend (Vercel) and the backend (Render) for seamless API connectivity.

### Storage & Media Handling
- **Pillow:**
  - *Where:* Used by Django's `ImageField` in `UploadedImage` models.
  - *Why:* Standard Python image processing library required to parse, validate, and verify that uploaded files are indeed valid images.
- **Cloudinary & django-cloudinary-storage:**
  - *Where:* Media settings in production.
  - *Why:* Cloudinary is used to host and store uploaded medical images. Cloud hosts like Render use ephemeral filesystems (where files disappear on container restarts), so static/media hosting is delegated to Cloudinary.

### Database & Deployment
- **PostgreSQL (Production) via `dj-database-url` + `psycopg[binary]`:**
  - *Where:* Main persistent database on Render.
  - *Why:* Render's free tier has no persistent disk — SQLite files stored inside the app container get wiped every time the instance spins down from inactivity and spins back up. Migrated to a managed PostgreSQL instance (also free-tier, hosted on Render) so all users, tasks, and annotation data survive restarts and redeploys. Connection string is read from the `DATABASE_URL` environment variable using `dj-database-url`.
- **SQLite (Local Development Fallback):**
  - *Where:* Used automatically whenever `DATABASE_URL` is not set.
  - *Why:* Zero-configuration, single-file database — ideal for quick local setup without needing a local Postgres instance running.
- **WhiteNoise:**
  - *Where:* Static files middleware.
  - *Why:* Allows the Django application to serve its own static assets (e.g., CSS/JS files for the Admin Panel) in production, removing the need for a separate Nginx setup.
- **Gunicorn:**
  - *Where:* WSGI Production server.
  - *Why:* A robust, production-grade WSGI HTTP Server that serves Python web applications efficiently on Render.
- **Python Decouple:**
  - *Where:* Environment configurations (`settings.py`).
  - *Why:* Enables secure separation of code and secrets (database passwords, Django Secret Key, Cloudinary tokens) from source code.

---

## 📊 Database Models
1. **User (Built-in Django Model):** Manages user registration, profiles, and authentication keys.
2. **Task:** Manages Kanban tasks (`title`, `description`, `status`, `priority`, `due_date`, `tags`, `assignee`, and a ForeignKey relation to the `owner`).
3. **UploadedImage:** Handles patient/scans upload metadata and references the hosted image path (`owner` relation, image location, and timestamp).
4. **AnnotationPolygon:** Stores coordinates (`JSONField` representing point arrays), dynamic labels, and colors linked directly to the parent `UploadedImage`.

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register/` | Create a new user account |
| POST | `/api/token/` | Log in, receive access + refresh JWT |
| POST | `/api/token/refresh/` | Refresh an expired access token |
| GET/POST | `/api/tasks/` | List (filterable by `?date=YYYY-MM-DD`) or create tasks |
| PATCH/DELETE | `/api/tasks/:id/` | Update or delete a task |
| GET/POST | `/api/images/` | List or upload images |
| DELETE | `/api/images/:id/` | Delete an image |
| GET/POST | `/api/polygons/` | List or create polygon annotations |
| PUT/PATCH/DELETE | `/api/polygons/:id/` | Update or delete a polygon annotation |

All endpoints (except `register` and `token`) require a valid JWT and are automatically scoped to the authenticated user's own data.

---

## 🛠️ Setup & Running Locally

### Prerequisites
- Python **3.12.7** (see `.python-version`)
- Virtualenv package

### Local Setup
1. Clone the repository and navigate to the backend folder:
```bash
   git clone https://github.com/mohiuddinshanto/radiology_backend.git
   cd radiology_backend
```
2. Create and activate a Python virtual environment:
```bash
   python -m venv venv
   # On Windows (PowerShell)
   venv\Scripts\Activate.ps1
   # On macOS/Linux
   source venv/bin/activate
```
3. Install the dependencies:
```bash
   pip install -r requirements.txt
```
4. Create a `.env` file from the example:
   Copy `.env.example` to `.env` and fill in the secrets (Django `SECRET_KEY`, Cloudinary credentials, etc.). Leave `DATABASE_URL` unset to use SQLite locally, or set it to a local/remote PostgreSQL connection string to test against Postgres.
5. Apply database migrations:
```bash
   python manage.py migrate
```
6. Start the local server:
```bash
   python manage.py runserver
```
   The backend API will run at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Django secret key |
| `DEBUG` | Yes | `True` locally, `False` in production |
| `ALLOWED_HOSTS` | Production | Comma-separated hostnames |
| `CORS_ALLOWED_ORIGINS` | Yes | Comma-separated frontend origin(s) |
| `DATABASE_URL` | Production | PostgreSQL connection string (omit locally to use SQLite) |
| `USE_CLOUDINARY` | Production | `True` to enable Cloudinary media storage |
| `CLOUDINARY_CLOUD_NAME` / `CLOUDINARY_API_KEY` / `CLOUDINARY_API_SECRET` | If `USE_CLOUDINARY=True` | Cloudinary credentials |
| `DJANGO_SUPERUSER_USERNAME` / `_EMAIL` / `_PASSWORD` | Optional | Auto-creates a superuser on migrate |
| `RESET_SUPERUSER_PASSWORD` | Optional | Set `True` once to (re)apply the superuser password, then set back to `False` |