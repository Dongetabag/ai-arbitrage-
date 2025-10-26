# 🚀 Railway Deployment Guide - AI Arbitrage Backend

## Quick Deploy to Railway

### Step 1: Create GitHub Repository
```bash
# Your code is already committed locally
# Now push to GitHub:

# Create a new repository on GitHub.com
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/ai-arbitrage-backend.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Railway
1. Go to [Railway.app](https://railway.app/new)
2. Click **"Deploy from GitHub repo"**
3. Connect your GitHub account
4. Select your `ai-arbitrage-backend` repository
5. Railway will auto-detect Python and start building

### Step 3: Set Environment Variables
In Railway dashboard, go to **Variables** tab and add:

```
GOOGLE_API_KEY=AIzaSyBOXCq6SjXVOJg7ulD4CT8FoMEvf-wq2ng
AI_PROVIDER=google
AI_MODEL=gemini-2.5-flash
PORT=8000
HOST=0.0.0.0
DATABASE_URL=sqlite:///arbitrage.db
```

### Step 4: Get Your Backend URL
Railway will give you a URL like:
```
https://ai-arbitrage-backend-production-xxxx.up.railway.app
```

### Step 5: Update Frontend
Once you have your backend URL, update the frontend:

```bash
# Edit frontend/out/index.html
# Replace the API_URL with your Railway URL
const API_URL = 'https://your-railway-url.up.railway.app';
```

## Alternative: Deploy to Render

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy to Render
1. Go to [Render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub and select your repository
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api/fastapi_endpoints.py`
   - **Environment**: Python 3

### Step 3: Set Environment Variables
In Render dashboard, add the same variables as above.

## What Happens After Deployment

✅ **Backend goes live** with Google Gemini AI  
✅ **Database initializes** automatically  
✅ **API endpoints** become accessible  
✅ **Frontend connects** to live backend  
✅ **Real opportunities** start appearing  
✅ **Force scan** triggers actual marketplace search  

## Testing Your Deployment

1. **Health Check**: Visit `https://your-backend-url/health`
2. **API Test**: Visit `https://your-backend-url/api/opportunities`
3. **Frontend**: Update frontend with backend URL
4. **Full Test**: Use force scan feature

## Troubleshooting

### Common Issues:
- **Build fails**: Check Python version (3.11+)
- **Import errors**: Ensure all dependencies in requirements.txt
- **Environment variables**: Double-check all variables are set
- **Port issues**: Railway auto-assigns port, use `PORT` env var

### Logs:
- Railway: View logs in dashboard
- Render: View logs in service dashboard

## Cost
- **Railway**: FREE (500 hours/month)
- **Render**: FREE (750 hours/month)
- **Total**: $0/month

Your AI arbitrage system will run completely free!
