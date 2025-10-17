@echo off
echo Committing Django-signals_orm-0x04 project...
cd /d "c:\Users\USER\Documents\Alx Projects\alx-backend-python"

echo Checking Git status...
git status

echo.
echo Committing files...
git commit -m "Add Django-signals_orm-0x04: Complete messaging app with signals, ORM, and caching"

echo.
echo Pushing to remote repository...
git push origin main

echo.
echo Done! Press any key to exit...
pause
