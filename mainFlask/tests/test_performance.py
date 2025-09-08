import time
import pytest
import utils
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from mainFlask.data.cachestore import CacheStore
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

