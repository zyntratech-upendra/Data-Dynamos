# Data-Dynamos Backend - Render Deployment Guide

## Prerequisites

- Render account (free tier available)
- Google Cloud Project with Earth Engine API enabled
- GitHub repository with your code

## Step 1: Set Up Google Earth Engine Credentials

### A. Create Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project or create a new one
3. Enable the **Earth Engine API**:
   - Go to APIs & Services → Library
   - Search for "Earth Engine API"
   - Click Enable

4. Create a Service Account:
   - APIs & Services → Credentials
   - Click "Create Credentials" → "Service Account"
   - Give it a name like `render-earthengine-service`
   - Click Create

5. Generate JSON Key:
   - Click on the service account you created
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose **JSON**
   - Download the JSON file (save it safely)

6. Register with Earth Engine:
   - Go to [Earth Engine Sign Up](https://signup.earthengine.google.com/#!/)
   - Use the service account email: `your-service-account@your-project.iam.gserviceaccount.com`
   - Wait for approval (usually a few minutes)

### B. Add Credentials to Render

1. Copy the contents of your downloaded JSON key
2. Go to your Render service dashboard
3. Go to **Settings** → **Environment**
4. Add new environment variable:
   - **Key:** `GOOGLE_APPLICATION_CREDENTIALS_JSON`
   - **Value:** (Paste the entire JSON content)

## Step 2: Update Your Backend Code

Your `app.py` has already been updated to remove the template issue. But we need to handle Earth Engine authentication properly for Render.

Create an `ee_auth.py` file in your Data-Dynamos folder:

```python
import json
import os
import ee
import logging

logging.basicConfig(level=logging.INFO)

def initialize_earth_engine():
    """Initialize Earth Engine with credentials from Render environment"""
    try:
        # Try to authenticate with credentials JSON from environment
        credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        
        if credentials_json:
            # Save credentials to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                f.write(credentials_json)
                credentials_path = f.name
            
            # Authenticate with service account
            credentials = ee.ServiceAccountCredentials(
                email=None,
                key_file=credentials_path
            )
            ee.Initialize(credentials)
            logging.info("✓ Earth Engine initialized with service account")
            
        else:
            # Fallback: try default initialization
            ee.Initialize(project='spectramining')
            logging.info("✓ Earth Engine initialized with default project")
            
    except Exception as e:
        logging.error(f"✗ Earth Engine initialization failed: {e}")
        logging.error("Earth Engine features will not work. Set GOOGLE_APPLICATION_CREDENTIALS_JSON env var.")
```

Then update your `app.py` to use this:

```python
# Replace the Earth Engine initialization block with:
from ee_auth import initialize_earth_engine
initialize_earth_engine()
```

## Step 3: Create Render Configuration Files

### A. render.yaml (for Render native build)

Create `render.yaml` in your Data-Dynamos folder:

```yaml
services:
  - type: web
    name: spectramining-backend
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
```

### B. requirements.txt

Make sure it includes these (update if needed):

```
Flask==2.3.0
Flask-CORS==4.0.0
google-cloud-ee==0.3.0
ee==0.2.30
geopy==2.3.0
Werkzeug==2.3.0
gunicorn==21.2.0
```

### C. Procfile (Traditional Render deployment)

If you're not using render.yaml:

```
web: gunicorn app:app
```

## Step 4: Deploy to Render

### Option A: Using GitHub (Recommended)

1. Push your code to GitHub
2. Go to [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Set these settings:
   - **Name:** `spectramining-backend`
   - **Root Directory:** `Data-Dynamos`
   - **Environment:** `Python 3.11`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free (or paid for better performance)

6. Click "Create Web Service"

### Option B: Using Render CLI

```bash
npm install -g render
render login
cd Data-Dynamos
render create-service
```

## Step 5: Add Environment Variables on Render

1. Go to your Render dashboard
2. Select your service
3. Click "Environment"
4. Add:
   - **Key:** `GOOGLE_APPLICATION_CREDENTIALS_JSON`
   - **Value:** (Paste full JSON from your service account key)

5. Click "Save" (this will redeploy your service)

## Step 6: Connect Frontend to Backend

In your Vercel frontend (`index.html`), set:

```javascript
const API_BASE_URL = 'https://your-service-name.onrender.com/api';
```

## Step 7: Test Your Deployment

1. Visit `https://your-service-name.onrender.com/`
   - Should return JSON with service info

2. Check health endpoint:
   ```
   https://your-service-name.onrender.com/api/health
   ```

3. Check Render logs for any Earth Engine errors

## Troubleshooting

### Earth Engine Still Not Initialized
- Verify service account is registered with Earth Engine
- Check JSON credentials are valid
- Try adding this to `app.py`:
  ```python
  import os
  print("Credentials available:", bool(os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')))
  ```

### 503 Service Unavailable
- Give Render 2-3 minutes to finish deployment
- Check logs for Python errors
- Verify `gunicorn` is in requirements.txt

### CORS Errors from Frontend
- Verify `Flask-CORS` is in requirements.txt
- CORS is already enabled in your `app.py` with `CORS(app)`

### Slow Performance
- Render free tier is slow. Upgrade to paid tier for better performance
- Free tier also spins down after 15 minutes of inactivity

## Your Deployment URLs

After deployment:
- **Backend API:** `https://your-service-name.onrender.com`
- **API Endpoints:** `https://your-service-name.onrender.com/api/analyze`, etc.
- **Frontend (Vercel):** `https://your-project.vercel.app`

## Next Steps

1. Update Earth Engine credentials in Render dashboard
2. Deploy backend with `git push`
3. Deploy frontend to Vercel with updated API URL
4. Test the connection between frontend and backend
