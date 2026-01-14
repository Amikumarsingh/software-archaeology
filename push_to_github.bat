@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Software Archaeology - GitHub Push
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Initialize Git if needed
if not exist .git (
    echo [1/5] Initializing Git repository...
    git init
    git branch -M main
) else (
    echo [1/5] Git repository already initialized
)

REM Add and commit
echo [2/5] Adding files...
git add .

echo [3/5] Committing...
git commit -m "Initial commit: Software Archaeology - Codebase Time Machine" 2>nul
if errorlevel 1 (
    echo No changes to commit or already committed
)

REM Prompt for GitHub username
echo.
echo [4/5] GitHub Setup
set /p GITHUB_USER="Enter your GitHub username: "

if "!GITHUB_USER!"=="" (
    echo ERROR: Username cannot be empty
    pause
    exit /b 1
)

set REPO_NAME=software-archaeology
set REPO_URL=https://github.com/!GITHUB_USER!/!REPO_NAME!.git

echo.
echo ========================================
echo IMPORTANT: Create GitHub Repository
echo ========================================
echo 1. Opening GitHub in your browser...
echo 2. Create a new repository named: %REPO_NAME%
echo 3. Do NOT initialize with README, .gitignore, or license
echo 4. Press any key after creating the repository...
echo.

start https://github.com/new

pause

REM Add remote
echo.
echo [5/5] Pushing to GitHub...
git remote remove origin 2>nul
git remote add origin !REPO_URL!

echo Pushing to: !REPO_URL!
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo Push failed. Common solutions:
    echo ========================================
    echo 1. Make sure the repository exists on GitHub
    echo 2. Check your GitHub credentials
    echo 3. Try: git push -u origin main --force
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS! Repository pushed to GitHub
echo ========================================
echo.
echo Repository: !REPO_URL!
echo.
echo ========================================
echo Enable GitHub Pages (Live Hosting):
echo ========================================
echo 1. Opening repository settings...
echo 2. Go to: Settings ^> Pages
echo 3. Under "Build and deployment":
echo    - Source: GitHub Actions
echo 4. Wait 2-3 minutes for deployment
echo 5. Your site will be live at:
echo    https://!GITHUB_USER!.github.io/software-archaeology/
echo.

start https://github.com/!GITHUB_USER!/!REPO_NAME!/settings/pages

echo Press any key to exit...
pause >nul
