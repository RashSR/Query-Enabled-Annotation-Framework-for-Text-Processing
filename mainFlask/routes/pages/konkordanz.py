from flask import Blueprint, render_template, session, request
from mainFlask.filter_node_object import FilterNodeObejct
from mainFlask.filter_type import FilterType
from mainFlask.settings import Settings
import utils

konkordanz_bp = Blueprint('konkordanz', __name__)

#TODO: the jump dont highlight case sensitiv, keyword gets multiple highlights
#maybe like in strg+shift+f VS Code with that icons 
#wenn teilstring gefunden wird -> in Hit sollte das gefundene Wort stehen, aber der gefundene wort gehíghlighted werden
#Dem Nutzer die Möglichkeit geben ob er e.g. Fehler in einer Nachricht suchen mag oder direktes Wort oder Nachfolger/Vorgänger
#check if a author is selected -> show nothing if not
@konkordanz_bp.route("/konkordanz")
def konkordanz_view():

    settings = Settings.Instance()
    
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
        fno.selected_color = settings.highlight_colors[i]
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