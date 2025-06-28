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
    
    _authors = None

    def get_all_authors(self):
        from myflask.mainFlask.db_handling import get_all_authors
        if self._authors is None:
            self._authors = get_all_authors(self._db, self._app, True)

        return self._authors
    
    def get_author_by_id(self, id):
        from myflask.mainFlask.db_handling import get_author_by_id

        if self._authors is None:
            self._authors = []

        author = next((a for a in self._authors if a.author_id == id), None)

        if author is None:
            author = get_author_by_id(self._db, self._app, id)
            self._authors.append(author)

        return author
            
        
    #TODO use dict
    #def get_author_by_id(self, id):
    #from myflask.mainFlask.db_handling import get_author_by_id

    #if not hasattr(self, "_author_cache"):
        #self._author_cache = {}

    #if id not in self._author_cache:
        #self._author_cache[id] = get_author_by_id(self._db, self._app, id)

    #return self._author_cache[id]
        
    