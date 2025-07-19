from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from sqlalchemy import text
from mainFlask.classes.author import Author
from mainFlask.classes.chat import Chat
from mainFlask.classes.message import Message
from .cachestore import CacheStore
from mainFlask.classes.ltmatch import LTMatch
from mainFlask.classes.spacymatch import SpacyMatch

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
    with app.app_context():
        result_row = db.session.execute(
            text("SELECT * FROM author_with_chat_ids WHERE name = :name"), 
            {'name': name}
        ).fetchone()
        
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
        result = db.session.execute(text("SELECT * FROM message_with_ltm_and_spacy_ids"))
        for row in result:
            loaded_message = _convert_db_row_to_message(row)
            messages.append(loaded_message)

    return messages

def get_message_by_id(db: SQLAlchemy, app: Flask, id: int):
    with app.app_context():
        result_row = db.session.execute(
            text("SELECT * FROM message_with_ltm_and_spacy_ids WHERE id = :id"),
            {'id': id}
        ).fetchone()

        loaded_message = _convert_db_row_to_message(result_row)
        return loaded_message
        
        #TODO: only load stuff that is not available

def get_messages_by_recipient_id(db: SQLAlchemy, app: Flask, recipient_id: int):
    with app.app_context():
        results = db.session.execute(
            text("SELECT chat_id FROM chat_participants WHERE author_id = :recipient_id"),
            {'recipient_id': recipient_id}
        )
        messages = []

        for row in results:
            chat_id = row[0]
            chat = get_chat_by_id(db, app, chat_id)
            for msg in chat.messages:
                if msg.sender.id != recipient_id:
                    messages.append(msg)
        
        return messages

#TODO: idea -> for get requests add dictionary like [param, value] -> SELECT * FROM message_with_ltm_ids WHERE param = :value
def get_messages_by_error_category(db: SQLAlchemy, app: Flask, error_category: str):
    with app.app_context():
        results = db.session.execute(
            text("SELECT * FROM message_join_lt_match WHERE category = :category"),
            {'category': error_category}
        )

        messages = []
        seen_ids = set()

        for row in results:
            msg = _convert_db_row_to_message(row, tableHasChatIds=False)
            if msg.message_id not in seen_ids:
                seen_ids.add(msg.message_id)
                messages.append(msg)
        
        return messages
    
def get_messages_by_error_rule_id(db: SQLAlchemy, app: Flask, error_rule_id: str):
    with app.app_context():
        results = db.session.execute(
            text("SELECT * FROM message_join_lt_match WHERE rule_id = :rule_id"),
            {'rule_id': error_rule_id}
        )

        messages = []
        seen_ids = set()

        for row in results:
            msg = _convert_db_row_to_message(row, tableHasChatIds=False)
            if msg.message_id not in seen_ids:
                seen_ids.add(msg.message_id)
                messages.append(msg)

        return messages

def get_messages_by_substring_in_content(db: SQLAlchemy, app: Flask, search_string: str):
    with app.app_context():
        results = db.session.execute(
            text("SELECT * FROM message_with_ltm_and_spacy_ids WHERE content LIKE :search_string "), #for case_sensitiv -> WHERE content LIKE :search_string COLLATE BINARY
            {'search_string': f"%{search_string}%"}
        )

        #TODO: make this call modular
        messages = []
        for row in results:
            msg = _convert_db_row_to_message(row)
            messages.append(msg)
        
        return messages


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

def get_all_distinct_categories_from_ltms(db:SQLAlchemy, app: Flask):
    with app.app_context():
        categories: list[str] = []
        result = db.session.execute(text("SELECT DISTINCT category FROM lt_match"))
        for row in result:
            category = row[0]
            categories.append(category)

        return categories
    
def get_all_distinct_rule_ids_from_ltms(db:SQLAlchemy, app: Flask):
    with app.app_context():
        rule_ids: list[str] = []
        result = db.session.execute(text("SELECT DISTINCT rule_id FROM lt_match"))
        for row in result:
            rule_id = row[0]
            rule_ids.append(rule_id)

        return rule_ids

# endregion

# region Spacy Matches

