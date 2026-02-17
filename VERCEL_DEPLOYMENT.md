# Data-Dynamos Vercel Deployment Guide

## Step 1: Update Backend URL

Before deploying, update the API URL in `index.html`:

```javascript
// Line ~1545 in index.html
const API_BASE_URL = 'https://your-render-backend.onrender.com/api';
```

Replace `your-render-backend.onrender.com` with your actual Render backend URL.

## Step 2: Deploy to Vercel

### Option A: Using Vercel CLI (Recommended)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Navigate to Data-Dynamos folder:**
   ```bash
   cd Data-Dynamos
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Follow prompts:**
   - Link to an existing Vercel project or create new
   - Select project name
   - Select `./` as root directory

### Option B: Using GitHub

1. Push Data-Dynamos to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Set root directory to `Data-Dynamos`
6. Deploy

## Step 3: Setup Environment Variables (Optional)

If you want to use environment variables instead of hardcoding URLs:

1. In Vercel Dashboard → Project Settings → Environment Variables
2. Add: `VITE_API_URL = https://your-render-backend.onrender.com/api`

Then update index.html:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://your-render-backend.onrender.com/api';
```

## Step 4: Configure Backend CORS

Your Render backend needs to allow requests from Vercel. Update your backend (Flask/Node.js):

### For Python (app.py):
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://your-vercel-domain.vercel.app",
            "localhost:3000",
            "localhost:5000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

### For Node.js (server.js):
```javascript
const cors = require('cors');

app.use(cors({
  origin: [
    'https://your-vercel-domain.vercel.app',
    'http://localhost:3000'
  ],
  credentials: true
}));
```

## Step 5: Test the Connection

1. Deploy to Vercel
2. Open your Vercel URL in browser
3. Try the "Analyze" button
4. Check browser console (F12 → Console) for any CORS errors

## Troubleshooting

### CORS Errors
- Make sure your Render backend CORS settings include your Vercel URL
- Check that API_BASE_URL in index.html matches your actual Render URL

### 404 Errors on API Calls
- Verify the API endpoint paths match your backend (e.g., `/api/analyze`, `/api/geocode`)
- Check Render backend logs

### Image/Asset Loading Issues
- All images are loaded from CDN (Leaflet, Google Fonts)
- No local assets required

## Your URLs After Deployment

- **Frontend (Vercel):** `https://your-project.vercel.app`
- **Backend (Render):** `https://your-service.onrender.com`
- **API Calls:** `https://your-service.onrender.com/api/analyze`

---

For questions or issues, check:
- Render dashboard logs
- Vercel deployment logs
- Browser console (F12)
