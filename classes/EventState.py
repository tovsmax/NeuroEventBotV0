import enum

class EventStatus(enum.Enum):
    NOT_STARTED = 0
    GATHERING_ART = 1
    VOTING = 2
    COMPLETED_VOTING = 3
    GAME_ENDED = 4
    
class EventState:
    def __init__(self) -> None:
        self.current = EventStatus.NOT_STARTED
        self.art_dict = {}