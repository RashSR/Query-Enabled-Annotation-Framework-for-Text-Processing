from flask import Flask, render_template, request, abort, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from markupsafe import Markup, escape
from myflask.mainFlask.db_handling import get_authors
import re
import utils
import locale
locale.setlocale(locale.LC_TIME, 'German_Germany.1252') #This is for windows only -> mac/linux: locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

# Store author_id in the session
def set_active_author(session, author_id):
    session['author_id'] = author_id

# get stored author
def get_active_author(session, authors: list):
    return next((a for a in authors if a.author_id == session.get('author_id')), None)

#Start application
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.jinja_env.globals.update(now=datetime.now, timedelta=timedelta)

#SQLite path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # This creates the DB file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

all_authors = get_authors(db, app)

author = all_authors[0]
chats = author.chats
#chats = utils.load_all_chats_from_files([0], True)
#chats = utils.load_all_chats_from_files([1, 2, 3], False)
#author.add_chat(chats[0])
#author.add_chat(chats[1])
#author.add_chat(chats[2])

@app.context_processor
def inject_request():
    return dict(request=request)

@app.route("/profile")
def profile():
    return render_template("profile.html", author=get_active_author(session, all_authors), authors=all_authors)

@app.route("/profile/<int:author_id>")
def author_profile(author_id):
    # Assuming authors is a list or query you have somewhere
    selected_author = next((a for a in all_authors if a.author_id == author_id), None)
    if not selected_author:
        # Handle not found, e.g. 404 or redirect
        abort(404)

    set_active_author(session, author_id)
    return render_template("profile.html", author=get_active_author(session, all_authors), authors=all_authors)


@app.route('/chat')
def chat_home():
    return render_template('chat.html', chat=None, author=get_active_author(session, all_authors))

beziehung = ["guter Freund", "rein geschäftlich", "lose Bekannte"]

@app.route("/chat/<int:chat_id>")
def chat_view(chat_id):
    chat = next((c for c in chats if c.chat_id == chat_id), chats[0])
    return render_template("chat.html", chat=chat, beziehung=beziehung, author=get_active_author(session, all_authors))

@app.route("/search")
def search_view():
    query = request.args.get("query", "").strip()
    sender = request.args.get("sender", "")
    all_messages = author.get_all_messages()
    all_senders = sorted(set(msg.sender.name for msg in all_messages))
    results = []

    if query:
        pattern = re.compile(re.escape(query), re.IGNORECASE)

        for msg in all_messages:
            if pattern.search(msg.content):
                if not sender or msg.sender.name == sender:
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
        query=query, author=author
    )

@app.route("/konkordanz")
def konkordanz_view():
    return render_template('konkordanz.html')

@app.route("/metrics")
def metrics_view():
    return render_template('metrics.html')

@app.route("/settings")
def settings_view():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True)
