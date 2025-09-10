from mainFlask.data.cachestore import CacheStore
from .chat import Chat

class Author:
    def __init__(self, id, name, age = None, gender = None, first_language = None, languages = None, region = None, job = None, annotation = None, chats = None):
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
        self._annotation = annotation

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
    def chats(self) -> list[Chat]:
        self._chats = CacheStore.Instance().get_all_chats_by_author_id(self._id);
        return self._chats
    
    @chats.setter
    def chats(self, value):
        self._chats = value

    def add_chat(self, chat: Chat):
        self._chats.append(chat)

    @property
    def annotation(self) -> str:
        return self._annotation

    @annotation.setter
    def annotation(self, value: str):
        self._annotation = value

    def get_chat_by_id(self, chat_id: int):
        for chat in self.chats:
            if chat.chat_id == chat_id:
                return chat
            
        return None
    
    def get_all_own_messages(self):
        msg_list = []
        for chat in self.chats:
            own_messages = chat.get_messages_by_author(self)
            msg_list.extend(own_messages)
        
        return msg_list
    
    def get_error_categories(self):
        all_categories = {
            category
            for chat in self.chats
            for category in chat.get_error_categories_by_author(self)
        }
        return sorted(all_categories)

    def get_error_rule_ids(self):
        all_rule_ids = {
            rule_id
            for chat in self.chats
            for rule_id in chat.get_error_rule_ids_by_author(self)
        }
        return sorted(all_rule_ids)

    def __str__(self):
        return (f"Author({self._id}): {self.name}, "
                f"Age: {self.age}, Gender: {self.gender}, "
                f"First Language: {self.first_language}, "
                f"Other Languages: {', '.join(self.languages)}, "
                f"Region: {self.region}, Job: {self.job}, " 
                f"Chatcount: {len(self.chats)}")

    def get_messages_by_error_category(self, category):
        msgs = []
        if category in self.get_error_categories():
            for chat in self.chats:
                msgs.extend(chat.get_messages_by_error_category_and_author(category, self))
        
        return msgs
    
    def get_messages_by_error_rule_id(self, rule_id):
        msgs = []
        if rule_id in self.get_error_rule_ids():
            for chat in self.chats:
                msgs.extend(chat.get_messages_by_error_rule_id_and_author(rule_id, self))

        return msgs
    
    def __eq__(self, other):
        if isinstance(other, Author):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
