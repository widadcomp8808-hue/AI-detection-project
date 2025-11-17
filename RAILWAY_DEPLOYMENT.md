# Railway Deployment Guide

## Prerequisites
- GitHub account with your repo pushed
- Railway account (sign up at [railway.app](https://railway.app))

## Step-by-Step Deployment

### 1. Push Your Code to GitHub
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Deploy on Railway

#### Option A: Using Railway Dashboard (Easiest)
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Authorize Railway to access your GitHub account
6. Select your phishing-detector repository
7. Click **"Deploy"**

Railway will automatically:
- Detect Node.js project
- Install dependencies (`npm install`)
- Start the server (`npm start`)

#### Option B: Using Railway CLI
```bash
# Install Railway CLI (if not already installed)
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 3. Configure Environment (if needed)
1. In Railway dashboard, go to your project
2. Click **"Variables"**
3. Add any environment variables needed
4. Changes apply automatically on redeploy

### 4. Access Your Website
- Railway assigns a public URL automatically
- Check **"Deployments"** tab in Railway dashboard
- Click the URL to view your live website

## What Railway Handles

✅ **Automatically:**
- Node.js runtime setup
- Python environment detection
- Dependency installation
- Port management (PORT env variable set automatically)
- Health checks and auto-restart
- HTTPS/SSL certificate
- Domain management

## Features

- **Auto-deploy**: Changes pushed to GitHub automatically deploy
- **Logs**: View real-time logs in dashboard
- **Rollback**: Revert to previous deployments instantly
- **Custom Domain**: Add your own domain in settings

## Troubleshooting

### Build fails
- Check logs in Railway dashboard
- Verify `package.json` exists
- Ensure `server.js` exists in root

### Application crashes
- Review logs for Python errors
- Check if model file is included
- Verify PORT environment variable is used

### Can't connect to API
- Ensure frontend uses `window.location.origin + '/api'`
- Check that server.js exports Express app properly
- Review deployment logs for startup errors

## Monitoring

- **Dashboard**: View real-time metrics
- **Logs**: Search and filter deployment logs
- **Alerts**: Set up notifications for failures

## Next Steps

Once deployed:
1. Share your Railway URL with users
2. Monitor logs for any issues
3. Set up custom domain if desired
4. Configure auto-deployment settings
