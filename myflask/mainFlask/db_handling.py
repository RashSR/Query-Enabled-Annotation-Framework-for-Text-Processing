from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from sqlalchemy import text
from classes.author import Author
from classes.chat import Chat
from classes.message import Message

# region GET

def get_all_messages(db: SQLAlchemy, app: Flask):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM message"))
        
    return None


def get_all_authors(db: SQLAlchemy, app: Flask, shouldLoadMessages: bool = False):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM author"))
        authors = []
        for row in result:
            loaded_author = _convert_db_row_to_author(row)
            _get_chats_from_author(db, app, loaded_author, shouldLoadMessages)
            authors.append(loaded_author)
        return authors

def _get_chats_from_author(db: SQLAlchemy, app: Flask, author: Author, shouldLoadMessages: bool = False):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM chat_participants WHERE author_id = :id"), {'id': author.author_id})
        for row in result:
            chat_id = row[0]
            loaded_chat = Chat(chat_id)
            if shouldLoadMessages:
                _get_messages_from_chat(db, app, loaded_chat)
            author.add_chat(loaded_chat)

def _get_messages_from_chat(db: SQLAlchemy, app: Flask, chat: Chat):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM message where chat_id = :id"), {'id': chat.chat_id})
        for row in result:
            loaded_message = _convert_db_row_to_message(row, db, app)
            loaded_message.chat = chat
            chat.add_message(loaded_message)
        
        #TODO: only load stuff that is not available

def _get_author_with_id(db: SQLAlchemy, app: Flask, id: int):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM author WHERE id = :id"), {'id': id})
        for row in result:
            return _convert_db_row_to_author(row)

# endregion

#region Conversion

def _convert_db_row_to_message(row, db: SQLAlchemy, app: Flask):
            message_id = row[0]
            chat_id = row[1]
            sender_id = row[2]
            sender = _get_author_with_id(db, app, sender_id)
            timestamp = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S") 
            content = row[4] #TODO: add check for row name maybe?
            annotated_text = row[7]
            loaded_message = Message(chat_id=chat_id, message_id=message_id, sender=sender, timestamp=timestamp, content=content, annotated_text=annotated_text)
            return loaded_message

def _convert_db_row_to_author(row):
    author_id = row[0]
    name = row[1]
    age = row[2]
    gender = row[3]
    first_language = row[4]
    languages = [lang.strip() for lang in row[5].split(',')] #at this time the languages are stored in the DB like 'Language1, Language2, ...'
    region = row[6]
    job = row[7]
    loaded_author = Author(author_id, name, age, gender, first_language, languages, region, job)
    return loaded_author

# endregion