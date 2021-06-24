from app.crud.types import NoteType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import Boolean, Enum


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    username = Column(String(30), unique=True, index=True)
    hashed_password = Column(String(64), nullable=False)
    salt = Column(String(32), nullable=False)


class Folder(Base):
    __tablename__ = "folder"
    __table_args__ = (UniqueConstraint("user_id", "name", name="unique_user_id_name"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String(30), nullable=False)


class Note(Base):
    __tablename__ = "note"
    __table_args__ = (UniqueConstraint("folder_id", "name", name="unique_folder_id_name"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    folder_id = Column(Integer, ForeignKey("folder.id"))
    name = Column(String(30), nullable=False)
    shared = Column(Boolean, nullable=False)
    type = Column(Enum(NoteType), nullable=False)
    text_body = Column(String(), nullable=False)


class ListDbModel(Base):
    __tablename__ = "list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    note_id = Column(Integer, ForeignKey("note.id"))
    text_body = Column(String(), nullable=False)
