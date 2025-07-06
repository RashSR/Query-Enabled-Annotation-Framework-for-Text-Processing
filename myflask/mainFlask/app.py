from flask import Flask, render_template, request, abort, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from markupsafe import Markup, escape
from myflask.mainFlask.cachestore import CacheStore
from myflask.mainFlask.search_result import SearchResult
from classes.author import Author
from classes.message import Message
from classes.chat import Chat
from classes.messagetype import MessageType
from myflask.mainFlask.ltmatch import LTMatch
import utils
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

#TODO: improvement in the future -> only load needed chat 
@app.route("/chat/<int:chat_id>")
def chat_view(chat_id):
    keyword = request.args.get("keyword")
    author = get_active_author(session)
    chat = author.get_chat_by_id(chat_id)
    return render_template("chat.html", chat=chat, author=author, keyword=keyword)

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

#TODO: the jump dont highlight case sensitiv, keyword gets multiple highlights
#maybe like in strg+shift+f VS Code with that icons 
#wenn teilstring gefunden wird -> in Hit sollte das gefundene Wort stehen, aber der gefundene wort gehíghlighted werden
#Dem Nutzer die Möglichkeit geben ob er e.g. Fehler in einer Nachricht suchen mag oder direktes Wort oder Nachfolger/Vorgänger
@app.route("/konkordanz")
def konkordanz_view():
    keyword = request.args.get('keyword', '').strip()
    selected_type = request.args.get('selected_type')
    case_sensitive = request.args.get('case_sensitive') == '1'
    whole_word = request.args.get('whole_word') == '1'
    use_regex = request.args.get('use_regex') == '1'

    author = get_active_author(session)
    author.analyze_all_own_messages()
    errors = author.get_error_categories()

    if selected_type is not None:
        found_msgs = author.get_messages_by_error_category(selected_type)
        for msg in found_msgs:
            print(msg)
            for ltm in msg.error_list:
                print(ltm)


    results = []
    if keyword:
        
        all_msgs = author.get_all_own_messages()

        for msg in all_msgs:
            original_content = msg.content
            content = original_content if case_sensitive else original_content.lower()
            query = keyword if case_sensitive else keyword.lower()

            matches = []

            if use_regex:
                try:
                    pattern = re.compile(query) if case_sensitive else re.compile(query, re.IGNORECASE)
                    matches = pattern.finditer(original_content)
                except re.error:
                    pass  # optionally handle error
            elif whole_word:
                flags = 0 if case_sensitive else re.IGNORECASE
                pattern = re.compile(r'\b{}\b'.format(re.escape(query)), flags)
                matches = pattern.finditer(original_content)
            else:
                # Not regex, not whole word: simple substring
                index = content.find(query)
                if index != -1:
                    matches = [re.Match]  # dummy placeholder
                    matched_word = original_content[index:index+len(keyword)]
                    results.append(SearchResult(msg, keyword, matched_word))
                    continue

            for match in matches:
                matched_word = match.group()
                results.append(SearchResult(msg, keyword, matched_word))

    return render_template(
        "konkordanz.html",
        results=results,
        keyword=keyword,
        case_sensitive=case_sensitive,
        whole_word=whole_word,
        use_regex=use_regex,
        errors=errors
    )

#TODO: HTML wird nur generiert wonach auch gesucht wird? CSS ein und ausschalten?

@app.route("/metrics")
def metrics_view():
    aut1 = Author(7, "Max")
    aut2 = Author(9, "Felix")
    new_message = Message(5, 1, aut1, datetime.now(), "Das hier ist ein TestText mit kl FEhler. Was machst du jtdsd?!", MessageType.TEXT)
    second_message = Message(5, 2, aut2, datetime.now(), "dd  dasds Wasd WarUm isst er hier das Budget..", MessageType.TEXT)

    new_chat = Chat(5)
    new_chat.add_message(new_message)
    new_chat.add_message(second_message)
    
    #utils.analyze_msg_with_spacy(new_message)
    return render_template('metrics.html')

#TODO:
# überprüfen lohnt es sich alles mit spacy zu analysieren und jedes einzelen Wort danach noch in Language tool zu packen? bzw anders rum mit langauge tool und falls Fehler -> nicht in spacy 
# Nur Wert in Dropdown anzeigen die es gibt? 
# Wie bei CompOV linke und rechte seite auswählbar

@app.route("/settings")
def settings_view():
    my_ltm = LTMatch(81, 3, 0, 4, 'hihi', 'TestCat', 'TestRule')
    print(my_ltm)
    created_ltm = CacheStore.Instance().create_lt_match(my_ltm)
    print(created_ltm)
    return render_template("settings.html")

#TODO: Maybe add a performance analysis at the end python vs DB call. Is the DB in some ways faster even with the overhead to make the SQL call