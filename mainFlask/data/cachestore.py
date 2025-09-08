from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from mainFlask.classes.ltmatch import LTMatch 
from mainFlask.classes.spacymatch import SpacyMatch 
from mainFlask.classes.annotation import Annotation

class CacheStore:
    _instance = None

    def __init__(self, db: SQLAlchemy, app: Flask = None):
        self._db = db
        self._app = app

    @classmethod
    def Instance(cls, db: SQLAlchemy = None, app: Flask = None):
        if cls._instance is None:
            if db is None:
                raise ValueError("A SQLAlchemy instance must be provided on first initialization")
            cls._instance = cls(db, app)
        return cls._instance

    #region GET
    
    #region Author

    _authors = None #use dict to go from O(n) to O(1)
    _loaded_all_authors = False

    def get_all_authors(self):
        from .db_handling import get_all_authors

        if self._authors is None or self._loaded_all_authors is False:
            authors = get_all_authors(self._db, self._app)
            self._authors = {author.id: author for author in authors}
            self._loaded_all_authors = True

        return list(self._authors.values())
    
    def get_author_by_id(self, id):

        if not isinstance(id, int):
            return None

        from .db_handling import get_author_by_id

        if self._authors is None:
            self._authors = {}

        if id in self._authors:
            return self._authors[id]
        
        author = get_author_by_id(self._db, self._app, id) #db_handling function
        self._authors[id] = author
        return author
    
    def get_author_by_name(self, name: str):
        from .db_handling import get_author_by_name 

        if self._authors is None:
            self._authors = {}

        for author in self._authors.values():
            if author.name == name:
                return author
            
        author = get_author_by_name(self._db, self._app, name)
        self._authors[author.id] = author
        return author
        
    
    # endregion
    
    #region Chat

    _chats = None

    def get_all_chats_by_author_id(self, author_id):
        
        if not isinstance(author_id, int):
            return None
        
        #initialize dictionary
        if self._chats is None:
            self._chats = {}

        chat_ids = self.get_author_by_id(author_id).chat_ids;
        not_cached_chat_ids = []
        chats = []
        for c_id in chat_ids:
            if c_id in self._chats:
                #append exisitng chat
                cached_chat = self._chats[c_id]
                chats.append(cached_chat)
            else:
                not_cached_chat_ids.append(c_id)

        if len(not_cached_chat_ids) > 0:
            # Need to load from DB
            from .db_handling import get_chat_by_ids
            missing_chats = get_chat_by_ids(self._db, self._app, not_cached_chat_ids)
            chats.extend(missing_chats)
            #this could be async -> store loaded chats in cache
            for chat in missing_chats:
                self._chats[chat.chat_id] = chat

        return chats
    
    def get_chat_by_id(self, id):

        if not isinstance(id, int):
            return None

        from .db_handling import get_chat_by_id

        if self._chats is None:
            self._chats = {}
        
        if id in self._chats:
            return self._chats[id]
        
        chat = get_chat_by_id(self._db, self._app, id)
        self._chats[id] = chat
        return chat
    
    # endregion

    #region Message
    
    _messages = None
    _loaded_all_messages = False

    def get_all_messages(self):
        from .db_handling import get_all_messages

        if self._messages is None or self._loaded_all_messages is False:
            messages = get_all_messages(self._db, self._app)
            self._messages = {message.message_id: message for message in messages}
            self._loaded_all_messages = True

        return list(self._messages.values())
    
    def get_message_by_id(self, id):

        if not isinstance(id, int):
            return None

        from .db_handling import get_message_by_id

        if self._messages is None:
            self._messages = {}

        if id in self._messages:
            return self._messages[id]
        
        message = get_message_by_id(self._db, self._app, id) #db_handling function
        
        if message is not None:
            self._messages[id] = message
        
        return message
    
    def get_messages_by_recipient_id(self, recipient_name: str):
        from .db_handling import get_messages_by_recipient_id

        if self._messages is None:
            self._messages = {}

        messages = get_messages_by_recipient_id(self._db, self._app, recipient_name)
        for msg in messages:
            self._messages[msg.message_id] = msg

        return messages
    
    def get_messages_by_error_category(self, category: str):
        from .db_handling import get_messages_by_error_category

        if self._messages is None:
            self._messages = {}
        
        messages = get_messages_by_error_category(self._db, self._app, category)
        for msg in messages:
            self._messages[msg.message_id] = msg

        return messages
    
    def get_messages_by_error_rule_id(self, rule_id: str):
        from .db_handling import get_messages_by_error_rule_id

        if self._messages is None:
            self._messages = {}
        
        messages = get_messages_by_error_rule_id(self._db, self._app, rule_id)
        for msg in messages:
            self._messages[msg.message_id] = msg
            
        return messages
    
    def get_messages_by_substring_in_content(self, search_string: str):
        from .db_handling import get_messages_by_substring_in_content

        #TODO: make this call modular
        if self._messages is None:
            self._messages = {}

        messages = get_messages_by_substring_in_content(self._db, self._app, search_string)
        #TODO make this call modular
        for msg in messages:
            self._messages[msg.message_id] = msg
        
        return messages
    
    def get_messages_from_spacy_matches_by_column_and_value(self, column_name: str, value: str):
        from .db_handling import get_messages_from_spacy_matches_by_column_and_value
        
        if self._messages is None:
            self._messages = {}
        
        messages = get_messages_from_spacy_matches_by_column_and_value(self._db, self._app, column_name, value)
        for msg in messages:
            self._messages[msg.message_id] = msg

        return messages

    # endregion

    #region LTM

    _ltms = None

    def get_all_ltms_by_msg_id_and_chat_id(self, msg_id, chat_id):
        #TODO: is always loaded, maybe look up in store?
        if not isinstance(msg_id, int) or not isinstance(chat_id, int):
            return None
        
        from .db_handling import get_all_ltms_by_msg_id_and_chat_id
        
        if self._ltms is None:
            self._ltms = {}

        ltms: list[LTMatch] = get_all_ltms_by_msg_id_and_chat_id(self._db, self._app, msg_id, chat_id)
        return ltms
    
    def get_all_distinct_categories_from_ltms(self):
        from .db_handling import get_all_distinct_categories_from_ltms
        categories = get_all_distinct_categories_from_ltms(self._db, self._app)
        return categories

    def get_all_distinct_rule_ids_from_ltms(self):
        from .db_handling import get_all_distinct_rule_ids_from_ltms
        rule_ids = get_all_distinct_rule_ids_from_ltms(self._db, self._app)
        return rule_ids
    
    # endregion

    #region Spacy Match

    _spacy_matches = None

    def get_all_distinct_column_values_from_spacy_matches_by_column_name(self, column_name: str):
        from .db_handling import get_all_distinct_column_values_from_spacy_matches_by_column_name
        column_values = get_all_distinct_column_values_from_spacy_matches_by_column_name(self._db, self._app, column_name)
        return column_values
    
    def get_all_spacy_matches_by_msg_id(self, msg_id: int):
        from .db_handling import get_all_spacy_matches_by_msg_id
        
        if self._spacy_matches is None:
            self._spacy_matches = {}

        spacy_matches: list[SpacyMatch] = get_all_spacy_matches_by_msg_id(self._db, self._app, msg_id)
        return spacy_matches

    # endregion
    
    #region Annotation
    
    _annotations = None

    def get_annotation_by_id(self, id) -> Annotation:

        if not isinstance(id, int):
            return None

        from .db_handling import get_annotation_by_id

        if self._annotations is None:
            self._annotations = {}

        if id in self._annotations:
            return self._annotations[id]
        
        annotation = get_annotation_by_id(self._db, self._app, id)
        self._annotations[id] = annotation
        return annotation
    
    def get_all_annotations_by_msg_id(self, msg_id: int) -> list[Annotation]:
        from .db_handling import get_all_annotations_by_msg_id
        
        if self._annotations is None:
            self._annotations = {}

        annotations: list[Annotation] = get_all_annotations_by_msg_id(self._db, self._app, msg_id)
        return annotations

    # endregion

    # endregion

    #region CREATE 

    #region Author

    def create_author(self, author):
        if author is None:
            return None
        
        from .db_handling import create_author

        generated_id = create_author(self._db, self._app, author)
        author.id = generated_id

        if self._authors is None:
            self._authors = {}

        self._authors[generated_id] = author
        return author
    
    # endregion

    #region Chat
    def create_chat(self, chat):
        if chat is None:
            return None
        
        from .db_handling import create_chat

        generated_id = create_chat(self._db, self._app, chat)
        chat.chat_id = generated_id

        if self._chats is None:
            self._chats = {}

        self._chats[generated_id] = chat
        for author in chat.participants:
            self._authors[author.id].chat_ids.append(generated_id)
            self._authors[author.id].chats.append(chat)

        return chat
    
    # endregion

    #region Message
    def create_message(self, message):
        if message is None:
            return None
        
        from .db_handling import create_message

        generated_id = create_message(self._db, self._app, message)
        message.message_id = generated_id

        if self._messages is None:
            self._messages = {}

        self._messages[generated_id] = message
        self._chats[message.chat_id].add_message(message)

        return message
    
    def create_messages(self, messages):
        if messages is None or len(messages) == 0:
            return None

        created_messages = []
        for msg in messages:
            created_msg = self.create_message(msg)
            created_messages.append(created_msg)

        return created_messages
    # endregion

    #region LTM

    def create_lt_match(self, lt_match: LTMatch):
        if lt_match is None:
            return None
        
        from .db_handling import create_lt_match

        generated_id = create_lt_match(self._db, self._app, lt_match)
        lt_match.id = generated_id

        if self._ltms is None:
            self._ltms = {}

        self._ltms[generated_id] = lt_match
        self._messages[lt_match.message_id].ltmatch_ids.append(lt_match.id)
        self._messages[lt_match.message_id].error_list.append(lt_match)
        return lt_match
    
    # endregion

    #region SpacyMatch
    def create_spacy_match(self, spacy_match: SpacyMatch):
        if spacy_match is None:
            return None
        
        from .db_handling import create_spacy_match

        generated_id = create_spacy_match(self._db, self._app, spacy_match)
        spacy_match.id = generated_id

        if self._spacy_matches is None:
            self._spacy_matches = {}

        self._spacy_matches[generated_id] = spacy_match
        return spacy_match

    # endregion

    #region Annoation
    def create_annotation(self, annotation: Annotation) -> Annotation:
        if annotation is None:
            return None
        
        from .db_handling import create_annotation

        generated_id = create_annotation(self._db, self._app, annotation)
        annotation.id = generated_id

        if self._annotations is None:
            self._annotations = {}

        self._annotations[generated_id] = annotation
        return annotation
    
    # endregion

    # endregion 

    #region UPDATE

    #region Author
    def update_author(self, author, column_name: str, value):
        from .db_handling import update_author
        if update_author(self._db, self._app, author.id, column_name, value):
            setattr(author, column_name, value)
            self._authors[author.id] = author
            return self._authors[author.id]
        
        return None

    # endregion

    #region Chat
    def update_chat(self, chat, column_name: str, value):
        from .db_handling import update_chat
        if update_chat(self._db, self._app, chat.chat_id, column_name, value):
            setattr(chat, column_name, value)
            self._chats[chat.chat_id] = chat
            return self._chats[chat.chat_id]
        
        return None
    
    # endregion

    #region Message
    def update_message(self, message, column_name: str, value):
        from .db_handling import update_message
        if update_message(self._db, self._app, message.message_id, column_name, value):
            setattr(message, column_name, value)
            self._messages[message.message_id] = message
            return self._messages[message.message_id]
        
        return None
    
    # endregion

    # region LTM
    def update_lt_match(self, lt_match: LTMatch):
        from .db_handling import update_lt_match
        if update_lt_match(self._db, self._app, lt_match):
            self._ltms[lt_match.id] = lt_match
            return self._ltms[lt_match.id]
        
        return None
    
    # endregion
    
    # region SpacyMatch
    def update_spacy_match(self, spacy_match: SpacyMatch):
        from .db_handling import update_spacy_match
        if update_spacy_match(self._db, self._app, spacy_match):
            self._spacy_matches[spacy_match.id] = spacy_match
            return self._spacy_matches[spacy_match.id]
        
        return None
    
    # endregion
    
    #region Annotation

    def update_annotation(self, annotation: Annotation):
        from .db_handling import update_annotation
        
        if update_annotation(self._db, self._app, annotation):
            self._annotations[annotation.id] = annotation
            return self._annotations[annotation.id]
        
        return None

    # endregion

    # endregion
    
    #region DELETE
    
    #region Author

    def delete_author_by_id(self, id: int) -> bool:
        id = int(id)
        from .db_handling import delete_author_by_id
        if delete_author_by_id(self._db, self._app, id):
            if self._authors is not None and id in self._authors:
                del self._authors[id]
            return True
        return False
    # endregion

    #region Chat

    def delete_chat_by_id(self, id: int) -> bool:
        id = int(id)
        from .db_handling import delete_chat_by_id
        if delete_chat_by_id(self._db, self._app, id):
            if self._chats is not None and id in self._chats:
                del self._chats[id]
            return True
        return False
    
    # endregion

    #region Message

    def delete_message_by_id(self, id: int) -> bool:
        id = int(id)
        from .db_handling import delete_message_by_id
        if delete_message_by_id(self._db, self._app, id):
            if self._messages is not None and id in self._messages:
                del self._messages[id]
            return True
        return False
    
    # endregion
    
    # region LTM
    def delete_lt_match_by_id(self, id: int) -> bool:
        id = int(id)
        from .db_handling import delete_lt_match_by_id
        if delete_lt_match_by_id(self._db, self._app, id):
            if self._ltms is not None and id in self._ltms:
                del self._ltms[id]
            return True
        return False
    
    # endregion

    # region SpacyMatch
    def delete_spacy_match_by_id(self, id: int) -> bool:
        id = int(id)
        from .db_handling import delete_spacy_match_by_id
        if delete_spacy_match_by_id(self._db, self._app, id):
            if self._spacy_matches is not None and id in self._spacy_matches:
                del self._spacy_matches[id]
            return True
        return False
    
    # endregion

    #region Annotation

    def delete_annotation_by_id(self, id: int) -> bool:
        id = int(id)
        from .db_handling import delete_annotation_by_id
        if delete_annotation_by_id(self._db, self._app, id):
            if self._annotations is not None and id in self._annotations:
                del self._annotations[id]
            return True
        return False

    # endregion

    # endregion

    #region Temporary

    _temporary = None

    def save_temporary_data(self, data):
        self._temporary = data

    def get_temporary_data(self):
        return self._temporary 
    
    def clear_temporary_data(self):
        self._temporary = None

    # endregion