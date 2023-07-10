import discord
from discord import ui
from discord import SelectOption
from discord.ext.commands import Context
from discord import User
from classes.NeuroEventBot import NeuroEventBot
from classes.Texts import Texts
from classes.VoteList import ListCategory

class VoteListDropdown(ui.Select):
    def __init__(self, rank, list_items):
        self.rank = rank
        
        options = []
        for art_title in list_items:
            option = SelectOption(label=art_title)
            options.append(option)
        
        super().__init__(
            placeholder=f'{Texts.VOTING_TITLE_PLACEHOLDER.format(str(rank))}',
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        self.view.top_list[self.rank] = self.values[0]
        
        await interaction.response.defer()


class VoteListView(ui.View):
    def __init__(self, list_items, NEB: NeuroEventBot):
        super().__init__()
        
        self.NEB = NEB
        
        PREMAX_ROW_COUNT = 4
        item_count = len(list_items)
        last_rank_ind = item_count \
            if item_count <= PREMAX_ROW_COUNT \
            else PREMAX_ROW_COUNT
            
        self.top_list = {}
        for rank in range(1, last_rank_ind+1):
            self.add_item(VoteListDropdown(rank, list_items))
            self.top_list[rank] = None
    
    @discord.ui.button(
        label=Texts.VOTING_BUTTON_LABEL,
        style=discord.ButtonStyle.primary,
        row=4
    )
    async def submit_button(self, interaction: discord.Interaction, btn):
        send = interaction.response.send_message        
        top_items = self.top_list.values()
                
        if None in top_items:
            await send(Texts.VOTING_EMPTY_RANK)
            return

        if len(set(top_items)) != len(top_items):
            await send(Texts.VOTING_MULTIPLE_RANK)
            return
        
        if  ListCategory

        await send(Texts.VOTING_REPLY)
        
        cur_category = 'test'
        self.NEB.art_top[cur_category] = top_items
        
        self.stop()


class Voting:
    def __init__(self, NEB: NeuroEventBot) -> None:
        self.NEB = NEB
    
    async def _send_list(self, voter: User, list_items: list[str]):        
        await voter.send(
            Texts.VOTING_LIST_BEFORE_TEXT.format(),
            view=VoteListView(list_items, self.NEB)
        )
    
    async def send_lists_to_spectators(self, ctx: Context):
        sm_id = self.NEB.spectators_msg_id
        if sm_id == None:
            raise ValueError('There is no msg id, where reactions can be obtained!')
        
        spectators_msg = await ctx.channel.fetch_message(sm_id)
        SPECTATOR_EMOJI_IND = 0
        spectators = spectators_msg.reactions[SPECTATOR_EMOJI_IND].users()
        spectators = [spectator async for spectator in spectators]
        
        HUMANS_START_IND = 1
        for spectator in spectators[HUMANS_START_IND:]:
            list_items = list(self.NEB.art_dict.values())
            await self._send_list(spectator, list_items)
    
    
    async def send_lists_to_artists(self):
        await self.NEB.fetch_user()
        for artist_id in self.NEB.state.art_dict:
            self.NEB.fetch_user()


    async def send_lists_to_organizers(self):
        pass