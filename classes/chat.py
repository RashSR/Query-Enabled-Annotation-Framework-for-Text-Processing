from message import Message
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

if __name__ == "__main__":
    chat = Chat(6)

    msg1 = Message(6, 1, 'Alice',  datetime.now(),"Hello what up", "Text")
    msg2 = Message(6, 2, 'Alice', datetime.now(), "Do you want to go outside?", "Text")
    msg3 = Message(6, 3, 'Bob', datetime.now(), "This sounds awesome!", "Text")

    chat.add_message(msg1)
    chat.add_message(msg2)
    chat.add_message(msg3)

    chat.show_messages()
    