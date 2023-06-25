import discord
from discord.ext import commands
from classes.EventState import EventStage, EventState
from classes.Configuration import Config
from classes import Texts

class NeuroEventBot(commands.Bot):
    def __init__(self, **args):
        super().__init__(command_prefix=Texts.PREFIX, **args)
        self.state = EventState()        
        
    async def setup_hook(self):
        await self.tree.sync()

if __name__ == '__main__':
    NEB = NeuroEventBot(intents=Config.intents)

    @NEB.hybrid_command()
    async def start(ctx):
        await ctx.send(Texts.START)
        
        NEB.state.current = EventStage.GATHERING_ART


    @NEB.hybrid_command()
    async def voting(ctx):
        pass
        

    @NEB.hybrid_command()
    async def finish(ctx):
        pass


    @NEB.command()
    async def show_id(ctx):
        await ctx.reply('Зырь в консоль.')
        
        print(f'{ctx.author}: {ctx.author.id}')


    @NEB.event
    async def on_message(msg):
        await NEB.process_commands(msg)
        
        if msg.author == NEB.user:
            return
        
        if NEB.state.current == EventStage.GATHERING_ART:
            artist_id = msg.author.id
            art_title = msg.content
            
            NEB.state.art_dict[artist_id] = art_title
            
    NEB.run(Config.token)

