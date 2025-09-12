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
        CacheStore.Instance().empty_database()

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

def test_loop(establish_db_connection):
    for i in range(8):
        test_loading_and_persisting_and_analyzing_messages_with_spacy(establish_db_connection)
 
def test_loading_and_persisting_and_analyzing_messages_with_spacy(establish_db_connection):
    overall_start = time.perf_counter()

    # Load messages
    file_path = Path(__file__).parent / "instance" / "test_messages.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
    messages = utils.get_messages_from_text(file_content)

    author = Author(70, 'Esther')
    chat = Chat(None)
    created_chat = CacheStore.Instance().create_chat(chat)
    for msg in messages:
        msg.chat_id = created_chat.chat_id
        msg.sender = author

    # Persist messages
    start_persist = time.perf_counter()
    CacheStore.Instance().create_messages(messages)
    persist_duration = time.perf_counter() - start_persist

    # spaCy analysis
    start_spacy = time.perf_counter()
    for msg in messages:
        utils.analyze_msg_with_spacy(msg)
    spacy_duration = time.perf_counter() - start_spacy

    # Total duration
    total_duration = time.perf_counter() - overall_start

    # Throughput calculations
    persist_throughput = len(messages) / persist_duration
    spacy_throughput = len(messages) / spacy_duration
    total_throughput = len(messages) / total_duration

    # Write results to file
    results_file = Path(__file__).parent / "performance_results.txt"
    with open(results_file, "a", encoding="utf-8") as f:
        f.write(
            f"Persisted {len(messages)} messages in {persist_duration:.2f}s "
            f"({persist_throughput:.0f} msgs/sec)\n"
            f"spaCy analyzed {len(messages)} messages in {spacy_duration:.2f}s "
            f"({spacy_throughput:.0f} msgs/sec)\n"
            f"TOTAL: {len(messages)} messages in {total_duration:.2f}s "
            f"({total_throughput:.0f} msgs/sec)\n\n"
        )

    CacheStore.Instance().empty_database()
    CacheStore.Instance().empty_cache()
    assert len(messages) > 0


def test_loading_and_persisting_and_analyzing_messages_with_language_tool(establish_db_connection):
    overall_start = time.perf_counter()

    # Load messages
    file_path = Path(__file__).parent / "instance" / "test_messages.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
    messages = utils.get_messages_from_text(file_content)

    author = Author(70, 'Esther')
    chat = Chat(None)
    created_chat = CacheStore.Instance().create_chat(chat)
    for msg in messages:
        msg.chat_id = created_chat.chat_id
        msg.sender = author

    # Persist messages
    start_persist = time.perf_counter()
    CacheStore.Instance().create_messages(messages)
    persist_duration = time.perf_counter() - start_persist

    # LanguageTool analysis
    start_lang = time.perf_counter()
    for msg in messages:
        utils.analyze_msg_with_language_tool(msg)
    lang_duration = time.perf_counter() - start_lang

    # Total duration
    total_duration = time.perf_counter() - overall_start

    # Throughput calculations
    persist_throughput = len(messages) / persist_duration
    lang_throughput = len(messages) / lang_duration
    total_throughput = len(messages) / total_duration

    # Write results to file
    results_file = Path(__file__).parent / "performance_results.txt"
    with open(results_file, "a", encoding="utf-8") as f:
        f.write(
            f"Persisted {len(messages)} messages in {persist_duration:.2f}s "
            f"({persist_throughput:.0f} msgs/sec)\n"
            f"LanguageTool analyzed {len(messages)} messages in {lang_duration:.2f}s "
            f"({lang_throughput:.0f} msgs/sec)\n"
            f"TOTAL: {len(messages)} messages in {total_duration:.2f}s "
            f"({total_throughput:.0f} msgs/sec)\n\n"
        )

    CacheStore.Instance().empty_database()
    CacheStore.Instance().empty_cache()
    assert len(messages) > 0