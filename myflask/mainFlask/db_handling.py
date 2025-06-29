from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from sqlalchemy import text
from classes.author import Author
from classes.chat import Chat
from classes.message import Message

# region GET

def get_all_authors(db: SQLAlchemy, app: Flask):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM author"))
        authors = []
        for row in result:
            loaded_author = _convert_db_row_to_author(row)
            loaded_author.chat_ids = _get_chat_ids_from_author(db, app, loaded_author.id) #TODO: maybe create DB view with ids in it
            authors.append(loaded_author)
        return authors
    
def _get_chat_ids_from_author(db: SQLAlchemy, app: Flask, author_id: int):
        with app.app_context():
            chat_ids = []
            result = db.session.execute(text("SELECT * FROM chat_participants WHERE author_id = :id"), {'id': author_id})
            for row in result:
                loaded_chat_id = row[0]
                chat_ids.append(loaded_chat_id)
            return chat_ids

    
def get_author_by_id(db: SQLAlchemy, app: Flask, id: int):
    with app.app_context():
        result_row = db.session.execute(
            text("SELECT * FROM author WHERE id = :id"),
            {'id': id}
        ).fetchone()

        loaded_author = _convert_db_row_to_author(result_row)
        return loaded_author

def get_participants_from_chat(db: SQLAlchemy, app: Flask, chat: Chat):
    with app.app_context():
        participants = []
        result = db.session.execute(text("SELECT author_id FROM chat_participants WHERE chat_id = :id"), {'id': chat.chat_id})
        participant_ids = [row[0] for row in result]
        for p_id in participant_ids:
            loaded_author = get_author_by_id(db, app, p_id)
            participants.append(loaded_author)

        return participants

def get_messages_from_chat(db: SQLAlchemy, app: Flask, chat: Chat):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM message where chat_id = :id"), {'id': chat.chat_id})
        for row in result:
            loaded_message = _convert_db_row_to_message(row, db, app)
            loaded_message.chat = chat
            chat.add_message(loaded_message)

def get_chat_by_id(db: SQLAlchemy, app: Flask, chat_id: int):
    with app.app_context():
        print("Wie oft bin ihc hier?")
        result = db.session.execute(text("SELECT * FROM message where chat_id = :id"), {'id': chat_id})
        chat = Chat(chat_id)
        for row in result:
            loaded_message = _convert_db_row_to_message(row, db, app)
            loaded_message.chat = chat
            chat.add_message(loaded_message)

        return chat

def get_all_messages(db: SQLAlchemy, app: Flask):
    with app.app_context():
        messages = []
        result = db.session.execute(text("SELECT * FROM message"))
        for row in result:
            loaded_message = _convert_db_row_to_message(row, db, app)
            messages.append(loaded_message)

    return messages

def get_message_by_id(db: SQLAlchemy, app: Flask, id: int):
    with app.app_context():
        result_row = db.session.execute(
            text("SELECT * FROM message WHERE id = :id"),
            {'id': id}
        ).fetchone()

        loaded_message = _convert_db_row_to_message(result_row)
        return loaded_message
        
        #TODO: only load stuff that is not available

# endregion

#region Conversion

def _convert_db_row_to_message(row, db: SQLAlchemy, app: Flask):
            message_id = row[0]
            chat_id = row[1]
            sender_id = row[2]
            sender = get_author_by_id(db, app, sender_id)
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