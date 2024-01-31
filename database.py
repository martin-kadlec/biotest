from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import os

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'database.db'))

def init_db():
    import models
    models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()