from classes.message import Message
from datetime import datetime

class Chat:

    #TODO: group chats? -> participants + who is admin, title of group chat, creation date
    #other features -> pinned messages, archived?

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.messages = []
    
    def add_message(self, message):
        self.messages.append(message)

    def show_messages(self):
        for msg in self.messages:
            print(msg)

    