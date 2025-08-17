#!/bin/bash

# Pre-deployment setup script
# This script prepares your portfolio for Google Cloud deployment

echo "🔧 Setting up portfolio for Google Cloud deployment..."

# Check if running in portfolio directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the portfolio directory"
    exit 1
fi

# Create necessary directories
mkdir -p instance
mkdir -p static/certificates

# Check if certificates exist
echo "📋 Checking certificate files..."
if [ ! -f "static/certificates/Coursera_duke.pdf" ]; then
    echo "⚠️  Certificate file not found: static/certificates/Coursera_duke.pdf"
    echo "   Please add your certificate files to the static/certificates/ directory"
fi

# Update gitignore for deployment
echo "📝 Updating .gitignore..."
cat >> .gitignore << EOF

# Google Cloud
.gcloudignore

# Deployment
deployment.log
*.bak

# Instance data
instance/
EOF

# Check Python dependencies
echo "🐍 Checking Python dependencies..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi

# Install dependencies locally for testing
echo "📦 Installing dependencies locally..."
pip3 install -r requirements.txt

# Test app locally
echo "🧪 Testing application..."
python3 -c "
import app
try:
    app.init_app()
    print('✅ App initialization successful')
except Exception as e:
    print(f'❌ App initialization failed: {e}')
    exit(1)
"

echo "✅ Pre-deployment setup complete!"
echo ""
echo "Next steps:"
echo "1. Run: gcloud auth login"
echo "2. Run: gcloud config set project YOUR_PROJECT_ID"
echo "3. Run: ./deploy.sh"
echo ""
echo "Or follow the DEPLOYMENT_GUIDE.md for detailed instructions."
