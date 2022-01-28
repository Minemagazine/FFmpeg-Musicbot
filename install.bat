@echo off
title Discord.py BOT Module Installer
echo.
echo.
echo 스페이스바를 누르면 모듈 설치가 시작됩니다
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
echo 모듈 설치가 끝났습니다.
echo 아무키나 눌러서 종료하기
echo.
echo.
pause
