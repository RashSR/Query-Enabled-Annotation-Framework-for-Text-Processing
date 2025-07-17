from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from markupsafe import Markup, escape
from .cachestore import CacheStore
from .search_result import SearchResult
from classes.author import Author
from .routes import blueprints
import re
import locale
import utils
locale.setlocale(locale.LC_TIME, 'German_Germany.1252') #This is for windows only -> mac/linux: locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

#region functions

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
# Register all blueprints
for bp in blueprints:
    print(bp)
    app.register_blueprint(bp)

#SQLite path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # This creates the DB file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#intialize CacheStore
cache = CacheStore.Instance(db, app)

@app.context_processor
def inject_request():
    active_author = utils.get_active_author(session)
    return dict(request=request, active_author=active_author)

@app.route("/search")
def search_view():
    query = request.args.get("query", "").strip()
    sender = request.args.get("sender", "")
    all_messages = utils.get_active_author(session).get_all_messages() #TODO: only messages from selected author?
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
        query=query, author=utils.get_active_author(session)
    )

#TODO: HTML wird nur generiert wonach auch gesucht wird? CSS ein und ausschalten?

#TODO:
# überprüfen lohnt es sich alles mit spacy zu analysieren und jedes einzelen Wort danach noch in Language tool zu packen? bzw anders rum mit langauge tool und falls Fehler -> nicht in spacy 
# Nur Wert in Dropdown anzeigen die es gibt? 
# Wie bei CompOV linke und rechte seite auswählbar


#TODO: Maybe add a performance analysis at the end python vs DB call. Is the DB in some ways faster even with the overhead to make the SQL call