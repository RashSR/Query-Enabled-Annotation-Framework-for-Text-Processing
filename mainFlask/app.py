from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from markupsafe import Markup, escape
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3
from .data.cachestore import CacheStore
from .routes import blueprints
import re
import locale
import utils
locale.setlocale(locale.LC_TIME, 'German_Germany.1252') #This is for windows only -> mac/linux: locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

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

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

#intialize CacheStore
CacheStore.Instance(db, app)

@app.context_processor
def inject_active_author():
    from flask import session
    import utils
    return {'active_author': utils.get_active_author(session)}

@app.route('/')
def landing_redirect():
    return redirect('/profile')

@app.route("/search")
def search_view():
    query = request.args.get("query", "").strip()
    sender = request.args.get("sender", "")
    all_messages = CacheStore.Instance().get_all_messages()
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