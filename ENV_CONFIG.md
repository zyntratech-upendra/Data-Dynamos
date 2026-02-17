# Environment Configuration Guide

## .env File Setup

### Step 1: Copy .env.example to .env

```bash
cp .env.example .env
```

### Step 2: Update .env with Your Render Backend URL

Edit `.env` and replace the placeholder with your actual Render service URL:

```env
VITE_API_URL=https://your-actual-service-name.onrender.com/api
VITE_ENV=production
```

**Example:**
If your Render service URL is `https://spectramining-xyz.onrender.com`, set:
```env
VITE_API_URL=https://spectramining-xyz.onrender.com/api
```

### Step 3: For Local Development

To test locally with your backend running on localhost:5000:

```env
VITE_API_URL=http://localhost:5000/api
VITE_ENV=development
```

## Vercel Deployment Configuration

### Method 1: Using Vercel Environment Variables (Recommended)

1. Go to your **Vercel Dashboard**
2. Select your project (Data-Dynamos)
3. Go to **Settings → Environment Variables**
4. Add a new variable:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://your-render-service.onrender.com/api`
   - **Environments:** Select "Production" (or all if needed)
5. Click **Save** → Project will redeploy automatically

### Method 2: Using a Custom Domain Wrapper

If you want the API URL to be a custom domain that points to Render:

1. Create a CNAME record pointing to your Render backend
2. In Vercel env vars, use your custom domain:
   ```
   VITE_API_URL=https://api.yourdomain.com/api
   ```

### Method 3: Using a Proxy (API Routes)

For advanced setups, create a Vercel API route that proxies requests to Render:

Create `api/proxy.js` in your project:
```javascript
export default async (req, res) => {
  const { path } = req.query;
  const renderUrl = process.env.RENDER_API_URL || 'https://your-service.onrender.com';
  const response = await fetch(`${renderUrl}/api/${path}`, {
    method: req.method,
    body: req.body,
    headers: req.headers
  });
  return res.status(response.status).json(await response.json());
};
```

Then update config.js to use `/api/proxy?path=...`

## File Structure

```
Data-Dynamos/
├── .env                 # Local environment variables (IGNORED by git)
├── .env.example         # Template for .env (COMMITTED to git)
├── .gitignore          # Prevents .env from being committed
├── config.js           # Runtime configuration manager
├── index.html          # Updated to use config.js
└── ...other files
```

## How It Works

1. **config.js** - Reads the API URL and provides it to the React app
2. **.env** - Contains your local configuration (never committed)
3. **Vercel Environment Variables** - Production settings managed in Vercel dashboard
4. **index.html** - Uses `window.__CONFIG__.getApiUrl()` to get the API endpoint

## Security Notes

- **Never commit `.env` to git** - It's in `.gitignore` for this reason
- **Use `.env.example`** - Share this template with your team, they create their own `.env`
- **Never expose secrets in HTML** - API URLs are okay to expose (they're public-facing anyway)
- **Use Vercel dashboard** for production secrets

## Testing Your Configuration

### Local Testing
1. Start your Flask backend: `python app.py`
2. Update `.env` to `VITE_API_URL=http://localhost:5000/api`
3. Open `index.html` in browser (or run local server)
4. Open DevTools (F12) → Console
5. Type: `console.log(window.__CONFIG__.getApiUrl())`
6. Should output: `http://localhost:5000/api`

### Production Testing (After Vercel Deployment)
1. Visit your Vercel URL
2. Open DevTools (F12) → Console
3. Type: `console.log(window.__CONFIG__.getApiUrl())`
4. Should output your Render API URL (from Vercel env var)

## Troubleshooting

### API URL not loading
- Check that `.env` file exists locally
- Check Vercel dashboard → Environment Variables for production
- Open DevTools → Console → Type `window.__CONFIG__`

### CORS errors
- Verify Render backend CORS settings allow your Vercel domain
- Check Render logs for blocked origins

### "API URL not configured" warning
- Ensure `VITE_API_URL` environment variable is set
- Check both local `.env` and Vercel environment variables

## Quick Reference Commands

```bash
# Copy template for local development
cp .env.example .env

# Edit with your Render URL
nano .env
# or
code .env

# Test configuration
# Open index.html in browser and check console

# Deploy to Vercel with new env var
git add .env.example
git commit -m "Add env configuration template"
git push
# Then set VITE_API_URL in Vercel dashboard
```
