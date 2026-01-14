# GitHub Setup Instructions

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `software-archaeology`
3. Description: `Codebase Time Machine - Analyze Git repository evolution`
4. Make it Public
5. Don't initialize with README (we already have one)
6. Click "Create repository"

## Step 2: Push to GitHub

Run these commands in your terminal:

```bash
git remote add origin https://github.com/YOUR_USERNAME/software-archaeology.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click "Settings" tab
3. Click "Pages" in the left sidebar
4. Under "Source", select "GitHub Actions"
5. Click "Save"

## Step 4: Wait for Deployment

1. Go to the "Actions" tab in your repository
2. You'll see the "Deploy Demo to GitHub Pages" workflow running
3. Wait ~2-3 minutes for it to complete
4. Once done, your site will be live at:
   `https://YOUR_USERNAME.github.io/software-archaeology/`

## Step 5: View Your Live Demo

Visit: `https://YOUR_USERNAME.github.io/software-archaeology/`

The demo will show:
- Landing page with project info
- Live demo report analyzing this repository itself
- Links to GitHub repo

## Troubleshooting

If the workflow fails:
1. Check the Actions tab for error logs
2. Make sure the repository is public
3. Verify GitHub Pages is enabled in Settings

## Update the Demo

Every time you push to main branch, the demo will automatically regenerate!

```bash
git add .
git commit -m "Update project"
git push
```
