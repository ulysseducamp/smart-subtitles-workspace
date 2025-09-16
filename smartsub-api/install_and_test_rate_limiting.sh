#!/bin/bash

# Script to install slowapi and test rate limiting functionality
# Usage: ./install_and_test_rate_limiting.sh

echo "🚀 Installing slowapi and testing rate limiting..."
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Please run this script from the smartsub-api directory."
    exit 1
fi

# Install slowapi
echo "📦 Installing slowapi..."
pip install slowapi==0.1.9

if [ $? -ne 0 ]; then
    echo "❌ Failed to install slowapi"
    exit 1
fi

echo "✅ slowapi installed successfully"

# Check if API_KEY is set
if [ -z "$API_KEY" ]; then
    echo "⚠️  Warning: API_KEY environment variable not set"
    echo "   You can set it with: export API_KEY=your_api_key_here"
    echo "   Or the test will use a fallback key"
fi

# Run quick test
echo ""
echo "🧪 Running quick rate limiting test..."
echo "====================================="

python test_rate_limiting_quick.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Quick test completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Deploy the updated code to Railway"
    echo "   2. Run the full test: python test_rate_limiting.py"
    echo "   3. Monitor the logs for rate limiting activity"
else
    echo ""
    echo "❌ Quick test failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "🎉 Rate limiting setup completed!"
