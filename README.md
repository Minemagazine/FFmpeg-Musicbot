# FFmpeg-Musicbot
Zeroy 봇의 기반이 되는 오픈소스 뮤직봇 </br>

### Python 3.8.10 | Windows 10, Linux Ubuntu Server 20.04.3 LTS
## 세팅
1. [Python 3.8.10](<https://www.python.org/downloads/release/python-3810>) 및 [FFmpeg](<https://www.ffmpeg.org/download.html>) 설치하기
2. 필요한 모듈 설치하기 </br>
3. .env file TOKEN = YOUR_TOKEN 설정하기 </br>
4. Prefix = BOT_Prefix 설정하기 </br>
5. index.py 실행 </br>

## 필요한 모듈 설치</br>
pip install discord.py </br>
pip install discord.py[voice] </br>
pip install python-dotenv </br>
pip install logging </br>
pip install youtube_dl </br>
pip install datetime </br>
pip install pytz </br>
pip install youtube-search-python </br>

### 현재 명령어:
prefix/help : Discord.py 기본 Help </br>
prefix/join : 음성채널 접속 </br>
prefix/leave : 음성채널 연결 끊기 </br>
prefix/play <song> : 음악 재생 </br>

#### 그다음 업데이트..
> 대기열 기능 </br>
> 스킵, 일시정지, 재개 등 재생 컨트롤 명령어 </br>
