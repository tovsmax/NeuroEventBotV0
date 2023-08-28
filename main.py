from discord.ext.commands import Context
from classes.Configuration import Config, Organizers
from classes.NeuroEventBot import NeuroEventBot
from classes.Texts import Texts
from classes.NeuroEventActions import Voting, Finishing
import re

if __name__ == '__main__':
    NEB = NeuroEventBot(intents=Config.intents)

    @NEB.hybrid_command()
    async def send_lists(ctx: Context, vote_items: str, artists: str, spectators: str = ''):
        if not Organizers().is_organizer(ctx.author.id):
            await ctx.reply(Texts.VOTING_NOT_ORGANIZER)
            return
        
        voters_pattern = '<@(\d+)>'
        artist_list = re.findall(voters_pattern, artists)
        spectator_list = re.findall(voters_pattern, spectators)
        
        ptrn_title_with_quotes = r'"([^"]*)",?'
        ptrn_coma_separated_title = r'(.+?),'
        ptrn_last_title = r'(.+?)$'
        arts_pattern = f'{ptrn_title_with_quotes}|{ptrn_coma_separated_title}|{ptrn_last_title}'
        vote_item_list = re.findall(arts_pattern, vote_items)
        
        voting = Voting(NEB)
        
        await voting.send_lists_to_artists()
        await voting.send_lists_to_spectators()            
        
        await ctx.reply(Texts.VOTING_STARTED)
        
    @NEB.hybrid_command()
    async def get_total_scores(ctx: Context):
        pass
            
    NEB.run(Config.token)

