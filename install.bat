@echo off
title Discord.py BOT Module Installer
echo.
echo.
echo Press the space bar to start installing the module.
echo.
echo.

pause
echo.
echo.
echo %DATE%
python --version

python -m pip install -U pip
pip install discord.py
pip install discord.py[voice]
pip install python-dotenv
pip install logging
pip install youtube_dl
pip install datetime
pip install pytz
pip install youtube-search-python

echo.
echo.
echo You have completed installing the modules required to run the Bot.
echo.
echo.
pause
