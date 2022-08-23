import logging, os
# NEXTCORD
import nextcord
from nextcord.ext import commands, application_checks

PREFIX = str("음악!")
OWNER_ID = int("971981029206274079")
TOKEN = str("your bot token")

bot = commands.Bot(command_prefix=PREFIX, help_command=None, owner_id=OWNER_ID)

def load_cogs(bot):
    extensions = []
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extensions.append(file.split('.')[0])
    failed = []
    for extension in extensions:
        try:
            bot.load_extension(f"cogs.{extension}")
        except Exception as e:
            print(f"{e.__class__.__name__}: {str(e)}")
            failed.append(extension)
    if failed:
         print("failed")
    return failed

def unload_cogs(bot):
    extensions = []
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extensions.append(file.split('.')[0])
    failed = []
    for extension in extensions:
        try:
            bot.unload_extension(f"cogs.{extension}")
        except Exception as e:
            print(f"{e.__class__.__name__}: {str(e)}")
            failed.append(extension)
    if failed:
         print("failed")
    return failed

@bot.event
async def on_ready():
    print('\033[93m-------------------------------------\u001b[37m')
    print("\033[95mSystem login SUCCESS\u001b[37m")
    print('\033[93m-------------------------------------\u001b[37m')
    guild_list = (bot.guilds)
    for i in guild_list:
        print("서버 ID: {} / 서버 이름: {}".format(i.id, i.name))
    server_count = len(bot.guilds)
    await bot.change_presence(status=nextcord.Status.online, activity=nextcord.Game(f'내기!help | {server_count} 서버에서 내기 심판중'))

@bot.event
async def on_command_error(ctx,error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("명령어를 찾지 못했습니다")

@bot.slash_command(name="update", description="업데이트 명령어")
@application_checks.is_owner()
async def reload(interaction: nextcord.Interaction):
    await interaction.response.send_message('완료!')
    unload_cogs(bot)
    load_cogs(bot)

@bot.slash_command(name="cache ", description="캐시삭제 명령어")
@application_checks.is_owner()
async def reload(interaction: nextcord.Interaction):
    await interaction.response.send_message('완료!')
    os.system(r"""find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf""")
    os.system(r"""youtube-dl --rm-cache-dir""")

@bot.slash_command(name="ping", description="pong")
async def ping(interaction: nextcord.Interaction):
    await interaction.response.send_message(f'pong! :ping_pong: {round(bot.latency*1000)}ms')

# 로깅 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s %(levelname)s] [%(name)s]: %(message)s', datefmt='%H:%M:%S')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# 로깅 설정 끝

if __name__ == '__main__':
    load_cogs(bot)
    bot.run(TOKEN)
