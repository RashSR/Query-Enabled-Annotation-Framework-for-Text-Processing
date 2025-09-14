import time
import pytest
import utils
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from mainFlask.data.cachestore import CacheStore
from mainFlask.classes.author import Author
from mainFlask.classes.chat import Chat
from mainFlask.classes.message import Message
from mainFlask.classes.filter_node_object import FilterNodeObject
from mainFlask.classes.filter_node_group import FilterNodeGroup
from mainFlask.classes.filter_node import FilterNode
from mainFlask.classes.filter_type import FilterType
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
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
        #CacheStore.Instance().empty_database()

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

def test_linguistic_analysis_with_full_db(establish_db_connection):
    messages: list[Message] = CacheStore.Instance().get_all_messages()

    # spaCy analysis
    start_spacy = time.perf_counter()
    for msg in messages:
        utils.analyze_msg_with_spacy(msg)
    spacy_duration = time.perf_counter() - start_spacy

    # --- Parallel LanguageTool analysis ---
    start_lang = time.perf_counter()
    workers = utils.get_optimal_worker_count()
    lt_results = []

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(utils.analyze_msg_with_language_tool, msg): msg for msg in messages}
        for future in as_completed(futures):
            try:
                result = future.result()
                lt_results.extend(result)
            except Exception as e:
                msg = futures[future]
                print(f"Error analyzing message {msg.message_id}: {e}")

    CacheStore.Instance().create_lt_matches(lt_results)
    lang_duration = time.perf_counter() - start_lang

    # Write results to file
    results_file = Path(__file__).parent / "performance_results.txt"
    with open(results_file, "a", encoding="utf-8") as f:
        f.write(
            
            f"spaCy analyzed {len(messages)} messages in {spacy_duration:.2f}s "
            f"LT analyzed {len(messages)} messages in {lang_duration:.2f}s \n"
        )  
    assert len(messages) > 0

def test_execute_simple_query_empty_cache(establish_db_connection):
    start_query = time.perf_counter()
    fno: FilterNodeObject = FilterNodeObject(FilterNodeGroup.AUTHOR, None, selected_value="Esther")
    result = fno.get_result()
    query_duration = time.perf_counter() - start_query

    # Write results to file
    results_file = Path(__file__).parent / "performance_results.txt"
    with open(results_file, "a", encoding="utf-8") as f:
        f.write(
            f"Collected {len(result)} results in {query_duration:.2f}s\n"
        )

    CacheStore.Instance().empty_cache()
    assert len(result) >= 0

def test_execute_simple_query_full_cache(establish_db_connection):
    CacheStore.Instance().get_all_messages()
    start_query = time.perf_counter()
    fno: FilterNodeObject = FilterNodeObject(FilterNodeGroup.AUTHOR, None, selected_value="Esther")
    result = fno.get_result()
    query_duration = time.perf_counter() - start_query

    # Write results to file
    results_file = Path(__file__).parent / "performance_results.txt"
    with open(results_file, "a", encoding="utf-8") as f:
        f.write(
            f"Collected {len(result)} results in {query_duration:.2f}s\n"
        )

    CacheStore.Instance().empty_cache()
    assert len(result) >= 0

def test_execute_complex_query_empty_cache(establish_db_connection):
    start_query = time.perf_counter()
    root_node: FilterNode = FilterNode(FilterType.AND)
    fno_author: FilterNodeObject = FilterNodeObject(FilterNodeGroup.AUTHOR, None, selected_value="Esther")
    fno_pos: FilterNodeObject = FilterNodeObject(FilterNodeGroup.WORTART, None, selected_value="VERB")
    fno_error: FilterNodeObject = FilterNodeObject(FilterNodeGroup.CATEGORY, None, selected_value="CASING")
    root_node.add_leaf(fno_author)
    root_node.add_leaf(fno_pos)
    root_node.add_leaf(fno_error)
    result =  root_node.get_full_result()
    query_duration = time.perf_counter() - start_query

    # Write results to file
    results_file = Path(__file__).parent / "performance_results.txt"
    with open(results_file, "a", encoding="utf-8") as f:
        f.write(
            f"Collected {len(result)} results in {query_duration:.2f}s\n"
        )

    CacheStore.Instance().empty_cache()
    assert len(result) >= 0

def test_execute_complex_query_full_cache(establish_db_connection):
    CacheStore.Instance().get_all_messages()
    CacheStore.Instance().get_all_ltms()
    CacheStore.Instance().get_all_spacy_matches()
    start_query = time.perf_counter()
    root_node: FilterNode = FilterNode(FilterType.AND)
    fno_author: FilterNodeObject = FilterNodeObject(FilterNodeGroup.AUTHOR, None, selected_value="Esther")
    fno_pos: FilterNodeObject = FilterNodeObject(FilterNodeGroup.WORTART, None, selected_value="VERB")
    fno_error: FilterNodeObject = FilterNodeObject(FilterNodeGroup.CATEGORY, None, selected_value="CASING")
    root_node.add_leaf(fno_author)
    root_node.add_leaf(fno_pos)
    root_node.add_leaf(fno_error)
    result =  root_node.get_full_result()
    query_duration = time.perf_counter() - start_query

    # Write results to file
    results_file = Path(__file__).parent / "performance_results.txt"
    with open(results_file, "a", encoding="utf-8") as f:
        f.write(
            f"Collected {len(result)} results in {query_duration:.2f}s\n"
        )

    CacheStore.Instance().empty_cache()
    assert len(result) >= 0

def test_loop(establish_db_connection):
    for i in range(9):
        test_execute_complex_query_full_cache(establish_db_connection)
 
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

    # --- Parallel LanguageTool analysis ---
    start_lang = time.perf_counter()
    workers = utils.get_optimal_worker_count()
    lt_results = []

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(utils.analyze_msg_with_language_tool, msg): msg for msg in messages}
        for future in as_completed(futures):
            try:
                result = future.result()
                lt_results.extend(result)
            except Exception as e:
                msg = futures[future]
                print(f"Error analyzing message {msg.message_id}: {e}")

    CacheStore.Instance().create_lt_matches(lt_results)
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

    # Clean up
    CacheStore.Instance().empty_database()
    CacheStore.Instance().empty_cache()
    assert len(messages) > 0