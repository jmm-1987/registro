from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///database/registro.db',
connect_args={'check_same_thread': False})

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()