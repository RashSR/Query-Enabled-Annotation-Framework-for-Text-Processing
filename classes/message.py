from datetime import datetime

class Message:
    
    #TODO: sender hier notwendig? -> Nur wenn nach einzelnen Nachrichten gesucht werden muss. 

    def __init__(self, chat_id, message_id, sender, timestamp, content, message_type = "TEXT", quoted_message = None):
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

if __name__ == "__main__":
    msg_without_quote = Message(6, 1, 'Alice',  datetime.now(),"Hello what up", "Text")
    print(msg_without_quote)
    quote = Message(7, 1, 'Ute', datetime.now(), "Do you want to go outside?", "Text")
    msg_with_quote = Message(7, 2, 'Bob', datetime.now(), "This sounds awesome!", "Text", quote)
    print(msg_with_quote)

    print(f"Has msg1 a quote? -> {msg_without_quote.hasQuote()}")
    print(f"Has msg2 a quote? -> {msg_with_quote.hasQuote()}")
    

