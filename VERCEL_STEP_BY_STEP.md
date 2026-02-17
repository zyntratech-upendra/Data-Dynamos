# Step-by-Step Vercel Deployment Guide

## Prerequisites
- GitHub account
- Vercel account (free at vercel.com)
- Your Render backend URL (e.g., https://your-service.onrender.com)

---

## STEP 1: Prepare Your Code (Local)

### 1.1 Update .env File
Navigate to `Data-Dynamos` folder and edit `.env`:

```bash
# On your computer
cd Data-Dynamos
```

Edit `.env` file and add your Render backend URL:
```env
VITE_API_URL=https://your-actual-service-name.onrender.com/api
VITE_ENV=production
```

**Example:** If your Render URL is `https://spectramining-backend.onrender.com`, use:
```env
VITE_API_URL=https://spectramining-backend.onrender.com/api
```

### 1.2 Test Locally (Optional)
```bash
# Open index.html in browser
# Right-click → Open with Browser
# Or use: python -m http.server 8000
```

---

## STEP 2: Push Code to GitHub

### 2.1 Initialize Git (if not done)
```bash
cd Data-Dynamos
git init
git add .
git commit -m "Initial commit: SpectraMining AI frontend ready for Vercel"
```

### 2.2 Push to GitHub
```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

**Replace:**
- `YOUR_USERNAME` - Your GitHub username
- `YOUR_REPO` - Repository name (e.g., spectramining-ai)

### 2.3 Verify on GitHub
- Go to github.com and check your repository
- Confirm all files are there (index.html, config.js, .env.example, etc.)

---

## STEP 3: Connect to Vercel

### 3.1 Go to Vercel
1. Visit https://vercel.com
2. Click **Sign Up** or **Login**
3. Choose "GitHub" option
4. Authorize Vercel to access your GitHub account

### 3.2 Import Your Repository
1. Click **Add New...** → **Project**
2. Select **Import Git Repository**
3. Find your repository (spectramining-ai or similar)
4. Click **Import**

---

## STEP 4: Configure Vercel Project

### 4.1 Configure Project Settings
After importing, you'll see a configuration page:

| Setting | Value |
|---------|-------|
| **Framework Preset** | Other (Static Site) |
| **Root Directory** | `./` (or leave empty) |
| **Build Command** | (leave empty) |
| **Output Directory** | (leave empty) |
| **Install Command** | (leave empty) |

**Don't change anything** - Just leave defaults for a static site.

### 4.2 Add Environment Variables
1. Scroll down to **Environment Variables**
2. Click **Add**
3. Fill in:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://your-render-backend.onrender.com/api`
   - **Environments:** Select `Production`

4. Click **Add**

Example environment variables section:
```
VITE_API_URL = https://spectramining-backend.onrender.com/api
```

### 4.3 Deploy
Click **Deploy** button at bottom right

---

## STEP 5: Wait for Deployment

### 5.1 Monitor Progress
- You'll see a deployment log
- Watch for:
  - ✅ "Building..." 
  - ✅ "Generating output..."
  - ✅ "Finalizing deployment"
  - ✅ **"Ready"** - Your site is live!

### 5.2 Common Build Status
```
Building...     (In progress)
Preview URL     (Temporary test link)
Production URL  (Your final URL - appears after "Ready")
```

---

## STEP 6: Get Your Live URL

### 6.1 Find Your URL
After deployment completes:
- **Domain:** `your-project.vercel.app`
- **Example:** `spectramining-ai.vercel.app`

### 6.2 Test Your Site
1. Click the production URL
2. You should see the SpectraMining AI interface
3. Try the "Analyze" button to test API connection

---

## STEP 7: Test API Connection

### 7.1 Open Developer Tools
Press **F12** in your browser

### 7.2 Check Console
1. Go to **Console** tab
2. Type: `window.__CONFIG__.getApiUrl()`
3. You should see your Render backend URL

### 7.3 Try Analysis
1. Enter a location: "Bailadila, India"
2. Click **Analyze** button
3. Check Console for errors:
   - If working: You'll see analysis results
   - If CORS error: Backend CORS needs fixing (see troubleshooting)

---

## STEP 8: Troubleshooting

### Issue: CORS Error
**Error:** `Access to XMLHttpRequest blocked by CORS`

**Solution:** Update backend CORS on Render

In `app.py` (backend):
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-project.vercel.app"],
        "methods": ["GET", "POST", "OPTIONS"]
    }
})
```

Then redeploy Render backend.

### Issue: API URL Not Configured
**Error:** "API URL not configured" in console

**Solution:** 
1. Check Vercel Environment Variables
2. Verify `VITE_API_URL` is set in Vercel dashboard
3. Redeploy: Go to Vercel → Deployments → Redeploy

### Issue: Blank Page
**Solution:**
1. Check browser console for JavaScript errors
2. Verify all CDN links are loading (React, Leaflet, Axios)
3. Check Network tab for failed requests

---

## STEP 9: Update Your Site (Future Deployments)

### When You Want to Update:
```bash
cd Data-Dynamos
git add .
git commit -m "Update: Fix bugs or add features"
git push origin main
```

**Vercel will automatically redeploy!** ✅

No need to push to Vercel again - it watches your GitHub repo.

---

## STEP 10: Custom Domain (Optional)

### Add Your Own Domain
1. Go to Vercel Dashboard
2. Select your project
3. Go to **Settings** → **Domains**
4. Click **Add Domain**
5. Enter your domain (e.g., spectramining.com)
6. Follow DNS setup instructions

---

## Final URLs Structure

After deployment, you'll have:

```
Frontend (Vercel):
├─ URL: https://spectramining-ai.vercel.app
├─ Files: index.html, config.js, etc.
└─ API Calls: → Render backend

Backend (Render):
├─ URL: https://spectramining-backend.onrender.com
├─ API: /api/analyze, /api/geocode, etc.
└─ Technology: Python Flask + Earth Engine
```

---

## Complete Checklist

- [ ] Updated `.env` with Render backend URL
- [ ] Pushed code to GitHub
- [ ] Created Vercel account
- [ ] Imported GitHub repo to Vercel
- [ ] Set `VITE_API_URL` environment variable
- [ ] Clicked Deploy
- [ ] Waited for "Ready" status
- [ ] Tested API connection
- [ ] Shared your Vercel URL with others

---

## Quick Reference Commands

```bash
# 1. Update .env
nano .env
# (or use your editor to edit VITE_API_URL)

# 2. Push to GitHub
git add .
git commit -m "Update backend URL"
git push origin main

# 3. Vercel will auto-deploy!
# (No additional commands needed)

# 4. Check deployment status
# Go to: vercel.com → Your project → Deployments
```

---

## Need Help?

| Issue | Where to Check |
|-------|---|
| Deployment failed | Vercel → Deployments → Build logs |
| API not working | Browser F12 → Console → Check API URL |
| CORS errors | Render backend → Check CORS settings |
| Site not updating | Vercel → Deployments → Manual redeploy |

**Your SpectraMining AI is now live! 🚀**
