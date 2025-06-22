from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from sqlalchemy import text
from classes.author import Author
from classes.chat import Chat

def create_tables(db: SQLAlchemy, app: Flask):

    #here the models
    chat_participants = db.Table(
        'chat_participants',
        db.Column('chat_id', db.Integer, db.ForeignKey('chats.id'), primary_key=True),
        db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True)
    )

    class Author(db.Model):
        __tablename__ = 'authors'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        age = db.Column(db.Integer)
        gender = db.Column(db.String(20))
        first_language = db.Column(db.String(50))
        languages = db.Column(db.String(200))  # Comma-separated list
        region = db.Column(db.String(100))
        job = db.Column(db.String(100))

        chats = db.relationship('Chat', secondary=chat_participants, back_populates='participants')


    class Chat(db.Model):
        __tablename__ = 'chats'

        id = db.Column(db.Integer, primary_key=True)

        messages = db.relationship('Message', backref='chat', lazy=True)
        participants = db.relationship('Author', secondary=chat_participants, back_populates='chats')


    class Message(db.Model):
        __tablename__ = 'messages'

        id = db.Column(db.Integer, primary_key=True)
        chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)

        sender = db.Column(db.String(100), nullable=False)
        timestamp = db.Column(db.DateTime, default=datetime.utcnow)
        content = db.Column(db.Text, nullable=False)

        quoted_message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)
        quoted_message = db.relationship('Message', remote_side=[id])

        error_dict_json = db.Column(db.Text)  # Optional: store dict as JSON string
        annotated_text = db.Column(db.Text)

    new_author = Author(
        name="Max Mustermann",
        age=35,
        gender="Männlich",
        first_language="Deutsch",
        languages="Englisch, Spanisch",  # stored as comma-separated string
        region="München",
        job="Ingenieur"
    )
    db.session.add(new_author)
    db.session.commit()
    print(f"Added author with id {new_author.id}")

def add_authors(db: SQLAlchemy, author):
    db.session.add(author)
    db.session.commit()
    print(f"Added author with ID: {author.id}")

def get_authors(db: SQLAlchemy, app: Flask):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM author"))
        authors = []
        for row in result:
            author_id = row[0]
            name = row[1]
            age = row[2]
            gender = row[3]
            first_language = row[4]
            languages = [lang.strip() for lang in row[5].split(',')] #at this time the languages are stored in the DB like 'Language1, Language2, ...'
            region = row[6]
            job = row[7]
            loaded_author = Author(author_id, name, age, gender, first_language, languages, region, job)
            _get_chats_from_author(db, app, loaded_author)
            authors.append(loaded_author)
            print(loaded_author)
        return authors

def _get_chats_from_author(db: SQLAlchemy, app: Flask, author: Author):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM chat_participants WHERE author_id = :id"), {'id': author.author_id})
        for row in result:
            chat_id = row[0]
            loaded_chat = Chat(chat_id)
            author.add_chat(loaded_chat)
            #TODO: add messages