def get_all_distinct_column_values_from_spacy_matches_by_column_name(db: SQLAlchemy, app: Flask, column_name: str):
    with app.app_context():
        column_values: list[str] = []

        sql_text = f"SELECT DISTINCT {column_name} FROM spacy_match"
        result = db.session.execute(text(sql_text))
        for row in result:
            column_value = row[0]
            column_values.append(column_value)

        return column_values
    
def get_all_spacy_matches_by_msg_id(db: SQLAlchemy, app: Flask, msg_id: int):
    with app.app_context():
        spacy_matches: list[SpacyMatch] = []
        result = db.session.execute(
            text("SELECT * FROM spacy_match WHERE message_id = :msg_id"),
            {'msg_id': msg_id}
        )
        for row in result:
            loaded_spacy_match = _convert_db_row_to_spacy_match(row)
            spacy_matches.append(loaded_spacy_match)

        return spacy_matches 

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

def create_spacy_match(db: SQLAlchemy, app: Flask, spacy_match: SpacyMatch):
    with app.app_context():
        sql_text = text("""
            INSERT INTO spacy_match (
                id, message_id, chat_id, start_pos, end_pos, text,
                lemma, pos, tag, is_alpha, is_stop,
                tense, person, verb_form, voice, degree, gram_case,
                number, gender, mood, pron_type
            ) VALUES (
                :id, :message_id, :chat_id, :start_pos, :end_pos, :text,
                :lemma, :pos, :tag, :is_alpha, :is_stop,
                :tense, :person, :verb_form, :voice, :degree, :gram_case,
                :number, :gender, :mood, :pron_type
            )
        """)

        values = {
            'id': None,
            'message_id': spacy_match.message_id,
            'chat_id': spacy_match.chat_id,
            'start_pos': spacy_match.start_pos,
            'end_pos': spacy_match.end_pos,
            'text': spacy_match.text,
            'lemma': spacy_match.lemma,
            'pos': spacy_match.pos,
            'tag': spacy_match.tag,
            'is_alpha': spacy_match.is_alpha,
            'is_stop': spacy_match.is_stop,
            'tense': spacy_match.tense,
            'person': spacy_match.person,
            'verb_form': spacy_match.verb_form,
            'voice': spacy_match.voice,
            'degree': spacy_match.degree,
            'gram_case': spacy_match.gram_case,
            'number': spacy_match.number,
            'gender': spacy_match.gender,
            'mood': spacy_match.mood,
            'pron_type': spacy_match.pron_type
        }

        result = db.session.execute(sql_text, values)
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

def _convert_db_row_to_message(row, tableHasChatIds: bool = True) -> Message:
    message_id = row[0]
    chat_id = row[1]
    sender_id = row[2]
    sender = CacheStore.Instance().get_author_by_id(sender_id) #TODO: sender does not to be set!
    timestamp = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S") 
    content = row[4]
    #quoted_msg is in row[5]
    annotated_text = row[6]
    loaded_message = Message(chat_id=chat_id, message_id=message_id, sender=sender, timestamp=timestamp, content=content, annotated_text=annotated_text)
    if tableHasChatIds:
        ltm_ids = [ltm_id.strip() for ltm_id in row[7].split(',')] if row[7] else []
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

def _convert_db_row_to_spacy_match(row) -> SpacyMatch:
    id = row[0]
    message_id = row[1]
    chat_id = row[2]
    start_pos = row[3]
    end_pos = row[4]
    content = row[5]
    lemma = row[6]
    pos = row[7]
    tag = row[8]
    is_alpha = row[9]
    is_stop = row[10]
    tense = row[11]
    person = row[12]
    verb_form = row[13]
    voice = row[14]
    degree = row[15]
    gram_case = row[16]
    number = row[17]
    gender = row[18]
    mood = row[19]
    pron_type = row[20]

    loaded_spacy_match = SpacyMatch(message_id, chat_id, start_pos, end_pos, content, 
                                    lemma, pos, tag, is_alpha, is_stop, tense, person, 
                                    verb_form, voice, degree, gram_case, number, 
                                    gender, mood, pron_type)
    loaded_spacy_match.id = id
    return loaded_spacy_match



# endregion