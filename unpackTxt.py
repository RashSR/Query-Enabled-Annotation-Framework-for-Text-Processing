import re
from classes.message import Message
from classes.chat import Chat
from datetime import datetime

# Read the file
with open("texts/whatsapp_chat.txt", "r", encoding="utf-8") as file:
    chat_text = file.read()

# Pattern to match each message
pattern = r'\[(\d{1,2}:\d{2}), (\d{1,2}\.\d{1,2}\.\d{4})\] ([^:]+): (.*?)((?=\n\[\d{1,2}:\d{2}, \d{1,2}\.\d{1,2}\.\d{4}\])|$)'

# Find all matches
matches = re.findall(pattern, chat_text, re.DOTALL)

chat_id = 1
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

#chat_id, message_id, sender, timestamp, content, message_type, quoted_message = None