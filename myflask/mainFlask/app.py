from flask import Flask, render_template
from classes.chat import Chat
from classes.message import Message
from classes.messagetype import MessageType
from datetime import datetime

app = Flask(__name__)

# Create some chats
chat1 = Chat(chat_id=1)
chat1.add_message(Message(1, 1, "Alice", datetime.now(), "Hello!"))
chat1.add_message(Message(1, 2, "Bob", datetime.now(), "Hi Alice!", quoted_message="Hello!"))

chat2 = Chat(chat_id=2)
chat2.add_message(Message(2, 1, "Charlie", datetime.now(), "Hey there"))

chats = [chat1, chat2]

@app.route("/")
def index():
    return render_template("chat.html", chats=chats, chat=chat1, current_user="Bob")

@app.route("/chat/<int:chat_id>")
def chat_view(chat_id):
    chat = next((c for c in chats if c.chat_id == chat_id), chats[0])
    return render_template("chat.html", chats=chats, chat=chat, current_user="Bob")

if __name__ == "__main__":
    app.run(debug=True)
