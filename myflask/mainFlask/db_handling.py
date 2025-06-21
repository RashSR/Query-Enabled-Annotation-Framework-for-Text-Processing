from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

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

    with app.app_context():
        db.create_all()
    
    print("Created db")