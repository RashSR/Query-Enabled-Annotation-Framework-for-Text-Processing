from classes.message import Message
from datetime import datetime

class Chat:

    #TODO: group chats? -> participants + who is admin, title of group chat, creation date
    #other features -> pinned messages, archived?

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.messages = []
        self.participants = []
    
    def add_message(self, message):
        self.messages.append(message)
        if message.sender not in self.participants:
            self.participants.append(message.sender)

    def show_messages(self):
        for msg in self.messages:
            print(msg)

    @property
    def participants(self):
        return self._participants

    @participants.setter
    def participants(self, value):
        self._participants = value