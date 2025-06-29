from flask_sqlalchemy import SQLAlchemy
from flask import Flask

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
    
    
    _authors = None #use dict to go from O(n) to O(1)

    def get_all_authors(self):
        from myflask.mainFlask.db_handling import get_all_authors

        if self._authors is None:
            authors = get_all_authors(self._db, self._app)
            self._authors = {author.id: author for author in authors}

        return list(self._authors.values())
    
    def get_author_by_id(self, id):

        if not isinstance(id, int):
            return None

        from myflask.mainFlask.db_handling import get_author_by_id

        if self._authors is None:
            self._authors = {}

        if id in self._authors:
            return self._authors[id]
        
        author = get_author_by_id(self._db, self._app, id) #db_handling function
        self._authors[id] = author
        return author
    
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
            from myflask.mainFlask.db_handling import get_chat_by_ids
            missing_chats = get_chat_by_ids(self._db, self._app, not_cached_chat_ids)
            chats.extend(missing_chats)
            #this could be async -> store loaded chats in cache
            for chat in missing_chats:
                self._chats[chat.chat_id] = chat

        return chats
    
    def get_chat_by_id(self, id):

        if not isinstance(id, int):
            return None

        from myflask.mainFlask.db_handling import get_chat_by_id

        if self._chats is None:
            self._chats = {}
        
        if id in self._chats:
            return self._chats[id]
        
        chat = get_chat_by_id(self._db, self._app, id)
        self._chats[id] = chat
        return chat


        
    