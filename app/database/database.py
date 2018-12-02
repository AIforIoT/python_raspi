from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#TODO: CHANGE DB PATH TO A RELATIVE ONE
engine = create_engine('sqlite:////home/celiasantos/celia/db_IoT/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import app.database.models
    Base.metadata.create_all(bind=engine)

