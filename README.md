[![image](https://camo.githubusercontent.com/92ea74d7973332713853b8c55160f4aa90287bb2e110273868dbe03e35d47391/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f6e657874636f72642e737667)](<https://python.org>)
[![image](https://camo.githubusercontent.com/324d18ad5779de51284f50c943a0fd12d62f11c3e1f8d114480082e439e082ce/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f6c6963656e73652f4d6967616e3137382f6b75626f74)](<https://www.gnu.org/licenses/gpl-3.0.html>)
# FFmpeg-Musicbot
Zeroy 봇의 기반이 되는 오픈소스 뮤직봇 </br>

### [Python 3.8.10](<https://www.python.org/downloads/release/python-3810>) | [Windows 10](<https://www.microsoft.com/ko-kr/software-download/windows10>) 및 [Linux Ubuntu Server 20.04.3 LTS](<https://ubuntu.com/download/server>) 전용
## 세팅
1. [Python 3.8.10](<https://www.python.org/downloads/release/python-3810>) 및 [FFmpeg](<https://www.ffmpeg.org/download.html>) 설치하기
2. 필요한 모듈 설치하기 </br>
3. .env 파일에 `TOKEN = (토큰)` 설정하기 </br>
4. `Prefix = (접두사)` 설정하기 </br>
5. index.py 실행 </br>

## [필요한 모듈 설치](<https://pypi.org/>)</br>
pip install nextcord </br>
pip install nextcord[voice] </br>
pip install nextcord[speed] </br>
pip install python-dotenv </br>
pip install logging </br>
pip install youtube_dl </br>
pip install datetime </br>
pip install pytz </br>
pip install youtube-search-python </br>

### 현재 명령어:
prefix/help : Discord Cogs Help </br>
prefix/join : 음성채널 접속 </br>
prefix/leave : 음성채널 연결 끊기 </br>
prefix/play <song> : 음악 재생 (대기열 가능) </br>
prefix/skip : 음악 스킵 </br>

#### 그다음 업데이트..
> 일시정지, 재개 등 재생 컨트롤 명령어 </br>
