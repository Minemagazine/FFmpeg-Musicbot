import discord
from discord import client, mentions, FFmpegAudio, voice_client, FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands, tasks
from discord.ext.commands.cooldowns import BucketType
from discord.utils import get

from youtube_dl import YoutubeDL

global vc
vc = { } # Voice Client



class music(commands.Cog):

    def __init__(self, client):
        self.client = client

        print(f'\033[96m Cogs Loading Success: Music\u001b[37m')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                try:
                    await vc[member.guild.id].disconnect()
                except:
                    pass
                return


    
    @commands.command(name='join', aliases=['j', '들어와', '접속'])
    @commands.cooldown(1, 2, commands.BucketType.user)
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
    @commands.cooldown(1, 2, commands.BucketType.user)
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




def setup(client):
    client.add_cog(music(client))
