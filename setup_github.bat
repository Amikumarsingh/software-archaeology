@echo off
echo ========================================
echo Software Archaeology - GitHub Setup
echo ========================================
echo.

REM Check if git is initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    git branch -M main
) else (
    echo Git repository already initialized.
)

REM Add all files
echo Adding files to Git...
git add .

REM Commit
echo Committing files...
git commit -m "Initial commit: Software Archaeology - Codebase Time Machine"

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Create a new repository on GitHub: https://github.com/new
echo 2. Name it: software-archaeology
echo 3. Do NOT initialize with README (we already have one)
echo 4. Copy the repository URL
echo 5. Run: git remote add origin YOUR_REPO_URL
echo 6. Run: git push -u origin main
echo.
echo After pushing, enable GitHub Pages:
echo 1. Go to Settings ^> Pages
echo 2. Source: GitHub Actions
echo 3. Wait 2-3 minutes for deployment
echo 4. Your site will be live at: https://YOUR_USERNAME.github.io/software-archaeology/
echo.
pause
