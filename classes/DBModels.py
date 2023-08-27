from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.sql import func
from classes.EventStage import EventStage

class Base(DeclarativeBase):
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        fields = ','.join([
            f'{field}={value}'
            for field, value in self.__dict__.items()
            if not field.startswith('_')
        ])
        
        return f"<{class_name}({fields})>"

class EventSession(Base):
    __tablename__ = 'EventSessions'
    # autoincrement=True
    id = Column(Integer, primary_key=True, index=True)
    current_stage = Column(Enum(EventStage), default=EventStage.NOT_STARTED)
    start_datetime = Column(DateTime(timezone=True), server_default=func.now())
    update_datetime = Column(DateTime(timezone=True), onupdate=func.now())
    end_datetime = Column(DateTime(timezone=True))
    
    __table_args__ = (
        CheckConstraint('end_datetime >= start_datetime'),
    )
    
class User(Base):
    __tablename__ = 'Users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, nullable=False)
    
# class Art(Base):
#     __tablename__ = 'Arts'
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     image_url = Column(String, nullable=False)

class Art(Base):
    __tablename__ = 'Arts'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

class RankedArt(Base):
    __tablename__ = 'RankedArts'
    
    id = Column(Integer, primary_key=True, index=True)
    rank = Column(Integer)
    art_id = Column(ForeignKey('Arts.id', ondelete='CASCADE'), nullable=False, index=True)
    voter_id = Column(ForeignKey('Users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    
    __table_args__ = (
        CheckConstraint('rank > 0'),
    )

class RankedArtData(RankedArt):
    pass
    # title = 
    # voter = 