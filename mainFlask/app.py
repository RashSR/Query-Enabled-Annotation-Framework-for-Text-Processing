from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from markupsafe import Markup, escape
from mainFlask.cachestore import CacheStore
from mainFlask.search_result import SearchResult
from classes.author import Author
from mainFlask.filter_node_object import FilterNodeObejct
from mainFlask.filter_type import FilterType
from mainFlask.routes import blueprints
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

#TODO: the jump dont highlight case sensitiv, keyword gets multiple highlights
#maybe like in strg+shift+f VS Code with that icons 
#wenn teilstring gefunden wird -> in Hit sollte das gefundene Wort stehen, aber der gefundene wort gehíghlighted werden
#Dem Nutzer die Möglichkeit geben ob er e.g. Fehler in einer Nachricht suchen mag oder direktes Wort oder Nachfolger/Vorgänger
#check if a author is selected -> show nothing if not
@app.route("/konkordanz")
def konkordanz_view():
    
    #All messages should be anlyzed when entering this view
    author = utils.get_active_author(session)
    author.analyze_all_own_messages()

    keyword = None

    # total bars == how many keyword[i] you received
    total = len([k for k in request.args if k.startswith('selected_type[')])
    
    fno_list: list[FilterNodeObejct] = []
    results = []

    for i in range(total):
        kw   = request.args.get(f'keyword[{i}]', '')
        typ  = request.args.get(f'selected_type[{i}]')
        scp  = request.args.get(f'selected_scope[{i}]')
        color = request.args.get(f'selected_color[{i}]')
        
        cs = bool(request.args.get(f'case_sensitive[{i}]'))
        ww = bool(request.args.get(f'whole_word[{i}]'))
        rg = bool(request.args.get(f'use_regex[{i}]'))
        
        
        fno = FilterNodeObejct(FilterType(typ), kw, scp, cs, ww, rg)
        fno.selected_color = color
        fno.scope_choices = FilterNodeObejct.get_values(fno.filter_type, author) #is needed to keep the selected value
        fno_list.append(fno)

        keyword = kw
        
    #hier wurden werte gesetzt all fno results zusammen packen
    for fnObject in fno_list:
        search_results_from_fno = fnObject.get_result(author)
        results.extend(search_results_from_fno)

    return render_template(
        "konkordanz.html",
        results=results,
        keyword=keyword,
        filter_types=FilterType,
        nodes = fno_list
    )

#TODO: HTML wird nur generiert wonach auch gesucht wird? CSS ein und ausschalten?

#TODO:
# überprüfen lohnt es sich alles mit spacy zu analysieren und jedes einzelen Wort danach noch in Language tool zu packen? bzw anders rum mit langauge tool und falls Fehler -> nicht in spacy 
# Nur Wert in Dropdown anzeigen die es gibt? 
# Wie bei CompOV linke und rechte seite auswählbar


#TODO: Maybe add a performance analysis at the end python vs DB call. Is the DB in some ways faster even with the overhead to make the SQL call

#TODO: if hit is very long -> link sitzt in right context