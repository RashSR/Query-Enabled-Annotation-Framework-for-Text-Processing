from flask import Flask, render_template
from classes.chat import Chat
from classes.message import Message
from datetime import datetime, timedelta
import utils

app = Flask(__name__)
app.jinja_env.globals.update(now=datetime.now, timedelta=timedelta)

# Create some chats
chat1 = Chat(chat_id=1)
chat1.add_message(Message(1, 1, "Alice", datetime.now(), "Hello!"))
chat1.add_message(Message(1, 2, "Bob", datetime.now(), "Hi Alice!", quoted_message="Hello!"))

chat2 = Chat(chat_id=2)
chat2.add_message(Message(2, 1, "Charlie", datetime.now(), "Hey there"))

loaded_chat_1 = utils.load_single_chat_from_file(1)
loaded_chat_2 = utils.load_single_chat_from_file(2)

chats = [loaded_chat_1, loaded_chat_2]

@app.route("/")
def index():
    return render_template("chat.html", chats=chats, chat=chat1, current_user="Reinhold")

@app.route("/chat/<int:chat_id>")
def chat_view(chat_id):
    chat = next((c for c in chats if c.chat_id == chat_id), chats[0])
    return render_template("chat.html", chats=chats, chat=chat, current_user="Reinhold")

if __name__ == "__main__":
    app.run(debug=True)
