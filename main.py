from discord.ext.commands import Context
from classes.Configuration import Config, Organizers
from classes.NeuroEventBot import NeuroEventBot
from classes.Texts import Texts
from classes.NeuroEventActions import Voting, Finishing
import re

if __name__ == '__main__':
    NEB = NeuroEventBot(intents=Config.intents)

    @NEB.hybrid_command()
    async def send_lists(ctx: Context, artists_and_arts: str, spectators: str = ''):
        if not Organizers().is_organizer(ctx.author.id):
            await ctx.reply(Texts.VOTING_NOT_ORGANIZER)
            return
                
        for artist_and_art in artists_and_arts.split(','):
            pattern = r'^<@(\d+)>:(.*)$'
            artist_id, art_title = re.findall(pattern, artist_and_art)[0]
            
            NEB.art_dict[int(artist_id)] = art_title
        
        spectator_pattern = '<@(\d+)>'
        spectator_strs = re.findall(spectator_pattern, spectators)
        
        spectator_list = [
            int(spectator_str)
            for spectator_str in spectator_strs
        ]
        
        voting = Voting(NEB)
        
        await voting.send_lists_to_artists()
        await voting.send_lists_to_spectators(spectator_list)
        
        await ctx.reply(Texts.VOTING_STARTED)
        
    @NEB.hybrid_command()
    async def get_total_scores(ctx: Context):
        pass
            
    NEB.run(Config.token)

