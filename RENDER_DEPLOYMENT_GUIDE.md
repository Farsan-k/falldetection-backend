# Render Deployment Guide: Fall Detection Project

This guide provides step-by-step instructions to deploy the Fall Detection Django backend on [Render](https://render.com) for free and connect it with the Flutter mobile app and YOLOv7 AI detector.

---

## 1. Push Django Backend to GitHub

1. Open PowerShell or Terminal and navigate to the Django directory:
   ```powershell
   cd C:\Users\DELL\OneDrive\Desktop\FallDetetion\falldetectionusingai
   ```
2. Initialize git and commit your files:
   ```powershell
   git init
   git add .
   git commit -m "Configure project for Render deployment"
   ```
3. Create a new repository on [GitHub](https://github.com/new) (e.g., named `falldetection-backend`).
4. Link and push to GitHub:
   ```powershell
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/falldetection-backend.git
   git branch -M main
   git push -u origin main
   ```

---

## 2. Deploy on Render (1-Click Blueprint or Web Service)

### Option A: Using Render Blueprint (Recommended)
1. Log in to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** in the top right corner and select **Blueprint**.
3. Connect your GitHub repository `falldetection-backend`.
4. Render will detect the [`render.yaml`](./render.yaml) file and automatically set up:
   - A Web Service (`falldetection-backend`)
   - A Free PostgreSQL Database (`falldetection-db`)
5. Click **Apply**.
6. Wait 2-3 minutes for the build to finish. Once done, you will receive a URL such as:
   `https://falldetection-backend-xxxx.onrender.com`

### Option B: Manual Web Service Setup
If you want to create the web service manually:
1. Click **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure settings:
   - **Name**: `falldetection-backend`
   - **Region**: Choose the closest region (e.g., Singapore, Frankfurt, Oregon)
   - **Branch**: `main`
   - **Root Directory**: *(leave blank)*
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh` (or `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`)
   - **Start Command**: `gunicorn falldetectionusingai.wsgi:application`
   - **Instance Type**: `Free`
4. In **Environment Variables**, add:
   - `PYTHON_VERSION`: `3.11.9`
   - `SECRET_KEY`: *(any random long string)*
   - `DEBUG`: `False`
   - `DATABASE_URL`: *(PostgreSQL connection string from Render Postgres or an external free database like Supabase/Neon/TiDB)*
5. Click **Create Web Service**.

---

## 3. Seed Initial Database Accounts

Once the deployment finishes on Render:
1. In the Render Dashboard, go to your Web Service.
2. Click the **Shell** tab on the left menu.
3. Run:
   ```bash
   python seed_data.py
   ```
4. This instantly creates the default accounts:
   - **Portal Admin**: `admin1@gmail.com` / Password: `admin11`
   - **Doctor**: `doctor2@gmail.com` / Password: `doctor2`
   - **User / Patient**: `user1@gmail.com` / Password: `user1`
   - **Django Admin**: `admin` / Password: `admin12345`

---

## 4. Connect the Flutter Mobile App

1. Launch your Flutter app (`falldetectionusinal`).
2. On the initial connection screen ("Server URL or IP address"), enter your Render URL:
   ```
   https://falldetection-backend-xxxx.onrender.com
   ```
   *(or simply `falldetection-backend-xxxx.onrender.com`)*
3. Click **Connect**.
4. Log in using `user1@gmail.com` / `user1` or sign up a new account.

---

## 5. Connect AI Fall Detection (`Human-Fall-Detection-master`)

To run the YOLOv7 fall detection model on your computer and stream fall events directly to Render:
1. Open PowerShell in `Human-Fall-Detection-master`:
   ```powershell
   cd C:\Users\DELL\OneDrive\Desktop\FallDetetion\Human-Fall-Detection-master
   ```
2. Set the Render URL in the environment:
   ```powershell
   $env:RENDER_SERVER_URL="https://falldetection-backend-xxxx.onrender.com"
   ```
3. Run the fall detection:
   ```powershell
   python main.py
   ```
4. Whenever a fall is detected, it automatically uploads the snapshot and triggers a real-time fall notification on Render, which alerts the mobile app and doctors!
