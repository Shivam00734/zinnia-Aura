@echo off
echo Reverting lifecycle changes...
copy "resources\zinnialive.resource.backup" "resources\zinnialive.resource"
echo Original zinnialive.resource restored from backup
echo.
echo Note: You may also want to remove the lifecycle-only methods from ZinniaLive.py
echo if they are no longer needed (lines ~2292-2385)
pause
