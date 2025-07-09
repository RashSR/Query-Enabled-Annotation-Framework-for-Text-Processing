from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from .ltmatch import LTMatch 

class CacheStore:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db: SQLAlchemy = None, app: Flask = None):
        if self.__class__._initialized:
            if db is not None or app is not None:
                raise Exception("CacheStore is already initialized")
            return
        self._db = db
        self._app = app
        self.__class__._initialized = True

    @classmethod
    def Instance(cls, db: SQLAlchemy = None, app: Flask = None):
        return cls(db, app)
    
    #region GET
    
    #region Author

    _authors = None #use dict to go from O(n) to O(1)
    _loaded_all_authors = False

    def get_all_authors(self):
        from mainFlask.db_handling import get_all_authors

        if self._authors is None or self._loaded_all_authors is False:
            authors = get_all_authors(self._db, self._app)
            self._authors = {author.id: author for author in authors}
            self._loaded_all_authors = True

        return list(self._authors.values())
    
    def get_author_by_id(self, id):

        if not isinstance(id, int):
            return None

        from mainFlask.db_handling import get_author_by_id

        if self._authors is None:
            self._authors = {}

        if id in self._authors:
            return self._authors[id]
        
        author = get_author_by_id(self._db, self._app, id) #db_handling function
        self._authors[id] = author
        return author
    
    # endregion
    
    # region Chat

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
            from mainFlask.db_handling import get_chat_by_ids
            missing_chats = get_chat_by_ids(self._db, self._app, not_cached_chat_ids)
            chats.extend(missing_chats)
            #this could be async -> store loaded chats in cache
            for chat in missing_chats:
                self._chats[chat.chat_id] = chat

        return chats
    
    def get_chat_by_id(self, id):

        if not isinstance(id, int):
            return None

        from mainFlask.db_handling import get_chat_by_id

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
        from mainFlask.db_handling import get_all_messages

        if self._messages is None or self._loaded_all_messages is False:
            messages = get_all_messages(self._db, self._app)
            self._messages = {message.id: message for message in messages}
            self._loaded_all_messages = True

        return list(self._messages.values())
    
    def get_message_by_id(self):

        if not isinstance(id, int):
            return None

        from mainFlask.db_handling import get_message_by_id

        if self._messages is None:
            self._messages = {}

        if id in self._messages:
            return self._messages[id]
        
        message = get_message_by_id(self._db, self._app, id) #db_handling function
        self._messages[id] = message
        return message
    
    # endregion

    #region LTM

    _ltms = None

    def get_all_ltms_by_msg_id_and_chat_id(self, msg_id, chat_id):
        #TODO: is always loaded, maybe look up in store?
        if not isinstance(msg_id, int) or not isinstance(chat_id, int):
            return None
        
        from mainFlask.db_handling import get_all_ltms_by_msg_id_and_chat_id
        
        if self._ltms is None:
            self._ltms = {}

        ltms: list[LTMatch] = get_all_ltms_by_msg_id_and_chat_id(self._db, self._app, msg_id, chat_id)
        return ltms
    
    # endregion
    
    # endregion

    #region CREATE 

    #region LTM

    def create_lt_match(self, lt_match: LTMatch):
        if lt_match is None:
            return None
        
        from mainFlask.db_handling import create_lt_match

        generated_id = create_lt_match(self._db, self._app, lt_match)
        lt_match.id = generated_id

        if self._ltms is None:
            self._ltms = {}

        self._ltms[generated_id] = lt_match
        return lt_match
    
    # endregion


    # endregion 

        
    