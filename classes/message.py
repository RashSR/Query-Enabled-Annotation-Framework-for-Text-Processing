from classes.messagetype import MessageType
from typing import Dict
from myflask.mainFlask.cachestore import CacheStore

class Message:
    def __init__(self, chat_id, message_id, sender, timestamp, content, message_type = MessageType.TEXT, quoted_message = None, error_dict : Dict[str, int] = None, annotated_text = None, chat = None):
        self.chat_id = chat_id
        self._message_id = message_id
        self.sender = sender
        self.timestamp = timestamp
        self.content = content
        self.message_type = message_type
        self.quoted_message = quoted_message
        self._error_dict = {}
        self._annotated_text = annotated_text
        self._chat = chat

    def __str__(self):
        toString = f"""ChatId: {self.chat_id}, MessageId: {str(self._message_id)}
        Sender: {self.sender.name}
        Timestamp: {self.timestamp}
        Content: {self.content}
        MessageType: {self.message_type}
        quotedMessage: {{ {self.quoted_message } }}
        ErrorTypes: {len(self.error_dict)}
        """
        return toString
    
    def hasQuote(self):
        if self.quoted_message == None:
            return True
        return False
    
    def add_to_error_dict(self, error: str):
        if error in self.error_dict:
            self.error_dict[error] += 1
        else:
            self.error_dict[error] = 1

    @property
    def error_dict(self):
        return self._error_dict

    @error_dict.setter
    def error_dict(self, value):
        self._error_dict = value

    #return author
    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, value):
        self._sender = value

    @property
    def message_id(self):
        return self._message_id

    @message_id.setter
    def message_id(self, value):
        self._message_id = value

    @property
    def annotated_text(self):
        return self._annotated_text
    
    @annotated_text.setter
    def annotated_text(self, value):
        self._annotated_text = value

    @property
    def chat(self):
        self._chat = CacheStore.Instance().get_chat_by_id(self.chat_id)
        return self._chat
    
    @chat.setter
    def chat(self, value):
        self._chat = value

    #TODO: add group functionality 
    def get_recipient(self):
        chat_participants: list = self._chat.participants.copy()
        chat_participants = [p for p in chat_participants if p.id != self._sender.id]

        if len(chat_participants) == 1:
            return chat_participants[0]

        return None
        
        
    

