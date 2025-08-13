@echo off
echo ========================================
echo Taxora AI Finance Assistant
echo GitHub Deployment Script
echo ========================================

echo.
echo Step 1: Preparing repository for GitHub...

REM Remove sensitive files from git tracking
git rm --cached backend/.env 2>nul
git rm --cached -r __pycache__/ 2>nul
git rm --cached *.log 2>nul

echo.
echo Step 2: Adding all files to git...
git add .

echo.
echo Step 3: Creating commit...
git commit -m "Deploy Taxora AI Finance Assistant to GitHub - Multi-AI provider financial management system"

echo.
echo Step 4: Setting up GitHub remote...
echo Please enter your GitHub username:
set /p username="GitHub Username: "

echo.
echo Please enter your repository name (default: taxora-ai-finance):
set /p reponame="Repository Name: "
if "%reponame%"=="" set reponame=taxora-ai-finance

echo.
echo Setting up remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/%username%/%reponame%.git

echo.
echo Step 5: Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Your repository is now available at:
echo https://github.com/%username%/%reponame%
echo.
echo Next steps:
echo 1. Go to your GitHub repository
echo 2. Add repository description and topics
echo 3. Set up deployment (Heroku, Railway, etc.)
echo 4. Configure environment variables
echo.
echo For detailed deployment instructions, see:
echo DEPLOYMENT_GUIDE.md
echo.
pause
