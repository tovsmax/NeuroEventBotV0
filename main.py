import discord
from discord.ext.commands import Context
from classes.EventStage import EventStage
from classes.Configuration import Config
from classes.NeuroEventBot import NeuroEventBot
from classes.Texts import Texts
from classes.NeuroEventActions import Voting

if __name__ == '__main__':
    NEB = NeuroEventBot(intents=Config.intents)

    @NEB.hybrid_command()
    async def start(ctx: Context):
        NEB.current_stage = EventStage.GATHERING_ART
        
        sended_msg = await ctx.send(Texts.START)
        await sended_msg.add_reaction('👀')
        NEB.spectators_msg_id = sended_msg.id

    @NEB.hybrid_command()
    async def voting(ctx: Context):
        if NEB.current_stage != EventStage.GATHERING_ART:
            await ctx.reply(Texts.VOTING_GATHERING_NOT_STARTED)
            return
                
        voting = Voting(NEB)
        
        await voting.send_lists_to_spectators(ctx)
        # await voting.send_lists_to_artists()
        # await voting.send_lists_to_organizers()
        
        await ctx.reply(Texts.VOTING_STARTED)

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
        
        # TODO: Здесь нужно посмотреть, не идёт дальше код при срабатывании команды
        
        if msg.author == NEB.user:
            return
        
        if NEB.current_stage == EventStage.GATHERING_ART:
            artist_id = msg.author.id
            art_title = msg.content
            
            NEB.art_dict[artist_id] = art_title
            
    @NEB.hybrid_command()
    async def test(ctx: Context):
        voting = Voting(NEB)
        
        await voting._send_list(ctx.author, ['kek'])
            
    NEB.run(Config.token)

