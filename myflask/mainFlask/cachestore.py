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
            authors = get_all_authors(self._db, self._app, True)
            self._authors = {author.author_id: author for author in authors}

        return list(self._authors.values())
    
    def get_author_by_id(self, id):
        from myflask.mainFlask.db_handling import get_author_by_id

        if self._authors is None:
            self._authors = {}

        if id in self._authors:
            return self._authors[id]

        # Otherwise, load from DB and cache it
        author = get_author_by_id(self._db, self._app, id) #db_handling function
        self._authors[id] = author
        return author
            
        
    