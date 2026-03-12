from pathlib import Path
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

db_path = Path(__file__).parent.parent

sqlite_file_name = "records.db"

sqlite_url = f"sqlite:///{db_path/sqlite_file_name}"

connect_args = {"check_same_thread" : False}

engine = create_engine(sqlite_url, connect_args = connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]