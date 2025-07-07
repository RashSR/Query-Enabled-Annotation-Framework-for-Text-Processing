from flask import Blueprint, render_template, session, request
import utils

chat_bp = Blueprint('chat', __name__)

#TODO: improvement in the future -> only load needed information and not all chats
@chat_bp.route('/chat')
def chat_home():
    return render_template('chat.html', chat=None, author=utils.get_active_author(session))

#TODO: improvement in the future -> only load needed chat 
@chat_bp.route("/chat/<int:chat_id>")
def chat_view(chat_id):
    keyword = request.args.get("keyword")
    author = utils.get_active_author(session)
    chat = author.get_chat_by_id(chat_id)
    return render_template("chat.html", chat=chat, author=author, keyword=keyword)