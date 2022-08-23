import nextcord, datetime, pytz, youtubesearchpython, json
from nextcord import client, FFmpegOpusAudio
from nextcord.ext import commands
from youtube_dl import YoutubeDL
from typing import Optional
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} # FFmpeg 옵션
YDL_OPTIONS = {'netrc':'$HOME/.netrc', 'format':'bestaudio/best', 'audio_format':'flac', 'audio_quality':'0', 'extract_audio':'True', 'noplaylist':'True', 'no_warnings':'True'} # YouTube DL 옵션
client = nextcord.Client()

global vc
vc = { } # Voice Client

global np
np = { } # 현재 재생중인 곡의 정보를 담아둘 딕셔너리 자료

global queue
queue = { }

def videoSearch(msg):
    videosSearch = youtubesearchpython.VideosSearch(str(msg), limit = 1).result()
    try:
        video = videosSearch['result'][0]
        title = video['title']
        url = video['link']
        try:
            image = video['thumbnails'][1]['url']
        except:
            try:
                image = video['thumbnails'][0]['url']
            except:
                image = 'https://www.salonlfc.com/wp-content/uploads/2018/01/image-not-found-1-scaled-1150x647.png'
        try:
            cname = video['channel']['name']
        except:
            cname = 'Channel Not Found'

        return title, url, image, cname

    except:
        return None

def reset(guild_id):
    pass

def ydl_url(url):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)

    URL = info['formats'][0]['url']
    return URL

def next_play(self, interaction):
    key = queue.get(interaction.guild.id)

    # 대기열이 없거나 0이면 나가기
    if key is None or len(queue[interaction.guild.id]['title']) == 0:
        client.loop.create_task(vc[interaction.guild.id].disconnect())
        client.loop.create_task(interaction.send("Left Voice Channel"))

    # 대기열이 있으면 재생하기
    else: 
        URL = ydl_url(url = queue[interaction.guild.id]['url'][0])
        np.update({interaction.guild.id:{
                    "title": key['title'][0],
                    "url": key['url'][0],
                    "image": key['image'][0],
                    "cname": key['cname'][0]
                }
            }
        )
        del queue[interaction.guild.id]['title'][0]
        del queue[interaction.guild.id]['url'][0]
        del queue[interaction.guild.id]['image'][0]
        del queue[interaction.guild.id]['cname'][0]



        vc[interaction.guild.id].play(FFmpegOpusAudio(URL, **FFMPEG_OPTIONS, bitrate=512), after = lambda e: next_play(self, interaction))
        embed = nextcord.Embed(title = ' ', description = f'[{np[interaction.guild.id]["title"]}](<{np[interaction.guild.id]["url"]}>)', color=0x2F3136, timestamp=datetime.datetime.now(pytz.timezone('UTC')))
        embed.set_author(name=np[interaction.guild.id]["cname"], url=np[interaction.guild.id]["url"], icon_url=self.client.user.avatar.url)
        embed.set_thumbnail(url=np[interaction.guild.id]["image"])
        embed.set_footer(text=interaction.author, icon_url=interaction.author.avatar.url)
        client.loop.create_task(interaction.send(embed = embed))



