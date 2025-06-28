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
            self._authors = get_all_authors(self._db, self._app, False) 

        return self._authors
        
        

    