from datetime import datetime
from classes.messagetype import MessageType
from typing import Dict

class Message:
    
    #TODO: sender hier notwendig? -> Nur wenn nach einzelnen Nachrichten gesucht werden muss. 

    def __init__(self, chat_id, message_id, sender, timestamp, content, message_type = MessageType.TEXT, quoted_message = None, error_dict : Dict[str, int] = None, annotated_text = None):
        self.chat_id = chat_id
        self._message_id = message_id
        self.sender = sender
        self.timestamp = timestamp
        self.content = content
        self.message_type = message_type
        self.quoted_message = quoted_message
        self._error_dict = {}
        self._annotated_text = annotated_text

    def __str__(self):
        toString = f"""ChatId: {self.chat_id}, MessageId: {str(self._message_id)}
        Sender: {self.sender}
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
        self.annotated_text = value

    

