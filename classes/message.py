from datetime import datetime
from classes.messagetype import MessageType

class Message:
    
    #TODO: sender hier notwendig? -> Nur wenn nach einzelnen Nachrichten gesucht werden muss. 

    def __init__(self, chat_id, message_id, sender, timestamp, content, message_type = MessageType.TEXT, quoted_message = None):
        self.chat_id = chat_id
        self.message_id = message_id
        self.sender = sender
        self.timestamp = timestamp
        self.content = content
        self.message_type = message_type
        self.quoted_message = quoted_message

    def __str__(self):
        toString = f"""ChatId: {self.chat_id}, MessageId: {str(self.message_id)}
        Sender: {self.sender}
        Timestamp: {self.timestamp}
        Content: {self.content}
        MessageType: {self.message_type}
        quotedMessage: {{ {self.quoted_message } }}
        """
        return toString
    
    def hasQuote(self):
        if self.quoted_message == None:
            return True
        return False
    
    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, value):
        self._sender = value
    

