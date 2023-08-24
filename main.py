import discord
from discord.ext.commands import Context
from classes.EventStage import EventStage
from classes.Configuration import Config
from classes.NeuroEventBot import NeuroEventBot
from classes.Texts import Texts
from classes.NeuroEventActions import Voting, Finishing

if __name__ == '__main__':
    NEB = NeuroEventBot(intents=Config.intents)

    @NEB.hybrid_command()
    async def start(ctx: Context):
        NEB.current_stage = EventStage.GATHERING_ART
        
        sended_msg = await ctx.send(Texts.START)
        SPECTATOR_EMOJI = '👀'
        await sended_msg.add_reaction(SPECTATOR_EMOJI)
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
        await ctx.reply(NEB.top_lists)


    @NEB.command()
    async def show_id(ctx):
        await ctx.reply('Зырь в консоль.')
        
        print(f'{ctx.author}: {ctx.author.id}')

    @NEB.event
    async def on_message(msg: discord.Message):
        if msg.author == NEB.user:
            return
        
        if msg.content.startswith(Texts.PREFIX):
            await NEB.process_commands(msg)
            return
                
        if NEB.current_stage == EventStage.GATHERING_ART and msg.guild is None:
            if msg.attachments == []:
                await msg.reply('❌ There is no art in message')
                return
            
            artist_id = msg.author.id
            art_title = msg.content
            
            NEB.art_dict[artist_id] = art_title
            return
    
    @NEB.hybrid_command()
    async def order_arts(ctx: Context, artists: str):
        user = NEB.get_user(ctx.message.author.id)
        await ctx.reply(user.display_name)
        return
    
    @NEB.hybrid_command()
    async def test_voting(ctx: Context):
        voting = Voting(NEB)
        
        list_items = [
            'olol',
            'kek',
            'lolec',
            'cheburek',
            'lel'
        ]
        
        await voting.send_lists_to_artists(ctx)
        
    async def test_finish(ctx: Context):
        Finishing(NEB)
        pass
            
    NEB.run(Config.token)

