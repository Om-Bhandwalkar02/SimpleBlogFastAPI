from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the SQLite URL for the database
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.sqlite"

# Create an engine to interact with the SQLite database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for the models
Base = declarative_base()

