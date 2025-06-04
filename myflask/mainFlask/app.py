from flask import Flask, render_template
from classes.message import Message
from classes.chat import Chat
from classes.messagetype import MessageType
from datetime import datetime
from flask import Flask, render_template
import utils

app = Flask(__name__)

# Create example chat with your existing classes
chat = Chat(chat_id=1)
chat.add_message(Message(
    chat_id=1,
    message_id=1,
    sender="Alice",
    timestamp=datetime(2024, 6, 4, 10, 1),
    content="Hey! How are you?",
    message_type=MessageType.TEXT
))
chat.add_message(Message(
    chat_id=1,
    message_id=2,
    sender="Bob",
    timestamp=datetime(2024, 6, 4, 10, 2),
    content="I'm good, and you?",
    message_type=MessageType.TEXT
))
chat.add_message(Message(
    chat_id=1,
    message_id=3,
    sender="Alice",
    timestamp=datetime(2024, 6, 4, 10, 3),
    content="Doing great. Wanna catch up later?",
    message_type=MessageType.TEXT,
    quoted_message="I'm good, and you?"
))

loaded_chat = utils.load_single_chat_from_file(1)

@app.route("/chat")
def chat_view():
    return render_template("chat.html", chat=chat, current_user="Bob")


@app.route("/chat2")
def chat2_view():
    return render_template("chat.html", chat=chat, current_user="Alice")

@app.route("/")
def chat3_view():
    return render_template("chat.html", chat=loaded_chat, current_user=loaded_chat.participants[0])