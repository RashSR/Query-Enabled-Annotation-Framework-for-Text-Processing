from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from sqlalchemy import text
from classes.author import Author
from classes.chat import Chat
from classes.message import Message
from .cachestore import CacheStore
from .ltmatch import LTMatch

# region GET

#region Author

def get_all_authors(db: SQLAlchemy, app: Flask):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM author_with_chat_ids")) #specially created view with the chat_ids in it -> only one DB call needed
        authors = []
        for row in result:
            loaded_author = _convert_db_row_to_author(row)
            authors.append(loaded_author)
        return authors

def get_author_by_id(db: SQLAlchemy, app: Flask, id: int):
    with app.app_context():
        result_row = db.session.execute(
            text("SELECT * FROM author_with_chat_ids WHERE author_id = :id"),
            {'id': id}
        ).fetchone()

        loaded_author = _convert_db_row_to_author(result_row)
        return loaded_author
    
def get_author_by_name(db: SQLAlchemy, app: Flask, name: str):
    with app.context():
        result_row = db.session.execute(text("SELECT * FROM author_with_chat_ids WHERE name = :name"), {'name': name})
        
        if len(result_row) > 1: #more than one author with the same name
            return None
        
        loaded_author = _convert_db_row_to_author(result_row)
        return loaded_author
    
# endregion 

#region Chat

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

def get_chat_by_id(db: SQLAlchemy, app: Flask, chat_id: int):
    with app.app_context():
        result_row = db.session.execute(
            text("SELECT * FROM chat WHERE id = :id"),
            {'id': chat_id}
        ).fetchone() #TODO reuse this syntax in a function?
        chat = _convert_db_row_to_chat(result_row)
        result = db.session.execute(text("SELECT * FROM message_with_ltm_ids where chat_id = :id"), {'id': chat_id})
        for row in result:
            loaded_message = _convert_db_row_to_message(row)
            loaded_message.chat = chat
            chat.add_message(loaded_message)

        return chat

# endregion

#region Message
def get_all_messages(db: SQLAlchemy, app: Flask):
    with app.app_context():
        messages = []
        result = db.session.execute(text("SELECT * FROM message_with_ltm_ids"))
        for row in result:
            loaded_message = _convert_db_row_to_message(row)
            messages.append(loaded_message)

    return messages

def get_message_by_id(db: SQLAlchemy, app: Flask, id: int):
    with app.app_context():
        result_row = db.session.execute(
            text("SELECT * FROM message_with_ltm_ids WHERE id = :id"),
            {'id': id}
        ).fetchone()

        loaded_message = _convert_db_row_to_message(result_row)
        return loaded_message
        
        #TODO: only load stuff that is not available

# endregion

#region LTM

def get_all_ltms_by_msg_id_and_chat_id(db:SQLAlchemy, app: Flask, msg_id: int, chat_id: int):
    with app.app_context():
        ltms: list[LTMatch] = []
        result = db.session.execute(
            text("SELECT * FROM lt_match WHERE chat_id = :chat_id AND message_id = :msg_id"),
            {'chat_id': chat_id, 'msg_id': msg_id}
        )
        for row in result:
            loaded_ltm = _convert_db_row_to_ltm(row)
            ltms.append(loaded_ltm)

        return ltms
    
# endregion

# endregion

# region CREATE

#TODO: Category own DB table? 
def create_lt_match(db: SQLAlchemy, app: Flask, lt_match: LTMatch):
    with app.app_context():
        message_id = lt_match.message_id
        chat_id = lt_match.chat_id
        start_pos = lt_match.start_pos
        end_pos = lt_match.end_pos
        content = lt_match.text
        category = lt_match.category
        rule_id = lt_match.rule_id

        sql_text = text("INSERT INTO lt_match VALUES (:id, :message_id, :chat_id, :start_pos, :end_pos, :content, :category, :rule_id)")
        prepared_values = {'id': None, 'message_id': message_id, 'chat_id': chat_id, 'start_pos': start_pos, 'end_pos': end_pos, 'content': content, 'category': category, 'rule_id': rule_id}

        result = db.session.execute(sql_text, prepared_values)
        db.session.commit()

        new_id = result.lastrowid
        return new_id

# endregion 

#region Conversion

def _convert_db_row_to_author(row) -> Author:
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

def _convert_db_row_to_chat(row) -> Chat:
    chat_id = row[0]
    groupname = row[1]
    relation = row[2]
    loaded_chat = Chat(chat_id, relation, groupname)
    return loaded_chat

def _convert_db_row_to_message(row) -> Message:
    message_id = row[0]
    chat_id = row[1]
    sender_id = row[2]
    sender = CacheStore.Instance().get_author_by_id(sender_id) #TODO: sender does not to be set!
    timestamp = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S") 
    content = row[4] #TODO: add check for row name maybe?
    #quoted_msg is in row[5]
    annotated_text = row[6]
    ltm_ids = [ltm_id.strip() for ltm_id in row[7].split(',')] if row[7] else []
    loaded_message = Message(chat_id=chat_id, message_id=message_id, sender=sender, timestamp=timestamp, content=content, annotated_text=annotated_text)
    loaded_message.ltmatch_ids = ltm_ids
    return loaded_message

def _convert_db_row_to_ltm(row) -> LTMatch:
    id = row[0]
    message_id = row[1]
    chat_id = row[2]
    start_pos = row[3]
    end_pos = row[4]
    content = row[5]
    category = row[6]
    rule_id = row[7]

    loaded_ltm = LTMatch(message_id, chat_id, start_pos, end_pos, content, category, rule_id)
    loaded_ltm.id = id
    return loaded_ltm


# endregion