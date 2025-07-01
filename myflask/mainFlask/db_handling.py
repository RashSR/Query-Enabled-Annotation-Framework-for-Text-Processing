from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from sqlalchemy import text
from classes.author import Author
from classes.chat import Chat
from classes.message import Message
from myflask.mainFlask.cachestore import CacheStore

# region GET

def get_all_authors(db: SQLAlchemy, app: Flask):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM author_with_chat_ids")) #specially created view with the chat_ids in it -> only one DB call needed
        authors = []
        for row in result:
            loaded_author = _convert_db_row_to_author(row)
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

def get_chat_by_ids(db: SQLAlchemy, app: Flask, ids: list[int]):
     with app.app_context():
        #TODO: make one command to get this
        #sql = text("SELECT * FROM chat WHERE id IN :ids") #for groupname
        #result = db.session.execute(sql, {'ids': tuple(ids)})
        chats = []
        for id in ids:
            chat = get_chat_by_id(db, app, id)
            chats.append(chat)
        
        return chats

def get_author_by_id(db: SQLAlchemy, app: Flask, id: int):
    with app.app_context():
        result_row = db.session.execute(
            text("SELECT * FROM author_with_chat_ids WHERE author_id = :id"),
            {'id': id}
        ).fetchone()

        loaded_author = _convert_db_row_to_author(result_row)
        loaded_author.chat_ids = _get_chat_ids_from_author(db, app, loaded_author.id)
        return loaded_author

def get_chat_by_id(db: SQLAlchemy, app: Flask, chat_id: int):
    with app.app_context():
        result_row = db.session.execute(
            text("SELECT * FROM chat WHERE id = :id"),
            {'id': chat_id}
        ).fetchone() #TODO reuse this syntax in a function?
        chat = _convert_db_row_to_chat(result_row)
        result = db.session.execute(text("SELECT * FROM message where chat_id = :id"), {'id': chat_id})
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

def _convert_db_row_to_author(row):
    author_id = row[0]
    name = row[1]
    age = row[2]
    gender = row[3]
    first_language = row[4]
    languages = [lang.strip() for lang in row[5].split(',')] #at this time the languages are stored in the DB like 'Language1, Language2, ...'
    region = row[6]
    job = row[7]
    chat_ids = [chat_id.strip() for chat_id in row[8].split(',')] if row[8] else []
    loaded_author = Author(author_id, name, age, gender, first_language, languages, region, job)
    loaded_author.chat_ids = chat_ids
    return loaded_author

def _convert_db_row_to_chat(row):
    chat_id = row[0]
    groupname = row[1]
    relation = row[2]
    loaded_chat = Chat(chat_id, relation, groupname)
    return loaded_chat

def _convert_db_row_to_message(row, db: SQLAlchemy, app: Flask):
    message_id = row[0]
    chat_id = row[1]
    sender_id = row[2]
    sender = CacheStore.Instance().get_author_by_id(sender_id) #TODO: sender does not to be set!
    timestamp = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S") 
    content = row[4] #TODO: add check for row name maybe?
    annotated_text = row[7]
    loaded_message = Message(chat_id=chat_id, message_id=message_id, sender=sender, timestamp=timestamp, content=content, annotated_text=annotated_text)
    return loaded_message


# endregion