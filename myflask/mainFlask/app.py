from flask import Flask, render_template
from datetime import datetime, timedelta
import utils
import locale
locale.setlocale(locale.LC_TIME, 'German_Germany.1252') #This is for windows only -> mac/linux: locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

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
