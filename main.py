import discord
from classes.EventStage import EventStage
from classes.Configuration import Config
from classes.NeuroEventBot import NeuroEventBot
from classes.Texts import Texts
from classes.NeuroEventActions import Voting

if __name__ == '__main__':
    NEB = NeuroEventBot(intents=Config.intents)

    @NEB.hybrid_command()
    async def start(ctx):
        NEB.current_stage = EventStage.GATHERING_ART
        
        sended_msg = await ctx.send(Texts.START)
        sended_msg.add_reaction('👀')        
        NEB.spectators_msg_id = sended_msg.id

    @NEB.hybrid_command()
    async def voting(ctx):
        if NEB.current_stage != EventStage.GATHERING_ART:
            ctx.reply(Texts.VOTING_GATHERING_NOT_STARTED)
            return
        
        voting = Voting(NEB)
        
        await voting.send_lists_to_spectators(ctx)
        await voting.send_lists_to_artists()
        await voting.send_lists_to_organizers()
        

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
        
        if NEB.current_stage == EventStage.GATHERING_ART:
            artist_id = msg.author.id
            art_title = msg.content
            
            NEB.art_dict[artist_id] = art_title
            
    NEB.run(Config.token)

