# V3.1.0 Git Push and Streamlit Cloud Deployment Guide

**Version**: V3.1.0
**Status**: Ready to push to GitHub and deploy to Streamlit Cloud

---

## Current Git Status

**Local repository**: Ahead of remote by 7 commits
**Remote repository**: https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git

---

## Push Methods

### Method 1: Using GitHub Personal Access Token (Recommended)

#### Step 1: Create GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Enter Token description: `V3.1.0 - Seedance Tool`
4. Select permissions:
   - ✅ `repo` (Full control of private repositories)
5. Click "Generate token"
6. **Important**: Copy the generated token (shown only once)

#### Step 2: Push using Token URL

```bash
cd /workspace/projects/apps/seedance-tool-streamlit

# Push using Token URL (replace USERNAME and TOKEN)
git push https://USERNAME:TOKEN@github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git main
```

**Example**:
```bash
git push https://jinshanguzhou1021-afk:ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git main
```

---

### Method 2: Using GitHub Web Interface

#### Step 1: Create Pull Request

1. Open your GitHub repository: https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit
2. Click "Pull requests"
3. Click "New pull request"
4. Select base: `main`
5. Select compare: `main`
6. Click "Create pull request"
7. Click "Merge pull request"

---

### Method 3: Using GitHub Desktop

#### Step 1: Download GitHub Desktop

1. Go to: https://desktop.github.com/
2. Download and install GitHub Desktop

#### Step 2: Clone Repository

1. Open GitHub Desktop
2. Click "File" > "Clone repository"
3. Enter repository URL: `https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git`
4. Choose local path
5. Click "Clone"

#### Step 3: Push Changes

1. Open repository in GitHub Desktop
2. Check "Changes" or "History"
3. Click "Push origin"

---

## Streamlit Cloud Deployment

### Step 1: Login to Streamlit Cloud

1. Open browser and go to: https://streamlit.io/cloud
2. Click "Sign up" or "Log in"
3. Login with your GitHub account

### Step 2: Create New App

1. Click "New app"
2. Fill in app information:
   - **App name**: `seedance-tool-v3.1.0`
   - **Repository**: `jinshanguzhou1021-afk/seedance-tool-streamlit`
   - **Branch**: `main`
   - **Main file path**: `app_v3.1.0_integrated.py`
3. Click "Deploy"

### Step 3: Configure Secrets (API Key)

1. After deployment, click app name to go to settings
2. Click "Secrets"
3. Add new Secret:
   - **Key**: `DEEPSEEK_API_KEY`
   - **Value**: `sk-2f2c80b0af064d2a8ef04990630c8d7d`
4. Click "Save"

### Step 4: Redeploy

1. After configuring secrets, click "Deploy"
2. Wait for deployment to complete
3. Click app URL to access the app

---

## Accessing the App

### App URL Format

After deployment, Streamlit Cloud will provide an app URL:

```
https://[your-app-name]-[random-string].streamlit.app
```

### Example URL

```
https://seedance-tool-v3.1.0-xyz123.streamlit.app
```

---

## Secrets Configuration

### Required Secrets

Configure the following Secret in Streamlit Cloud:

| Key | Value | Description |
|-----|-------|-------------|
| **DEEPSEEK_API_KEY** | sk-2f2c80b0af064d2a8ef04990630c8d7d | DeepSeek V3 API Key |

### Optional Secrets

| Key | Value | Description |
|-----|-------|-------------|
| **OPENAI_API_KEY** | your-openai-api-key | OpenAI API Key (optional) |
| **OPENAI_BASE_URL** | https://api.openai.com/v1 | OpenAI API URL (optional) |

---

## Testing After Deployment

### Test Steps

1. **Access App**
   - Open app URL
   - Wait for app to load

2. **Test Storyboard Generator**
   - Switch to "📝 Storyboard Generator"
   - Enter creative description
   - Set parameters
   - Click generate
   - Verify output

3. **Test Prompt Builder**
   - Switch to "🧩 Prompt Builder"
   - Test Manual mode
   - Test AI Professional mode
   - Verify output

4. **Test History**
   - View history records
   - Test search function

5. **Test About Page**
   - View version information
   - Verify all information correct

---

## Troubleshooting

### Issue 1: Deployment Failed

**Possible causes**:
- Wrong main file path
- Missing dependencies
- Code errors

**Solutions**:
1. Check main file path is `app_v3.1.0_integrated.py`
2. Check `requirements.txt` exists
3. Check code for syntax errors
4. Check deployment logs

### Issue 2: API Call Failed

**Possible causes**:
- API Key not configured
- Wrong API Key
- Insufficient API quota

**Solutions**:
1. Check `DEEPSEEK_API_KEY` in Secrets
2. Verify API Key is correct
3. Check API quota

### Issue 3: App Won't Start

**Possible causes**:
- Dependency conflicts
- Port conflicts
- Environment incompatibility

**Solutions**:
1. Check `requirements.txt`
2. Check app logs
3. Try redeploying

---

## Best Practices

### 1. Version Management

- Use Git tags for versioning
- Keep main branch stable
- Use feature branches for new features

### 2. Secrets Management

- Don't write API Keys in code
- Use Streamlit Secrets for sensitive information
- Update API Keys regularly

### 3. Logging

- Use `logging` module for logging
- Set appropriate log level
- Avoid excessive logging in production

### 4. Error Handling

- Use try-except for exception handling
- Provide friendly error messages
- Log errors appropriately

---

## Technical Support

### Documentation

- **Version Release**: V3.1.0_正式发布完成报告.md
- **Deployment Guide**: Streamlit_Cloud_部署指南_V3.1.0.md
- **Push Script**: git_push_v3.1.0.sh

### GitHub Repository

https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git

### Streamlit Cloud Documentation

https://docs.streamlit.io/streamlit-cloud/get-started

---

## Push Summary

**Status**: Ready to push to GitHub
**Local ahead**: 7 commits
**Remote repository**: https://github.com/jinshanguzhou1021-afk/seedance-tool-streamlit.git

**Next Steps**:
1. Choose push method (Recommended: GitHub Token)
2. Push code to GitHub
3. Deploy to Streamlit Cloud
4. Update Streamlit Cloud URL

---

**Ready to push to GitHub and deploy to Streamlit Cloud!**
