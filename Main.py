from dotenv import dotenv_values
import discord, logging, os
from discord.ext import commands


config = dotenv_values(".env")
TOKEN = config['TOKEN']
PERFIX = config['PERFIX']

intentsa = discord.Intents().all()
client = commands.Bot(command_prefix= f"{PERFIX}", Intents=intentsa)


print('\033[93m-------------------------------------')

for filename in os.listdir("Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")

@client.event
async def on_ready():
    print('\033[93m-------------------------------------\u001b[37m')
    print("\033[95mSystem login SUCCESS")
    print('\u001b[37m')
    server_count = len(client.guilds)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{PERFIX}help | {server_count} Guilds'))

@client.event
async def on_command_error(ctx, error):
    logger.warning(f'\033[91m{error}\u001b[37m')


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s %(levelname)s] [%(name)s]: %(message)s', datefmt='%H:%M:%S')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

client.run(TOKEN)