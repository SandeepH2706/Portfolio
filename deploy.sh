#!/bin/bash

# Portfolio Deployment Script for Google Cloud Platform
# This script automates the deployment process to Google App Engine

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    print_error "Google Cloud CLI is not installed. Please install it first:"
    echo "https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    print_warning "Not authenticated with Google Cloud. Running authentication..."
    gcloud auth login
fi

# Set project variables
PROJECT_ID=""
REGION="us-central1"

echo "🚀 Portfolio Deployment to Google Cloud Platform"
echo "================================================"

# Get or set project ID
if [ -z "$PROJECT_ID" ]; then
    echo
    print_status "Available Google Cloud Projects:"
    gcloud projects list --format="table(projectId,name,projectNumber)"
    echo
    read -p "Enter your Google Cloud Project ID: " PROJECT_ID
fi

# Validate project ID
if ! gcloud projects describe "$PROJECT_ID" &>/dev/null; then
    print_error "Project '$PROJECT_ID' not found or not accessible."
    exit 1
fi

# Set the project
print_status "Setting project to: $PROJECT_ID"
gcloud config set project "$PROJECT_ID"

# Enable required APIs
print_status "Enabling required Google Cloud APIs..."
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Check if App Engine app exists
if ! gcloud app describe &>/dev/null; then
    print_warning "App Engine application not found. Creating one..."
    read -p "Enter region for App Engine (default: us-central): " app_region
    app_region=${app_region:-us-central}
    gcloud app create --region="$app_region"
fi

# Build and deploy
print_status "Preparing for deployment..."

# Generate a random secret key for production
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Update app.yaml with the secret key
print_status "Updating app.yaml with production secret key..."
sed -i.bak "s/your-production-secret-key-here-change-this/$SECRET_KEY/" app.yaml

# Deploy to App Engine
print_status "Deploying to Google App Engine..."
gcloud app deploy app.yaml --quiet

# Get the deployed URL
APP_URL=$(gcloud app describe --format="value(defaultHostname)")

# Restore original app.yaml
mv app.yaml.bak app.yaml

print_success "Deployment completed successfully!"
echo
echo "🌐 Your portfolio is now live at: https://$APP_URL"
echo
echo "📊 Useful commands:"
echo "   View logs:    gcloud app logs tail -s default"
echo "   Open browser: gcloud app browse"
echo "   View app:     gcloud app describe"
echo
print_status "Deployment summary saved to deployment.log"

# Save deployment info
cat > deployment.log << EOF
Deployment completed at: $(date)
Project ID: $PROJECT_ID
App URL: https://$APP_URL
Region: $REGION
Status: Successfully deployed
EOF

# Open the deployed app
read -p "Open the deployed app in browser? (y/n): " open_browser
if [[ $open_browser == "y" || $open_browser == "Y" ]]; then
    gcloud app browse
fi
