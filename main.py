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
                
        for artist_and_art in artists_and_arts.split(', '):
            pattern = r'^<@(\d+)> (.*)$'
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
    async def get_total_scores(ctx: Context, force_finish = False):
        if not Organizers().is_organizer(ctx.author.id):
            await ctx.reply(Texts.VOTING_NOT_ORGANIZER)
            return
        
        if not force_finish:
            unvoted_list = []
            top_lists = NEB.top_lists
            for voter_id, categorized_top_list in top_lists.items():
                #TODO: Возможно стоит удалить
                if {} in categorized_top_list.values():
                    unvoted_list.append(voter_id)
                    
            if unvoted_list != []:
                voter_strs = [f'<@{voter_id}>' for voter_id in unvoted_list]
                unvoted_str = '\n'.join(voter_strs)
                await ctx.reply(Texts.FINISH_NOT_ALL_VOTED.format(unvoted_str))
                return
        
        finish = Finishing(NEB)
        result = finish.get_voting_result()
        
        await ctx.reply(result)
            
    NEB.run(Config.token)
