from classes.chat import Chat
from classes.message import Message
from datetime import datetime

class Author:
    def __init__(self, author_id, name, last_name, age, gender, first_language, languages, region, job):
        self.author_id = author_id
        self.name = name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.first_language = first_language
        self.languages = languages
        self.region = region
        self.job = job
        self.chats = []

    def add_chat(self, chat):
        self.chats.append(chat)

    def __str__(self):
        return (f"Author({self.author_id}): {self.name} {self.last_name}, "
                f"Age: {self.age}, Gender: {self.gender}, "
                f"First Language: {self.first_language}, "
                f"Other Languages: {', '.join(self.languages)}, "
                f"Region: {self.region}, Job: {self.job}")


if __name__ == "__main__":
        author = Author(1, "Reinhold", "Schlager", 30, "Male", "Deutsch", ["Englisch", "Russisch"], "Bayern", "Softwareentwickler")
        print(author)