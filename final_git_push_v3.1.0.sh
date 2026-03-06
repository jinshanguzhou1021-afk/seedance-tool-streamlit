#!/bin/bash
# Final Git Push Script for V3.1.0

echo "=========================================="
echo "🚀 V3.1.0 - Final Git Push"
echo "=========================================="
echo ""

cd /workspace/projects/apps/seedance-tool-streamlit

echo "📌 Current Git Status"
echo "-" * 60

git status --short

echo ""
echo "📌 Removing problematic files"
echo "-" * 60

# Remove files with special characters
find . -maxdepth 1 -name "*\[*" -type f -exec rm -v {} \; 2>/dev/null
find . -maxdepth 1 -name "*\]*" -type f -exec rm -v {} \; 2>/dev/null

echo ""
echo "📌 Adding new files"
echo "-" * 60

git add Git_Push_and_Streamlit_Cloud_Deployment.md 2>/dev/null
git add git_push_v3.1.0.sh 2>/dev/null
git add Streamlit_Cloud_*.md 2>/dev/null

echo ""
echo "📌 Checking status again"
echo "-" * 60

git status --short

echo ""
echo "📌 Committing changes"
echo "-" * 60

git commit -m "Release: V3.1.0 - Final Git Push and Streamlit Cloud Deployment Guide

New files:
- Git_Push_and_Streamlit_Cloud_Deployment.md - Complete deployment guide
- git_push_v3.1.0.sh - Git push script
- Streamlit_Cloud_*.md - Deployment guides

Git Status:
- Local ahead of remote: 7-8 commits
- Files cleaned and organized
- Ready to push

Deployment Guide:
- Push methods: GitHub Token, SSH, Web Interface
- Streamlit Cloud deployment steps
- Secrets configuration guide
- Troubleshooting guide

Next Steps:
1. Push to GitHub using recommended method
2. Deploy to Streamlit Cloud
3. Update Streamlit Cloud URL
4. Test all features

Version: V3.1.0
Status: Ready to push and deploy

Ready to push to GitHub and deploy to Streamlit Cloud!" 2>&1 | head -50

echo ""
echo "=========================================="
echo "📊 Commit Summary"
echo "=========================================="
echo ""

echo "Git Status:"
git log --oneline -3

echo ""
echo "🚀 Push to GitHub:"
echo "  Method 1 (Recommended): GitHub Token"
echo "  Method 2: GitHub Web Interface"
echo "  Method 3: GitHub Desktop"
echo ""
echo "🌐 Deploy to Streamlit Cloud:"
echo "  1. Login to https://streamlit.io/cloud"
echo "  2. Create new app"
echo "  3. Configure secrets (DEEPSEEK_API_KEY)"
echo "  4. Deploy and access app"
echo ""
echo "=========================================="
