# Setup Checklist - Backend & Frontend Deployment

## ✅ Issues Fixed

- [x] Removed Flask template requirement (index.html not found error)
- [x] Created proper Earth Engine authentication module for Render
- [x] API-only backend setup (frontend served separately on Vercel)

---

## 📋 Quick Deployment Steps

### STEP 1: Get Google Earth Engine Credentials (5 mins)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create Service Account (see RENDER_DEPLOYMENT.md for details)
3. Download JSON key file
4. Copy the entire JSON content (you'll need this for Render)

### STEP 2: Deploy Backend to Render

**Option A: Using GitHub (Easiest)**
```bash
git add .
git commit -m "Fix backend for Render deployment"
git push
```

Then on Render:
1. Create new Web Service from your GitHub repo
2. Use folder: `Data-Dynamos`
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn app:app`

**Option B: Manual Push**
- Use Render CLI: `render push`

### STEP 3: Add Earth Engine Credentials to Render

1. Go to Render Dashboard → Your Service → Environment
2. Add environment variable:
   - **Key:** `GOOGLE_APPLICATION_CREDENTIALS_JSON`
   - **Value:** (Paste entire JSON from Step 1)
3. Click Save (will redeploy automatically)

### STEP 4: Get Your Backend URL

After deployment completes, your URL will be:
```
https://your-service-name.onrender.com
```

Keep this for the frontend!

### STEP 5: Update Frontend for Vercel

In `Data-Dynamos/index.html` (around line 1545):
```javascript
const API_BASE_URL = 'https://your-service-name.onrender.com/api';
```

### STEP 6: Deploy Frontend to Vercel

```bash
cd Data-Dynamos
vercel
```

Then when prompted:
- Project name: Choose one
- Framework: "Other" or "Static Site"
- Root directory: `./`
- Deploy!

### STEP 7: Test Everything

1. Visit your Vercel frontend URL
2. Open DevTools (F12)
3. Try the "Analyze" button
4. Check Console tab for any errors

---

## 📁 Files Modified/Created

- `app.py` - Fixed Flask routes and EE initialization
- `ee_auth.py` - NEW: Earth Engine authentication handler
- `RENDER_DEPLOYMENT.md` - NEW: Detailed setup guide
- `vercel.json` - NEW: Vercel static site config
- `VERCEL_DEPLOYMENT.md` - NEW: Frontend deployment guide

---

## 🔗 Your Final URLs (After Deployment)

| Service | URL |
|---------|-----|
| Frontend (Vercel) | `https://your-project.vercel.app` |
| Backend API (Render) | `https://your-service.onrender.com` |
| API Endpoint | `https://your-service.onrender.com/api/analyze` |

---

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| Earth Engine still fails | Check JSON credentials in Render Environment |
| CORS errors | Verify `GOOGLE_APPLICATION_CREDENTIALS_JSON` is set |
| 503 errors | Wait 2-3 mins for Render to deploy |
| Slow performance | Render free tier is slow, upgrade to paid plan |

---

## 📚 Need Help?

- Backend issues? → See `RENDER_DEPLOYMENT.md`
- Frontend issues? → See `VERCEL_DEPLOYMENT.md`
- Earth Engine auth? → Check Step 1

**Once deployed, share the Vercel URL with others!**
