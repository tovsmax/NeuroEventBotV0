from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from classes.DBModels import Base, EventSession
import os

if os.environ is None or os.environ['DEBUG'] == 'False':
    debug = False
elif os.environ['DEBUG'] == 'True':
    debug = True
else:
    raise ValueError(f'Error env value: DEBUG={os.environ["DEBUG"]}')

DB_PATH = 'NEB.db' if debug else 'NEB_test.db'
DB_URL = f'sqlite:///{DB_PATH}'


class SQLiteClient:
    _engine = create_engine(DB_URL, echo=debug)

    session_id: int

    @classmethod
    def _create_all_tables(cls):
        Base.metadata.drop_all(cls._engine)
        Base.metadata.create_all(cls._engine)

    @classmethod
    def create_event_session(cls):
        with Session(cls._engine) as con:
            event_session = EventSession()
            con.add(event_session)
            con.commit()

            cls.session_id = event_session.id

    @classmethod
    def get_current_session(cls):
        query = (
            select(EventSession)
            .where(EventSession.id == cls.session_id)
        )

        with Session(cls._engine) as con:
            event_session = con.scalars(query).one()
            # con.scalar(query).id

        return event_session

    @classmethod
    def get_all_sessions(cls):
        query = (
            select(EventSession)
        )

        with Session(cls._engine) as con:
            event_sessions = con.scalars(query).fetchall()

        return event_sessions


if __name__ == '__main__':

    for record in SQLiteClient.get_all_sessions():
        print(record)
