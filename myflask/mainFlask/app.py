from flask import Flask, render_template, request
from datetime import datetime, timedelta
from classes.author import Author
import utils
import locale
locale.setlocale(locale.LC_TIME, 'German_Germany.1252') #This is for windows only -> mac/linux: locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

app = Flask(__name__)
app.jinja_env.globals.update(now=datetime.now, timedelta=timedelta)

chats = utils.load_all_chats_from_files([0], True)
#chats = utils.load_all_chats_from_files([1, 2, 3], True)
author = Author(0, "Reinhold", 30, "Male", "Deutsch", ["English", "Russisch"], "Bayern", "Softwareentwickler")
author.add_chat(chats[0])
#author.add_chat(chats[1])
#author.add_chat(chats[2])

@app.context_processor
def inject_request():
    return dict(request=request)

@app.route("/profile")
def profile():
    return render_template("profile.html", author=author)

@app.route('/chat')
def chat_home():
    return render_template('chat.html', chats=chats, chat=None, current_user="Reinhold")

@app.route("/chat/<int:chat_id>")
def chat_view(chat_id):
    chat = next((c for c in chats if c.chat_id == chat_id), chats[0])
    return render_template("chat.html", chats=chats, chat=chat, current_user="Reinhold")

@app.route("/search")
def search_view():
    return render_template('search.html')

@app.route("/metrics")
def metrics_view():
    return render_template('metrics.html')

@app.route("/settings")
def settings_view():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True)
