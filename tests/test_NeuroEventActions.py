import unittest
from classes.NeuroEventActions import Finishing
from classes.NeuroEventBot import NeuroEventBot
from classes.Configuration import Config
from classes.VoteList import ListCategory

class TestNeuroEventActions(unittest.TestCase):
    def setUp(self):
        NEB = NeuroEventBot(intents=Config.intents)
        
        self.finishing = Finishing(NEB)

    @staticmethod
    def _create_top_list() -> dict[int, str]:
        top_list = {
            1: 'EBONYA',
            2: 'Путь я щастью превозмогая боль и трудности',
            3: 'Слиза',
            4: 'Зато не подмышки',
        }
        return top_list

    def test_get_voting_result(self):        
        self.finishing.get_voting_result()
        
if __name__ == '__main__':
    unittest.main()
