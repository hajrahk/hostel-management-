# Deploy Hostel Management System to Vercel

Vercel runs Django as a serverless app. You **must use a hosted PostgreSQL database** (Vercel does not support SQLite). Free options: **Vercel Postgres**, **Neon**, or **ElephantSQL**.

---

## 1. Create a PostgreSQL database (free)

Choose one:

- **[Neon](https://neon.tech)** – Free tier, instant. Create a project → copy the connection string (e.g. `postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require`).
- **[ElephantSQL](https://www.elephantsql.com)** – Free tier. Create instance → copy the URL.
- **Vercel Postgres** – In your Vercel project: Storage → Create Database → Postgres. Copy `POSTGRES_URL` (or the URL they show).

Keep this URL; you’ll add it as `DATABASE_URL` on Vercel.

---

## 2. Push your code to GitHub

Ensure the latest code (including `vercel.json`, `build_files.sh`, `hostel_management/wsgi.py` with `app = application`) is on GitHub:

```bash
git add -A
git commit -m "Add Vercel deployment config"
git push origin main
```

---

## 3. Deploy on Vercel

1. Go to **[vercel.com](https://vercel.com)** and sign in with GitHub.
2. Click **Add New…** → **Project**.
3. **Import** the repo **hajrahk/hostel-management-**.
4. **Root Directory**: leave as **.** (repo root = project with `manage.py`).
5. **Framework Preset**: leave as **Other** (or **Django** if shown).
6. Do **not** change Build/Rewrite; `vercel.json` defines them.

---

## 4. Environment variables

In the Vercel project → **Settings** → **Environment Variables**, add:

| Name | Value | Notes |
|------|--------|--------|
| `DJANGO_SECRET_KEY` | A long random string | e.g. from [djecrety.ir](https://djecrety.ir/) |
| `DJANGO_DEBUG` | `False` | Required in production |
| `DATABASE_URL` | Your Postgres URL | From Neon / ElephantSQL / Vercel Postgres |
| `ALLOWED_HOSTS` | Your Vercel host | e.g. `hostel-management-xxx.vercel.app` (see after first deploy) |
| `CSRF_TRUSTED_ORIGINS` | Your app URL | e.g. `https://hostel-management-xxx.vercel.app` |

After the first deploy, Vercel will show the URL (e.g. `hostel-management-xxxx.vercel.app`). Add that host to `ALLOWED_HOSTS` and the same URL (with `https://`) to `CSRF_TRUSTED_ORIGINS`, then redeploy.

---

## 5. Deploy and run migrations

1. Click **Deploy**.
2. Wait for the build. If it fails, check the build logs (often Python version or missing deps).
3. After a successful deploy, open your project on Vercel → **Settings** → **Functions** or use the **Vercel CLI** to run migrations (see below).  
   Alternatively, run migrations **locally** once, pointing at the same `DATABASE_URL`:

   ```bash
   set DATABASE_URL=your_postgres_url_here
   python manage.py migrate
   python manage.py createsuperuser
   ```

   Use the same `DATABASE_URL` you set on Vercel so the live app and this run use the same database.

4. Open your Vercel URL (e.g. `https://hostel-management-xxx.vercel.app`) and log in with the superuser you created.

---

## 6. (Optional) Node.js version on Vercel

If you see an `ImportError` or runtime error related to Node, set the Node version to **18.x**:

- Project → **Settings** → **General** → **Node.js Version** → **18.x** → Save, then redeploy.

---

## Summary checklist

- [ ] PostgreSQL database created (Neon / ElephantSQL / Vercel Postgres).
- [ ] Repo pushed with `vercel.json`, `build_files.sh`, and `app = application` in `wsgi.py`.
- [ ] Vercel project created and connected to **hajrahk/hostel-management-**.
- [ ] Env vars set: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DATABASE_URL`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`.
- [ ] Deploy successful; then run `migrate` and `createsuperuser` (locally with same `DATABASE_URL` or via CLI).
- [ ] App opens at the Vercel URL and you can log in.

Your app will be live at **https://your-project.vercel.app**.
