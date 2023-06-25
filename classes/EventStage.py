import enum

class EventStage(enum.Enum):
    NOT_STARTED = 0
    GATHERING_ART = 1
    VOTING = 2
    COMPLETED_VOTING = 3
    GAME_ENDED = 4