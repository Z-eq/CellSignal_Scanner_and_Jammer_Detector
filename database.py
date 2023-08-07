from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URI = 'sqlite:///wifis.db'  # Replace with the path to your SQLite database
engine = create_engine(DATABASE_URI)

# Initialize a session using the scoped sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

