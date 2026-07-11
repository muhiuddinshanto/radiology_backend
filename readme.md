# Radiology Task & Annotation App - Backend

A powerful and secure REST API server designed to handle user authentication, task status management, and image polygon annotation storage. Built with Django and Django REST Framework.

## 🚀 Live Demo
- **Backend API:** [https://radiology-backend-do2p.onrender.com](https://radiology-backend-do2p.onrender.com)
- **Frontend App:** [https://radiology-tawny.vercel.app](https://radiology-tawny.vercel.app)

---

## 🛠️ Tech Stack & Architecture (Why & Where)

### Core Backend & API Framework
- **Django (v5.2) & Python 3.12+:**
  - *Where:* Core framework of the backend server application.
  - *Why:* Django is a mature, batteries-included web framework. It provides robust built-in security (SQL injection protection, CSRF, etc.) and an automatic admin interface right out of the box.
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
- **SQLite Database:**
  - *Where:* Main persistent database.
  - *Why:* Lightweight, single-file relational database requiring zero configuration, making it perfect for rapid deployment and development.
- **WhiteNoise:**
  - *Where:* Static files middleware.
  - *Why:* Allows the Django application to serve its own static assets (e.g., CSS/JS files for the Admin Panel) in production, removing the need for a separate Nginx setup.
- **Gunicorn:**
  - *Where:* WSGI Production server.
  - *Why:* A robust, production-grade WSGI HTTP Server that serves Python web applications efficiently on Render.
- **Python Decouple:**
  - *Where:* Environment configurations (`settings.py`).
  - *Why:* Enables secure separation of code and secrets (database passwords, Django Secret Key, Cloudinary tokens).

---

## 📊 Database Models
1. **User (Built-in Django Model):** Manages user registration, profiles, and authentication keys.
2. **Task:** Manages Kanban tasks (`title`, `description`, `status`, `priority`, `due_date`, `tags`, `assignee`, and a ForeignKey relation to the `owner`).
3. **UploadedImage:** Handles patient/scans upload metadata and references the hosted image path (`owner` relation, image location, and timestamp).
4. **AnnotationPolygon:** Stores coordinates (`JSONField` representing point arrays), dynamic labels, and colors linked directly to the parent `UploadedImage`.

---

## 🛠️ Setup & Running Locally

### Prerequisites
- Python 3.12+ installed
- Virtualenv package

### Local Setup
1. Clone the repository and navigate to the backend folder:
   ```bash
   cd "thart backend/core_backend"
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
   Copy `.env.example` to `.env` and fill in the secrets (including Cloudinary credentials for image upload).
5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the local server:
   ```bash
   python manage.py runserver
   ```
   The backend API will run at [http://127.0.0.1:8000](http://127.0.0.1:8000).