from flask import Flask, render_template, request, abort, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from markupsafe import Markup, escape
from myflask.mainFlask.cachestore import CacheStore
from myflask.mainFlask.search_result import SearchResult
from classes.author import Author
import re
import locale
locale.setlocale(locale.LC_TIME, 'German_Germany.1252') #This is for windows only -> mac/linux: locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

#region functions

# Store author_id in the session
def set_active_author(session, author_id):
    session['author_id'] = author_id

# get stored author
def get_active_author(session):
    return CacheStore.Instance().get_author_by_id(session.get('author_id'))

#TODO: more than only author messages? maybe optional?
def get_keyword_hits(active_author: Author, keyword: str, case_sensitive: bool):
    hit_results = []

    if not case_sensitive:
        keyword = keyword.lower()

    for msg in active_author.get_all_own_messages():
        content = msg.content if case_sensitive else msg.content.lower()
        if keyword in content:
            hit_results.append(SearchResult(msg, keyword, case_sensitive))

    return hit_results

# endregion 

#Start application
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.jinja_env.globals.update(now=datetime.now, timedelta=timedelta)

#SQLite path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # This creates the DB file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#intialize CacheStore
cache = CacheStore.Instance(db, app)

@app.context_processor
def inject_request():
    active_author = get_active_author(session)
    return dict(request=request, active_author=active_author)

@app.route("/profile")
def profile():
    all_authors = CacheStore.Instance().get_all_authors()
    return render_template("profile.html", author=get_active_author(session), authors=all_authors)

@app.route("/profile/<int:author_id>")
def author_profile(author_id):

    all_authors = CacheStore.Instance().get_all_authors()
    selected_author = CacheStore.Instance().get_author_by_id(author_id)
    if not selected_author:
        # Handle not found, e.g. 404 or redirect
        abort(404)
    if not request.args.get('no_active_change'):
        
        set_active_author(session, author_id)
        selected_author = get_active_author(session)

    return render_template("profile.html", author=selected_author, authors=all_authors)

#TODO: improvement in the future -> only load needed information and not all chats
@app.route('/chat')
def chat_home():
    return render_template('chat.html', chat=None, author=get_active_author(session))

beziehung = ["guter Freund", "rein geschäftlich", "lose Bekannte"] #TODO: das muss in DB

#TODO: improvement in the future -> only load needed chat 
@app.route("/chat/<int:chat_id>")
def chat_view(chat_id):
    keyword = request.args.get("keyword")
    author = get_active_author(session)
    chat = author.get_chat_by_id(chat_id)
    return render_template("chat.html", chat=chat, beziehung=beziehung, author=author, keyword=keyword)

@app.route("/search")
def search_view():
    query = request.args.get("query", "").strip()
    sender = request.args.get("sender", "")
    all_messages = get_active_author(session).get_all_messages() #TODO: only messages from selected author?
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
        query=query, author=get_active_author(session)
    )

#TODO: fix that keyword is correct in the hit list, the jump dont highlight case sensitiv, keyword gets multiple highlights
@app.route("/konkordanz")
def konkordanz_view():
    keyword = request.args.get('keyword', '').strip()
    case_sensitive = request.args.get('case_sensitive') == '1'
    results = []
    if keyword:
        # Example search logic: You'd normally process your text corpus here
        results = get_keyword_hits(get_active_author(session), keyword, case_sensitive)
    return render_template("konkordanz.html", results=results, keyword=keyword, case_sensitive=case_sensitive)

@app.route("/metrics")
def metrics_view():
    return render_template('metrics.html')

@app.route("/settings")
def settings_view():
    return render_template("settings.html")

if __name__ == "__main__":
    app.run(debug=True)
