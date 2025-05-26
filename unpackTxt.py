import re
from classes.message import Message
from classes.chat import Chat
from classes.author import Author
from datetime import datetime

def generate_html_for_author(author, hasOtherMessages=False, filename="output_html/chats.html"):
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chat Export for {author.name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        details {{ margin-bottom: 10px; }}
        summary {{ font-weight: bold; cursor: pointer; }}
        .message-details {{ margin-left: 20px; }}
        .chat-summary {{ font-size: 18px; margin-top: 20px; }}
        .message.own {{ display: block; }}
        .message.other {{ display: none; }}
    </style>
    <script>
        function toggleMessages() {{
            const showAll = document.getElementById("toggleMessages").checked;
            const ownMessages = document.querySelectorAll(".message.own");
            const otherMessages = document.querySelectorAll(".message.other");

            ownMessages.forEach(m => m.style.display = "block");
            otherMessages.forEach(m => m.style.display = showAll ? "block" : "none");
        }}
        window.onload = () => toggleMessages();
    </script>
</head>
<body>
    <h1>Messages by {author.name}</h1>
    <p><strong>Author ID:</strong> {author.author_id}</p>
    <p><strong>Age:</strong> {author.age}</p>
    <p><strong>Gender:</strong> {author.gender}</p>
    <p><strong>Region:</strong> {author.region}</p>
    <p><strong>Job:</strong> {author.job}</p>
    <p><strong>First Language:</strong> {author.first_language}</p>
    <p><strong>Other Languages:</strong> {', '.join(author.languages)}</p>

    <label>
        <input type="checkbox" id="toggleMessages" onchange="toggleMessages()" {'checked' if hasOtherMessages else ''}>
        Show all messages
    </label>
"""

    for chat in author.chats:
        html += f"<details open>\n"
        participants = ", ".join(set(msg.sender for msg in chat.messages))
        html += f"<summary class='chat-summary'>Chat ID: {chat.chat_id} – Participants: {participants} ({len(chat.messages)} messages)</summary>\n"

        for msg in chat.messages:
            message_class = "own" if msg.sender == author.name else "other"
            html += f"<div class='message {message_class}'>\n"
            html += "<details class='message-details'>\n"
            html += f"<summary>Message {msg.message_id} from {msg.sender} at {msg.timestamp}</summary>\n"
            html += "<div style='margin-left: 20px;'>"
            html += f"ChatId: {msg.chat_id}<br>"
            html += f"MessageId: {msg.message_id}<br>"
            html += f"Sender: {msg.sender}<br>"
            html += f"Timestamp: {msg.timestamp}<br>"
            html += f"Content: {msg.content}<br>"
            html += f"MessageType: {msg.message_type}<br>"
            quoted = msg.quoted_message if hasattr(msg, "quoted_message") and msg.quoted_message else "None"
            html += f"Quoted Message: {{ {quoted} }}<br>"
            html += "</div>\n</details>\n</div>\n"

        html += "</details>\n"

    html += """
</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ HTML written to {filename}")






filename = "whatsapp_chat_"
list_of_chats = []
my_author = Author(0, "Reinhold", 30, "Male", "Deutsch", ["English", "Russisch"], "Bayern", "Softwareentwickler")

for i in range(1, 3):

    file_id = i
    print("ich habe file_id: " + str(file_id))
    # Read the file
    with open("texts/" + filename + str(file_id) + ".txt", "r", encoding="utf-8") as file:
        chat_text = file.read()

    # Pattern to match each message
    pattern = r'\[(\d{1,2}:\d{2}), (\d{1,2}\.\d{1,2}\.\d{4})\] ([^:]+): (.*?)((?=\n\[\d{1,2}:\d{2}, \d{1,2}\.\d{1,2}\.\d{4}\])|$)'

    # Find all matches
    matches = re.findall(pattern, chat_text, re.DOTALL)

    chat_id = i
    chat = Chat(chat_id)
    my_author.add_chat(chat)
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


#print(my_author.get_chats_with_own_messages())

generate_html_for_author(my_author)