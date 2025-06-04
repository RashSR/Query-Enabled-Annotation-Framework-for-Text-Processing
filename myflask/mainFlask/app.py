from flask import Flask, render_template
from classes.chat import Chat
from classes.message import Message
from datetime import datetime, timedelta
import utils

app = Flask(__name__)
app.jinja_env.globals.update(now=datetime.now, timedelta=timedelta)

chats = utils.load_all_chats_from_files([1, 2])

@app.route("/")
def index():
    return render_template("chat.html", chats=chats, chat=chats[0], current_user="Reinhold")

@app.route("/chat/<int:chat_id>")
def chat_view(chat_id):
    chat = next((c for c in chats if c.chat_id == chat_id), chats[0])
    return render_template("chat.html", chats=chats, chat=chat, current_user="Reinhold")

if __name__ == "__main__":
    app.run(debug=True)
