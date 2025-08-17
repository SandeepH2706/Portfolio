# 🚀 Portfolio Deployment Guide - Google Cloud Platform

This guide will help you deploy your portfolio website to Google Cloud Platform using Google App Engine.

## 📋 Prerequisites

1. **Google Cloud Account**: Sign up at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud Project**: Create a new project or use existing one
3. **Google Cloud CLI**: Install from [cloud.google.com/sdk](https://cloud.google.com/sdk/docs/install)
4. **Billing Account**: Enable billing for your project (free tier available)

## 🛠️ Installation Steps

### Step 1: Install Google Cloud CLI

**macOS (using Homebrew):**
```bash
brew install --cask google-cloud-sdk
```

**Or download directly:**
- Visit: https://cloud.google.com/sdk/docs/install
- Download and run the installer

### Step 2: Initialize and Authenticate

```bash
# Initialize gcloud
gcloud init

# Login to your Google account
gcloud auth login

# Set your project (replace YOUR_PROJECT_ID)
gcloud config set project YOUR_PROJECT_ID
```

## 🚀 Deployment Options

### Option 1: Automated Deployment (Recommended)

Use the provided deployment script:

```bash
# Make script executable (already done)
chmod +x deploy.sh

# Run deployment script
./deploy.sh
```

The script will:
- ✅ Check prerequisites
- ✅ Enable required APIs
- ✅ Create App Engine application
- ✅ Generate secure secret key
- ✅ Deploy your portfolio
- ✅ Provide deployment URL

### Option 2: Manual Deployment

1. **Enable Required APIs:**
```bash
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

2. **Create App Engine Application:**
```bash
gcloud app create --region=us-central
```

3. **Deploy:**
```bash
gcloud app deploy app.yaml
```

4. **Open Your Site:**
```bash
gcloud app browse
```

## 📊 Post-Deployment Management

### View Logs
```bash
# Tail live logs
gcloud app logs tail -s default

# View recent logs
gcloud app logs read -s default --limit=100
```

### Update Your Site
```bash
# After making changes, redeploy
gcloud app deploy app.yaml
```

### View App Information
```bash
# Get app details
gcloud app describe

# View versions
gcloud app versions list
```

### Custom Domain (Optional)
```bash
# Map custom domain
gcloud app domain-mappings create YOUR_DOMAIN.com
```

## 💰 Cost Optimization

### Free Tier Limits
- **App Engine**: 28 frontend instance hours/day
- **Bandwidth**: 1GB outbound/day
- **Storage**: 1GB

### Monitor Usage
```bash
# Check quotas
gcloud compute project-info describe --format="table(quotas[].metric,quotas[].limit,quotas[].usage)"
```

## 🔧 Configuration Files

### `app.yaml` (App Engine Configuration)
- **Runtime**: Python 3.9
- **Scaling**: 0-5 instances
- **Security**: HTTPS enforced
- **Static files**: Optimized serving

### `requirements.txt` (Dependencies)
- Flask web framework
- SQLAlchemy database
- Gunicorn WSGI server

## 🐛 Troubleshooting

### Common Issues

1. **"App Engine application not found"**
   ```bash
   gcloud app create --region=us-central
   ```

2. **"Project not found"**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **"Permission denied"**
   ```bash
   gcloud auth login
   ```

4. **"Billing not enabled"**
   - Go to Cloud Console → Billing
   - Enable billing (free tier available)

### Debug Commands
```bash
# Check current configuration
gcloud config list

# Verify authentication
gcloud auth list

# Test deployment locally
dev_appserver.py app.yaml
```

## 🌟 Additional Features

### Environment Variables
Add to `app.yaml`:
```yaml
env_variables:
  FLASK_ENV: production
  DATABASE_URL: your-database-url
  SECRET_KEY: your-secret-key
```

### Custom Runtime
For more control, use `Dockerfile`:
```bash
gcloud app deploy --dockerfile
```

### Multiple Services
Deploy additional services:
```bash
gcloud app deploy service.yaml
```

## 📱 Mobile Optimization

Your portfolio is already mobile-responsive with:
- ✅ Responsive CSS Grid
- ✅ Mobile-friendly navigation
- ✅ Touch-optimized buttons
- ✅ Optimized images

## 🔒 Security Features

- ✅ HTTPS enforced
- ✅ Secure headers
- ✅ Environment variables for secrets
- ✅ Static file optimization

## 📈 Performance

### Built-in Optimizations
- **CDN**: Global content delivery
- **Caching**: Automatic static file caching
- **Compression**: Gzip compression enabled
- **Auto-scaling**: Handles traffic spikes

### Monitoring
```bash
# View performance metrics
gcloud app operations list
```

## 🎯 Next Steps

After deployment:

1. **Test your site**: Visit the provided URL
2. **Check logs**: Monitor for any issues
3. **Update content**: Make changes and redeploy
4. **Add custom domain**: Optional branding
5. **Monitor usage**: Keep track of quotas

## 📞 Support

- **Google Cloud Docs**: [cloud.google.com/appengine/docs](https://cloud.google.com/appengine/docs)
- **Stack Overflow**: Tag questions with `google-app-engine`
- **Community**: [cloud.google.com/community](https://cloud.google.com/community)

---

**Happy Deploying! 🚀**

Your portfolio will be live at: `https://YOUR_PROJECT_ID.appspot.com`
