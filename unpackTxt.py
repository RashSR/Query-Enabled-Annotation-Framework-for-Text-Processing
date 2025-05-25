import re
from classes.message import Message
from classes.chat import Chat
from classes.author import Author
from datetime import datetime

def generate_html(chats, filename="output_html/chats.html"):
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chat Export</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        details { margin-bottom: 10px; }
        summary { font-weight: bold; cursor: pointer; }
        .message-details { margin-left: 20px; }
        .chat-summary { font-size: 18px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Chat Export</h1>
"""

    for chat in chats:
        html += f"<details open>\n"
        html += f"<summary class='chat-summary'>Chat ID: {chat.chat_id} – Participants: {chat.participants} ({len(chat.messages)} messages)</summary>\n"
        
        for msg in chat.messages:
            html += "<details class='message-details'>\n"
            html += f"<summary>Message {msg.message_id} from {msg.sender} at {msg.timestamp}</summary>\n"
            html += "<div style='margin-left: 20px;'>"
            html += f"ChatId: {msg.chat_id}<br>"
            html += f"MessageId: {msg.message_id}<br>"
            html += f"Sender: {msg.sender}<br>"
            html += f"Timestamp: {msg.timestamp}<br>"
            html += f"Content: {msg.content}<br>"
            html += f"MessageType: {msg.message_type}<br>"
            quoted = msg.quoted_message if hasattr(msg, "quoted_message") else "None"
            html += f"Quoted Message: {{ {quoted} }}<br>"
            html += "</div>\n</details>\n"

        html += "</details>\n"

    html += """
</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML written to {filename}")






# Read the file
with open("texts/whatsapp_chat.txt", "r", encoding="utf-8") as file:
    chat_text = file.read()

# Pattern to match each message
pattern = r'\[(\d{1,2}:\d{2}), (\d{1,2}\.\d{1,2}\.\d{4})\] ([^:]+): (.*?)((?=\n\[\d{1,2}:\d{2}, \d{1,2}\.\d{1,2}\.\d{4}\])|$)'

# Find all matches
matches = re.findall(pattern, chat_text, re.DOTALL)

chat_id = 0
chat = Chat(chat_id)
msg_id = 0

# Iterate and print each message
for time, date, sender, message, _ in matches:
    str_date = date + " " + time
    date_obj = datetime.strptime(str_date, "%d.%m.%Y %H:%M")
    msg = Message(chat_id, msg_id, sender, date_obj, message.strip())
    chat.add_message(msg)
    msg_id = msg_id + 1
    print(msg)

print(f"Der Chat besteht aus folgenden Teilnehmern: {chat.participants}")

author_id = 0
authors = []
for author in chat.participants:
    singleAuthor = Author(author_id, author)
    author_id = author_id + 1
    authors.append(singleAuthor)

for a in authors:
    print(a)

generate_html([chat])