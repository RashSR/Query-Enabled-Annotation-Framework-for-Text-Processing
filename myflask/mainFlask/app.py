from flask import Flask, render_template, request
from datetime import datetime, timedelta
from classes.author import Author
from markupsafe import Markup, escape
import re
import utils
import locale
locale.setlocale(locale.LC_TIME, 'German_Germany.1252') #This is for windows only -> mac/linux: locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

app = Flask(__name__)
app.jinja_env.globals.update(now=datetime.now, timedelta=timedelta)

chats = utils.load_all_chats_from_files([3])
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
    query = request.args.get("query", "").strip()
    sender = request.args.get("sender", "")
    all_messages = chats[0].messages
    all_senders = sorted(set(msg.sender for msg in all_messages))
    results = []

    if query:
        pattern = re.compile(re.escape(query), re.IGNORECASE)

        for msg in all_messages:
            if pattern.search(msg.content):
                if not sender or msg.sender == sender:
                    highlighted = pattern.sub(
                        lambda m: f'<span class="highlight">{escape(m.group(0))}</span>',
                        escape(msg.content)
                    )
                    msg.highlighted_content = Markup(highlighted)  # Safe HTML
                    results.append(msg)

    return render_template(
        "search.html",
        results=results if query else None,
        all_senders=all_senders,
        selected_sender=sender,
        query=query, current_user="Reinhold"
    )


@app.route("/metrics")
def metrics_view():
    return render_template('metrics.html')

@app.route("/settings")
def settings_view():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True)
