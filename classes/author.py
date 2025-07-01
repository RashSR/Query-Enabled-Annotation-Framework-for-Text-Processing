from classes.chat import Chat
from myflask.mainFlask.cachestore import CacheStore

class Author:
    def __init__(self, id, name, age = None, gender = None, first_language = None, languages = None, region = None, job = None, chats = None):
        self._id = id
        self._name = name
        self._age = age
        self._gender = gender
        self._first_language = first_language
        self._languages = languages if languages is not None else []
        self._region = region
        self._job = job
        self._chats = chats if chats is not None else []
        self._chat_ids = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

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
    def chat_ids(self):
        return self._chat_ids

    @chat_ids.setter
    def chat_ids(self, value):
        self._chat_ids = value

    @property
    def chats(self):
        self._chats = CacheStore.Instance().get_all_chats_by_author_id(self._id);
        return self._chats
    
    @chats.setter
    def chats(self, value):
        self._chats = value

    def add_chat(self, chat: Chat):
        self._chats.append(chat)

    def get_chat_by_id(self, chat_id: int):
        for chat in self.chats:
            if chat.chat_id == chat_id:
                return chat
            
        return None

    def get_chats_with_own_messages(self):
        list_of_chats = []
        for chat in self.chats:
            new_chat = Chat(chat.chat_id)
            list_of_chats.append(new_chat)
            for msg in chat.messages:
                if msg.sender.name == self._name:
                    new_chat.add_message(msg)
        
        return list_of_chats

    def get_all_own_messages(self):
        msg_list = []
        allChatsWithOwnMessages = self.get_chats_with_own_messages()
        for chat in allChatsWithOwnMessages:
            chatMessages = chat.messages
            for own_message in chatMessages:
                msg_list.append(own_message)
        
        return msg_list

    def get_all_messages(self):
        msg_list = []
        for chat in self.chats:
            for message in chat.messages:
                msg_list.append(message)

        return msg_list

    def __str__(self):
        return (f"Author({self._id}): {self.name}, "
                f"Age: {self.age}, Gender: {self.gender}, "
                f"First Language: {self.first_language}, "
                f"Other Languages: {', '.join(self.languages)}, "
                f"Region: {self.region}, Job: {self.job}, " 
                f"Chatcount: {len(self._chats)}")
