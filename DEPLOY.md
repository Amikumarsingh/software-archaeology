# 🚀 Quick Deploy Guide

## Option 1: Automated Script (Recommended)

Just run:
```bash
push_to_github.bat
```

The script will:
1. Initialize Git repository
2. Commit all files
3. Prompt for your GitHub username
4. Open GitHub to create the repository
5. Push everything automatically
6. Open GitHub Pages settings

## Option 2: Manual Steps

### Step 1: Initialize Git
```bash
git init
git branch -M main
git add .
git commit -m "Initial commit: Software Archaeology"
```

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `software-archaeology`
3. **Do NOT** initialize with README
4. Click "Create repository"

### Step 3: Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/software-archaeology.git
git push -u origin main
```

### Step 4: Enable GitHub Pages
1. Go to repository Settings → Pages
2. Under "Build and deployment":
   - Source: **GitHub Actions**
3. Wait 2-3 minutes

### Step 5: Access Your Live Site
```
https://YOUR_USERNAME.github.io/software-archaeology/
```

## What Gets Deployed?

The GitHub Actions workflow automatically:
- ✅ Installs Python dependencies
- ✅ Generates a demo report analyzing this repository
- ✅ Creates an interactive landing page
- ✅ Deploys everything to GitHub Pages

## Troubleshooting

### Push Failed?
```bash
# If repository already exists
git push -u origin main --force

# If authentication fails
# Use GitHub Personal Access Token as password
# Generate at: https://github.com/settings/tokens
```

### Pages Not Working?
1. Check Actions tab for deployment status
2. Ensure Pages source is set to "GitHub Actions"
3. Wait 2-3 minutes after first push

### Want to Update?
```bash
git add .
git commit -m "Update"
git push
```

## Live Demo

After deployment, your site will have:
- 🏠 Landing page at `/`
- 📊 Demo report at `/demo_report.html`
- 📁 All project files accessible

## Next Steps

1. Share your live demo: `https://YOUR_USERNAME.github.io/software-archaeology/`
2. Analyze other repositories and add more demo reports
3. Customize the landing page in `.github/workflows/deploy.yml`
