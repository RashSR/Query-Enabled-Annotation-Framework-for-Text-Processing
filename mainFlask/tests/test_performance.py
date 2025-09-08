import time
import pytest
import utils
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from mainFlask.data.cachestore import CacheStore
from mainFlask.classes.author import Author
from mainFlask.classes.chat import Chat
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO, force=True)

@pytest.fixture
def establish_db_connection():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    CacheStore.Instance(db, app)

    with app.app_context():
        yield db
        #This code runs after test execution
        db.session.execute(text("DELETE FROM chat"))
        db.session.execute(text("DELETE FROM message"))
        db.session.commit()

def test_loading_messages_from_file():
    start = time.perf_counter()
    file_path = Path(__file__).parent / "instance" / "test_messages.txt"

    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
        messages = utils.get_messages_from_text(file_content)

    duration = time.perf_counter() - start
    msgs_per_sec = len(messages) / duration

    # Write results to a file
    results_file = Path(__file__).parent / "performance_results.txt"
    with open(results_file, "a", encoding="utf-8") as f:
        f.write(
            f"Processed {len(messages)} messages in {duration:.6f}s "
            f"({msgs_per_sec:.0f} msgs/sec)\n"
        )

    # Keep the test passing
    assert len(messages) > 0

def test_loading_and_persisting_messages(establish_db_connection):
    start = time.perf_counter()
    
    file_path = Path(__file__).parent / "instance" / "test_messages.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
        messages = utils.get_messages_from_text(file_content)
        author = Author(70, 'Esther')
        chat = Chat(None)
        creatd_chat = CacheStore.Instance().create_chat(chat)
        for msg in messages:
            msg.chat_id = creatd_chat.chat_id
            msg.sender = author
        CacheStore.Instance().create_messages(messages)

    duration = time.perf_counter() - start
    msgs_per_sec = len(messages) / duration

    # Write results to a file
    results_file = Path(__file__).parent / "performance_results.txt"
    with open(results_file, "a", encoding="utf-8") as f:
        f.write(
            f"Processed {len(messages)} messages in {duration:.2f}s "
            f"({msgs_per_sec:.0f} msgs/sec)\n"
        )

    assert len(messages) > 0

def test_loading_and_persisting_and_analyzing_messages(establish_db_connection):
    start = time.perf_counter()
    
    file_path = Path(__file__).parent / "instance" / "test_messages.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
        messages = utils.get_messages_from_text(file_content)
        author = Author(70, 'Esther')
        chat = Chat(None)
        creatd_chat = CacheStore.Instance().create_chat(chat)
        for msg in messages:
            msg.chat_id = creatd_chat.chat_id
            msg.sender = author
        CacheStore.Instance().create_messages(messages)

    duration = time.perf_counter() - start
    msgs_per_sec = len(messages) / duration

    # Write results to a file
    results_file = Path(__file__).parent / "performance_results.txt"
    with open(results_file, "a", encoding="utf-8") as f:
        f.write(
            f"Processed {len(messages)} messages in {duration:.2f}s "
            f"({msgs_per_sec:.0f} msgs/sec)\n"
        )

    assert len(messages) > 0
