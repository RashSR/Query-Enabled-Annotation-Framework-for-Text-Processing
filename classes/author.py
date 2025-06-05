from classes.chat import Chat
#from classes.message import Message
from datetime import datetime

class Author:
    def __init__(self, author_id, name, age = None, gender = None, first_language = None, languages = None, region = None, job = None, chats = None):
        self._author_id = author_id
        self._name = name
        self._age = age
        self._gender = gender
        self._first_language = first_language
        self._languages = languages if languages is not None else []
        self._region = region
        self._job = job
        self._chats = chats if chats is not None else []

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        self._author_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = value

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = value

    @property
    def first_language(self):
        return self._first_language

    @first_language.setter
    def first_language(self, value):
        self._first_language = value

    @property
    def languages(self):
        return self._languages

    @languages.setter
    def languages(self, value):
        self._languages = value

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        self._region = value

    @property
    def job(self):
        return self._job

    @job.setter
    def job(self, value):
        self._job = value

    @property
    def chats(self):
        return self._chats

    def add_chat(self, chat):
        self._chats.append(chat)

    def get_chats_with_own_messages(self):
        list_of_chats = []
        for chat in self._chats:
            new_chat = Chat(chat.chat_id)
            list_of_chats.append(new_chat)
            for msg in chat.messages:
                if msg.sender == self._name:
                    new_chat.add_message(msg)
        
        return list_of_chats

    def get_all_own_messages(self):
        return None


    def __str__(self):
        return (f"Author({self.author_id}): {self.name}, "
                f"Age: {self.age}, Gender: {self.gender}, "
                f"First Language: {self.first_language}, "
                f"Other Languages: {', '.join(self.languages)}, "
                f"Region: {self.region}, Job: {self.job}")
