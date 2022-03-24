:gitupdate
git pull
:startbot
python botrunner.py
if %ERRORLEVEL% EQU 2 goto startbot
if %ERRORLEVEL% EQU 6 goto gitupdate