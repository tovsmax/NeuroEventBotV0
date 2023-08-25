import discord
from discord import ui
from discord import SelectOption
from discord.ext.commands import Context
from discord import User, Message
from classes.NeuroEventBot import NeuroEventBot
from classes.Texts import Texts
from classes.VoteList import ListCategory
from typing import Optional

class VoteListDropdown(ui.Select):
    rank: int
    
    def __init__(self, rank: int, list_items: list[str]):
        self.rank = rank
        
        options = []
        for art_title in list_items:
            option = SelectOption(label=art_title)
            options.append(option)
                
        super().__init__(
            placeholder=f'{Texts.VOTING_TITLE_PLACEHOLDER.format(str(rank))}',
            options=options,
        )
    
    async def callback(self, interaction: discord.Interaction):
        art_title = self.values[0]
        self.view.top_list[self.rank] = art_title
        self.chosen_art = art_title
        
        await interaction.response.defer()


class VoteListView(ui.View):
    top_list: dict[int, Optional[str]]
    list_items: list[str]
    
    def __init__(self, list_items: list[str], NEB: NeuroEventBot, category: ListCategory):
        super().__init__()
        
        self.NEB = NEB
        self.category = category
        self.list_items = list_items
        
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
    async def submit_button(self, interaction: discord.Interaction, btn: discord.ui.Button):
        send = interaction.response.send_message
        top_items = list(self.top_list.values())
                
        if None in top_items:
            await send(Texts.VOTING_EMPTY_RANK)
            return

        if len(set(top_items)) != len(top_items):
            await send(Texts.VOTING_MULTIPLE_RANK)
            return
        
        cur_user_id = interaction.user.id
        cur_cat = self.category
        self.NEB.top_lists[cur_user_id][cur_cat] = top_items
        
        if cur_cat == ListCategory.AESTHETICS:
            await send(
                Texts.VOTING_EXTRA.format(Texts.VOTING_DEGENERATENESS),
                view=VoteListView(self.list_items, self.NEB, ListCategory.DEGENERATENESS)
            )
        elif cur_cat == ListCategory.DEGENERATENESS:
            await send(
                Texts.VOTING_EXTRA.format(Texts.VOTING_DANKNESS),
                view=VoteListView(self.list_items, self.NEB, ListCategory.DANKNESS)
            )
        else:
            await send(Texts.VOTING_REPLY)
        
        self.stop()


class Voting:
    def __init__(self, NEB: NeuroEventBot) -> None:
        self.NEB = NEB
    
    async def _send_list(self, voter: User, list_items: list[str]):
        self.NEB.top_lists[voter.id] = {
            ListCategory.AESTHETICS: {},
            ListCategory.DEGENERATENESS: {},
            ListCategory.DANKNESS: {}
        }
        
        await voter.send(
            Texts.VOTING_LIST_BEFORE_TEXT.format(Texts.VOTING_AESTHETICS),
            view=VoteListView(list_items, self.NEB, ListCategory.AESTHETICS)
        )
    
    async def send_lists_to_spectators(self, ctx: Context):
        spectators = await self.NEB.get_spectators(ctx)
        
        HUMANS_START_IND = 1
        for spectator in spectators[HUMANS_START_IND:]:
            list_items = list(self.NEB.art_dict.values())
            await self._send_list(spectator, list_items)
    
    
    async def send_lists_to_artists(self):
        artists = [self.NEB.get_user(artist_id) for artist_id in self.NEB.art_dict]
        
        for artist in artists:
            list_items = [
                art_title
                for artist_id, art_title in self.NEB.art_dict.items()
                if artist_id != artist.id
            ]
            
            await self._send_list(artist, list_items)
    
class Finishing:
    NEB: NeuroEventBot
    
    def __init__(self, NEB: NeuroEventBot) -> None:
        self.NEB = NEB
    
    @staticmethod
    def _make_scores(
        top_lists: dict[int, dict[ListCategory, dict[int, str]]]
    ) -> dict[str, dict[str, int]]:
        
        scores = {
            'Эстетичность': {},
            'Культурность': {},
            'Всратость': {},
            'Общий': {},
        }
        
        list_category_to_str = {
            ListCategory.AESTHETICS: 'Эстетичность',
            ListCategory.DEGENERATENESS: 'Культурность',
            ListCategory.DANKNESS: 'Всратость',
        }
        
        for categorized_top_list in top_lists.values():
            for category, top_list in categorized_top_list.items():
                category_name = list_category_to_str[category]
                for rank, art_title in top_list.items():
                    category_score = scores[category_name].get(art_title, 0)
                    scores[category_name][art_title] = category_score + (5 - rank)
                    
                    total_score = scores['Общий'].get(art_title, 0)
                    scores['Общий'][art_title] = total_score + (5 - rank)
        
        return scores
    
    @staticmethod
    def _make_output(scores: dict[str, dict[str, int]]) -> str:
        sort_by_score = lambda x: -x[1]
        voting_results = []
        for score_category, scored_arts in scores.items():            
            sorted_score = sorted(scored_arts.items(), key=sort_by_score)
            
            voting_result = '\n'.join(
                [f'**{score_category}:**']
                + [
                    f'{ind+1}) {art_title}: {art_score}'
                    for ind, (art_title, art_score) in enumerate(sorted_score)
                ]
            )
            
            voting_results.append(voting_result)
        
        output_result = '\n\n'.join(voting_results)
        return output_result
    
    def _make_voting_result(self, top_lists: dict[int, dict[ListCategory, dict[int, str]]]) -> str:
        scores = self._make_scores(top_lists)
        result = self._make_output(scores)
        return result
    
    def get_voting_result(self):
        top_lists = self.NEB.top_lists
        result = self._make_voting_result(top_lists)
        return result
        
        