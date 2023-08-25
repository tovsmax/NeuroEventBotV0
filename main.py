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
        
        await voting.send_lists_to_artists()
        await voting.send_lists_to_spectators(ctx)
        
        await ctx.reply(Texts.VOTING_STARTED)

    @NEB.hybrid_command()
    async def finish(ctx: Context, force_finish: bool = False):
        artist_count = len(NEB.get_artists())
        spectator_count = len(await NEB.get_spectators())
        voter_count = artist_count + spectator_count
        
        voted_count = len(NEB.top_lists)
        if voted_count < voter_count and not force_finish:
            await ctx.reply(Texts.FINISH_NOT_ALL_VOTED.format(voted_count, voter_count))
            return
        
        finishing = Finishing(NEB)
        
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
                await msg.reply(Texts.GATHERING_ART_IS_NOT_ATTACHED)
                return
            
            if msg.content == '':
                await msg.reply(Texts.GATHERING_ART_TITLE_IS_NOT_PROVIDED)
                return
            
            artist_id = msg.author.id
            art_title = msg.content
            NEB.art_dict[artist_id] = art_title
            
            await msg.reply(Texts.GATHERING_ART_IS_ACCEPTED)
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
        
        voting.NEB.art_dict[ctx.author.id] = 'kek'
        
        await voting.send_lists_to_artists(ctx)
        
    async def test_finish(ctx: Context):
        Finishing(NEB)
        pass
            
    NEB.run(Config.token)

