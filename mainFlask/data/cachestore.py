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

    # endregion
    
    #region Annotation
    
    _annotations = None

    def get_annotation_by_id(self, id):

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

    # endregion

    # endregion

    #region CREATE 

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
    def create_annotation(self, annotation: Annotation):
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
        from .db_handling import delete_author_by_id
        if delete_author_by_id(self._db, self._app, id):
            if self._authors is not None and id in self._authors:
                del self._authors[id]
            return True
        return False
    # endregion

    #region Annotation

    def delete_annotation_by_id(self, id: int) -> bool:
        from .db_handling import delete_annotation_by_id
        if delete_annotation_by_id(self._db, self._app, id):
            if self._annotations is not None and id in self._annotations:
                del self._annotations[id]
            return True
        return False

    # endregion

    # endregion