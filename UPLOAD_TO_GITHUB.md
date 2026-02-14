# Upload this project to GitHub (hajrahk)

Follow these steps **in a terminal opened inside your project folder** (e.g. the `hajra` folder where `manage.py` is).

## 1. Open terminal in project folder

- In Cursor/VS Code: **Terminal → New Terminal** (it usually opens in your project root).
- If needed, run: `cd hajra` so you are in the folder that contains `manage.py`.

## 2. Initialize Git (if not already done)

```bash
git init
```

## 3. Stage all files

```bash
git add -A
```

## 4. First commit

```bash
git commit -m "Initial commit: Hostel Management System with Midnight Blue & Silver theme"
```

## 5. Create the repository on GitHub

1. Go to **https://github.com/new**
2. **Repository name:** e.g. `hostel-management`
3. **Description (optional):** e.g. `Django hostel management system with room assignment, announcements, attendance`
4. Choose **Public**
5. Do **not** check "Add a README" (you already have one)
6. Click **Create repository**

## 6. Connect and push

GitHub will show you commands. Use these (replace `hostel-management` if you used a different repo name):

```bash
git branch -M main
git remote add origin https://github.com/hajrahk/hostel-management.git
git push -u origin main
```

If GitHub asks you to log in, use your GitHub username and a **Personal Access Token** (not your password). Create one at: **GitHub → Settings → Developer settings → Personal access tokens**.

---

After this, your project will be at: **https://github.com/hajrahk/hostel-management**
