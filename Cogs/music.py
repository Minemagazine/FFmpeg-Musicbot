import discord, datetime, pytz, youtubesearchpython 
from discord import client, FFmpegPCMAudio
from discord.ext import commands
from youtube_dl import YoutubeDL
from dotenv import dotenv_values
config = dotenv_values(".env")
PREFIX = config['PREFIX']
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} # FFmpeg 옵션
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'} # YouTube DL 옵션

global vc
vc = { } # Voice Client

global np
np = { } # 현재 재생중인 곡의 정보를 담아둘 딕셔너리 자료

# np[123456789123] = {
#     "title": "영상 제목",
#     "url": "영상 주소",
#     "image": "썸네일 주소",
#     "cname": "채널 이름"
# } # 자동 생성될 예시 np[ctx.guild.id] 변수 ( 이건 지워도 됩니다. )

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



class music(commands.Cog):

    def __init__(self, client):
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

    @commands.command(name='join', aliases=['j', '들어와', '접속'])
    async def join(self, ctx):
        try:
            check_user_join_vcChannel = ctx.message.author.voice.channel.id
        except:
            await ctx.reply('이 명령어를 사용하려면 음성 채널에 있어야 합니다.', mention_author=False)
            return
            
        try:
            vc[ctx.guild.id] = await ctx.message.author.voice.channel.connect()

            await ctx.reply(f'Joined {ctx.message.author.voice.channel.mention}', mention_author=False)
        except:
            try:
                await ctx.message.author.voice.channel.connect().move_to(ctx.message.author.voice.channel.connect())
                await ctx.reply(f'Moved {ctx.message.author.voice.channel.mention}', mention_author=False)
            except:
                await ctx.reply('먼저 음성채널에 참가해주세요!', mention_author=False)
                return

    @commands.command(name='leave', aliases=['l', '나가', '퇴장'])
    async def leave(self, ctx):
        try:
            check_user_join_vcChannel = ctx.message.author.voice.channel.id
        except:
            await ctx.reply('이 명령어를 사용하려면 음성 채널에 있어야 합니다.', mention_author=False)
            return

        try:
            await vc[ctx.guild.id].disconnect()
            await ctx.send(f'Left {ctx.message.author.voice.channel.mention}', mention_author=False)

        except:
            await ctx.send('현재 접속중인 채널이 없어요!', mention_author=False)
            return
            
        if check_user_join_vcChannel != vc[ctx.guild.id].channel.id:
            await ctx.reply('봇과 같은 채널에 접속해 주세요!', mention_author=False)
            return

    @commands.command(name='play', aliases=['p', '재생'])
    async def leave(self, ctx, *, msg=None):
        """재생 명령어 입니다 | .env파일에 설정한 접두사 + play <Song>로 사용이 가능하고, 단축어로 p, 재생으로 사용가능"""
        if msg is None:
            await ctx.send(f'{PREFIX}play <song>')
            return

        # 사용자가 채널접속 여부
        try:
            check_user_join_vcChannel = ctx.message.author.voice.channel.id
        except:
            await ctx.reply('이 명령어를 사용하려면 음성 채널에 있어야 합니다.', mention_author=False)
            return

        # 음성 채널 입장
        try:
            vc[ctx.guild.id] = await ctx.message.author.voice.channel.connect()
            await ctx.send(f'Joined {ctx.message.author.voice.channel.mention}')
        except:
            try:
                vc[ctx.guild.id].move_to(ctx.message.author.voice.channel)
            except:
                await ctx.reply("먼저 음성채널에 참가해주세요!", mention_author=False)
                return

        # 봇과 같은 채널에 접속 해야만 명령어 사용 가능
        if check_user_join_vcChannel != vc[ctx.guild.id].channel.id:
            await ctx.reply('봇과 같은 채널에 접속해 주세요!', mention_author=False)
            return

        # 노래가 재생중이 아니라면
        if not vc[ctx.guild.id].is_playing(): 

            scmsg = await ctx.reply(embed = discord.Embed(title= "🔍 검색중", description = f'**`{msg}`** 검색중..', color=0xFFFFFF), mention_author=False)

            try:
                title, url, image, cname  = videoSearch(msg)
            except:
                await scmsg.edit(embed = discord.Embed(title= "검색 실패 <:failed1:912636274068832256>", description = f'**`{msg}`**에 대한 음악을 찾지 못했어요! \:(', color=0xF04747))
                return None

            # 리스트 초기화
            reset(ctx.guild.id)

            # YDL URL 생성 
            """대기열을 만들때 미리 다 해두는 것보단, 임시 URL이라 6시간 이내 사용이 불가능 하기 때문에 대기열을 만들때는 재생될 때 마다 생성하는게 좋음 :)"""
            URL = ydl_url(url)

            np.update({ctx.guild.id:{
                        "title": title,
                        "url": url,
                        "image": image,
                        "cname": cname
                    }
                }
            )

            vc[ctx.guild.id].play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

            embed = discord.Embed(title = ' ', description = f'[{title}](<{url}>)', color=0x2F3136, timestamp=datetime.datetime.now(pytz.timezone('UTC')))
            embed.set_author(name=cname, url=url, icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=image)
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await scmsg.edit(embed = embed) # 재생 시작 알림 전송

        else:
            await ctx.send("곡이 이미 재생중 입니다.")


def setup(client):
    client.add_cog(music(client))
