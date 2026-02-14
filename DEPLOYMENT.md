# Deploy Hostel Management System

This guide covers deploying the Django app to **Railway**, **Render**, or **PythonAnywhere** (all have free tiers).

---

## Before you deploy

1. **Database**: The project uses **SQLite** by default when deployed (no Oracle needed). For local Oracle, set env var `DB_ENGINE=oracle` and your Oracle vars.
2. **Static files**: Handled by WhiteNoise (no extra web server needed).
3. **Secrets**: You will set `DJANGO_SECRET_KEY` and optionally `ALLOWED_HOSTS` in the host’s dashboard.

---

## Option 1: Railway (recommended – simple)

1. Go to [railway.app](https://railway.app) and sign in with GitHub.
2. Click **New Project** → **Deploy from GitHub repo**.
3. Select **hajrahk/hostel-management-** and the **main** branch.
4. Railway will detect Django. Set:
   - **Root Directory**: `hajra` (if the repo root is one level above; if the repo root is already the folder with `manage.py`, leave blank).
   
   If your repo root is the folder that contains `manage.py`, leave root directory **empty**. If your repo has everything inside a `hajra` subfolder, set **Root Directory** to `hajra`.

5. **Variables** (in Railway project → your service → Variables):
   - `DJANGO_SECRET_KEY` = a long random string (e.g. from [djecrety.ir](https://djecrety.ir/)).
   - `DJANGO_DEBUG` = `False`
   - `ALLOWED_HOSTS` = `your-app-name.up.railway.app` (Railway shows the URL after first deploy; then add it here and redeploy if needed).

6. **Build**: Railway usually auto-detects. If not:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn hostel_management.wsgi --bind 0.0.0.0:$PORT`

7. Deploy. After deploy, open your app URL and run migrations once (Railway → your service → **Settings** → add a one-off run, or use **Shell**):
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

Your app will be live at `https://your-app-name.up.railway.app`.

---

## Option 2: Render

1. Go to [render.com](https://render.com) and sign in with GitHub.
2. **New** → **Web Service**.
3. Connect **hajrahk/hostel-management-**.
4. Settings:
   - **Name**: e.g. `hostel-management`
   - **Root Directory**: leave empty if `manage.py` is at repo root; otherwise `hajra`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn hostel_management.wsgi --bind 0.0.0.0:$PORT`

5. **Environment** (Environment tab):
   - `DJANGO_SECRET_KEY` = (generate a secret key)
   - `DJANGO_DEBUG` = `False`
   - `ALLOWED_HOSTS` = `your-service-name.onrender.com`

6. Click **Create Web Service**. After first deploy, open **Shell** and run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

Your app will be at `https://your-service-name.onrender.com`. (Free tier sleeps after inactivity.)

---

## Option 3: PythonAnywhere

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com) and create a free account.
2. Open the **Dashboard** → **Consoles** → **Bash**.
3. Clone and setup:
   ```bash
   git clone https://github.com/hajrahk/hostel-management-.git
   cd hostel-management-
   # If your repo has a hajra subfolder with manage.py, then: cd hajra
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Web** tab:
   - Add a new web app → **Manual configuration** → Python 3.10.
   - **Source code**: `/home/yourusername/hostel-management-` (and **Working directory** to `.../hajra` if you use that subfolder).
   - **WSGI file**: Edit the default and point to your project, e.g.:
     ```python
     import os
     import sys
     path = '/home/yourusername/hostel-management-/hajra'  # or path to folder with manage.py
     if path not in sys.path:
         sys.path.append(path)
     os.environ['DJANGO_SETTINGS_MODULE'] = 'hostel_management.settings'
     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```
   - **Static files**: URL `/static/`, Directory: `/home/yourusername/hostel-management-/hajra/staticfiles` (after you run collectstatic).

5. In the console (with venv on):
   ```bash
   python manage.py collectstatic --noinput
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. Set **ALLOWED_HOSTS**: in **Web** → **Code** or via env, add your PythonAnywhere host, e.g. `yourusername.pythonanywhere.com`.

Reload the web app. Your site will be at `https://yourusername.pythonanywhere.com`.

---

## Environment variables summary

| Variable           | Required in production | Example / note                          |
|--------------------|------------------------|-----------------------------------------|
| `DJANGO_SECRET_KEY`| Yes                    | Long random string                      |
| `DJANGO_DEBUG`     | Yes                    | `False`                                 |
| `ALLOWED_HOSTS`    | Yes                    | Your app host, e.g. `app.up.railway.app`|
| `DB_ENGINE`        | No                     | `oracle` only if using Oracle           |
| `ORACLE_*`         | If Oracle              | Connection details                      |

---

## After first deploy

1. Run migrations: `python manage.py migrate`
2. Create admin user: `python manage.py createsuperuser`
3. Open `/admin` and log in; create rooms and manage data as needed.

If anything fails, check the platform’s logs (Railway/Render/PythonAnywhere) and that `ALLOWED_HOSTS` and `DJANGO_DEBUG=False` are set.
