from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


BaseEntity = declarative_base()

db_engine = create_engine('sqlite:///db.sqlite')

PsqlSession = sessionmaker(
    bind=db_engine, autoflush=True, autocommit=True,
)

session = PsqlSession()
