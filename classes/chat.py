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
        if all(participant.author_id != message.sender.author_id for participant in self.participants):
            self.participants.append(message.sender)

    def show_messages(self):
        for msg in self.messages:
            print(msg)

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, value):
        self._chat_id = value

    @property
    def participants(self) -> list:
        return self._participants

    @participants.setter
    def participants(self, value):
        self._participants = value

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, value):
        self._messages = value

    def get_participant_names(self):
        name_list = []
        for a in self._participants:
            name_list.append(a.name)
        
        return name_list

    def get_message_count_for_author(self, author):
        count = 0
        for msg in self.messages:
            if msg.sender.name == author.name:
                count = count + 1

        return count