class music(commands.Cog):

    def __init__(self, client):
        self.count = 0
        self.client = client

        print(f'\033[96m Cogs Loading Success: Music\u001b[37m')

    @commands.Cog.listener() # 자동 퇴장
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                try:
                    await vc[member.guild.id].disconnect()
                except:
                    pass
                return

    @nextcord.slash_command(name="join", description="join") # 참가
    async def join(self, interaction: nextcord.Interaction):
        try:
            check_user_join_vcChannel = interaction.user.voice.channel.id
        except:
            await interaction.response.send_message('이 명령어를 사용하려면 음성 채널에 있어야 합니다.')
            return
            
        try:
            vc[interaction.guild.id] = await interaction.user.voice.channel.connect()

            await interaction.response.send_message(f'Joined {interaction.user.voice.channel.mention}')
        except:
            try:
                await interaction.user.voice.channel.connect().move_to(interaction.user.voice.channel.connect())
                await interaction.response.send_message(f'Moved {interaction.user.voice.channel.mention}')
            except:
                await interaction.response.send_message('먼저 음성채널에 참가해주세요!')
                return

    @nextcord.slash_command(name="leave", description="leave") # 나가기
    async def leave(self, interaction: nextcord.Interaction):
        try:
            check_user_join_vcChannel = interaction.user.voice.channel.id
        except:
            await interaction.response.send_message('이 명령어를 사용하려면 음성 채널에 있어야 합니다.')
            return

        try:
            await vc[interaction.guild.id].disconnect()
            await interaction.response.send_message(f'Left {interaction.user.voice.channel.mention}')

        except:
            await interaction.response.send_message('현재 접속중인 채널이 없어요!')
            return
            
        if check_user_join_vcChannel != vc[interaction.guild.id].channel.id:
            await interaction.response.send_message('봇과 같은 채널에 접속해 주세요!')
            return

    @nextcord.slash_command(name="play", description="play") # 재생
    async def play(self, interaction: nextcord.Interaction, msg: Optional[str] = nextcord.SlashOption(required=True, description="노래 URL")):
        """재생 명령어 입니다 | .env파일에 설정한 접두사 + play <Song>로 사용이 가능하고, 단축어로 p, 재생으로 사용가능"""
        if msg is None:
            await interaction.response.send_message('/play <song>')
            return

        # 사용자가 채널접속 여부
        try:
            check_user_join_vcChannel = interaction.user.voice.channel.id
        except:
            await interaction.response.send_message('이 명령어를 사용하려면 음성 채널에 있어야 합니다.')
            return

        # 음성 채널 입장
        try:
            vc[interaction.guild.id] = await interaction.user.voice.channel.connect()
            # await interaction.send(f'Joined {interaction.user.voice.channel.mention}')
        except:
            try:
                pass
            except:
                await interaction.response.send_message("먼저 음성채널에 참가해주세요!")
                return

        # 봇과 같은 채널에 접속 해야만 명령어 사용 가능
        if check_user_join_vcChannel != vc[interaction.guild.id].channel.id:
            await interaction.response.send_message('봇과 같은 채널에 접속해 주세요!')
            return

        # 노래가 재생중이 아니라면
        if not vc[interaction.guild.id].is_playing(): 

            scmsg = await interaction.response.send_message(embed = nextcord.Embed(title= "🔍 검색중", description = f'**`{msg}`** 검색중..', color=0xFFFFFF))

            try:
                title, url, image, cname  = videoSearch(msg)
            except:
                await scmsg.edit(embed = nextcord.Embed(title= "검색 실패", description = f'**`{msg}`**에 대한 음악을 찾지 못했어요! \:(', color=0xF04747))
                return None

            # 리스트 초기화
            reset(interaction.guild.id)

            # YDL URL 생성 
            """대기열을 만들때 미리 다 해두는 것보단, 임시 URL이라 6시간 이내 사용이 불가능 하기 때문에 대기열을 만들때는 재생될 때 마다 생성하는게 좋음 :)"""
            URL = ydl_url(url)

            np.update({interaction.guild.id:{
                        "title": title,
                        "url": url,
                        "image": image,
                        "cname": cname
                    }
                }
            )

            vc[interaction.guild.id].play(FFmpegOpusAudio(URL, **FFMPEG_OPTIONS, bitrate=512), after = lambda e: next_play(self, interaction))

            embed = nextcord.Embed(title = ' ', description = f'[{title}](<{url}>)', color=0x2F3136, timestamp=datetime.datetime.now(pytz.timezone('UTC')))
            embed.set_author(name=cname, url=url, icon_url=self.client.user.avatar.url)
            embed.set_thumbnail(url=image)
            embed.set_footer(text=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            await scmsg.edit(embed = embed) # 재생 시작 알림 전송

        else:
            scmsg = await interaction.response.send_message(embed = nextcord.Embed(title= "🔍 검색중", description = f'**`{msg}`** 검색중..', color=0xFFFFFF))

            try:
                title, url, image, cname  = videoSearch(msg)
            except:
                await scmsg.edit(embed = nextcord.Embed(title= "검색 실패", description = f'**`{msg}`**에 대한 음악을 찾지 못했어요! \:(', color=0xF04747))
                return None
            
            key = queue.get(interaction.guild.id)

            if key is None or len(queue[interaction.guild.id]['title']) == 0:
                queue.update({interaction.guild.id:{
                            "title": [title],
                            "url": [url],
                            "image": [image],
                            "cname": [cname]
                        }
                    }
                )

            else:
                queue[interaction.guild.id]['title'].append(title)
                queue[interaction.guild.id]['url'].append(url)
                queue[interaction.guild.id]['image'].append(image)
                queue[interaction.guild.id]['cname'].append(cname)

            embed = nextcord.Embed(description= f'Queued [{title}](<{url}>)') # Embed 선언
            await scmsg.edit(embed = embed) # 전송




    @nextcord.slash_command(name="skip", description="skip")
    async def skip(self, interaction: nextcord.Interaction):
        if not vc[interaction.guild.id].is_playing():
            await interaction.response.send_message("재생중인 노래가 없습니다.")

        else:
            embed = nextcord.Embed(title= f'⏭️ Skip Song', description = f'[{np[interaction.guild.id]["title"]}](<{np[interaction.guild.id]["url"]}>)', timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x8e8e8e)
            embed.set_thumbnail(url=np[interaction.guild.id]["image"])
            embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed = embed)
            vc[interaction.guild.id].stop()


    @nextcord.slash_command(name="stop", description="stop")
    async def stop(self, interaction: nextcord.Interaction):
        if vc[interaction.guild.id].is_playing():
            vc[interaction.guild.id].pause()
            await interaction.response.send_message(embed = nextcord.Embed(title= "⏸️ Stop", description = f'[{np[interaction.guild.id]["title"]}](<{np[interaction.guild.id]["url"]}>)', color = 0xff6464))

        else:
            await interaction.response.send_message("재생중인 노래가 없습니다.")


    @commands.command(name='resume', aliases=['r', '재개', '다시재생'])
    async def resume(self, interaction: nextcord.Interaction):
        try:
            vc[interaction.guild.id].resume()
        except:
            await interaction.response.send_message("재생중인 노래가 없습니다.")
        else:
            await interaction.response.send_message(embed = nextcord.Embed(title= "⏯️ Replay", description = f'[{np[interaction.guild.id]["title"]}](<{np[interaction.guild.id]["url"]}>)', color = 0x64ff68))

def setup(client):
    client.add_cog(music(client))
