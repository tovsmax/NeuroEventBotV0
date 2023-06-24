from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from classes.EventState import EventStatus, EventState

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True

bot = commands.Bot(command_prefix='!ne ', intents=intents)

state = EventState()

@bot.event
async def on_ready():
    await bot.tree.sync()    


@bot.hybrid_command()
async def start(ctx):
    await ctx.send('Нейроивент начинается! Участники, скидывайте сгенеренные арты. Если Вы хотите просто проголосовать, то ставьте эмодзи 👀, чтобы стать зрителем.')
    
    state.current = EventStatus.GATHERING_ART
    
@bot.hybrid_command()
async def voting(ctx):
    pass
    

@bot.hybrid_command()
async def finish(ctx):
    pass

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    
    if state.current == EventStatus.GATHERING_ART:
        artist_id = msg.author.id
        art_title = msg.content
        
        state.art_dict[artist_id] = art_title


bot.run(TOKEN)