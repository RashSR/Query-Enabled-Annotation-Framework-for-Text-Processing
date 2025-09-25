PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS author_with_chat_ids;
DROP VIEW IF EXISTS message_join_lt_match;
DROP VIEW IF EXISTS message_join_spacy_match;
DROP VIEW IF EXISTS message_with_ltm_and_spacy_ids;
DROP TABLE IF EXISTS annotation;
DROP TABLE IF EXISTS lt_match;
DROP TABLE IF EXISTS spacy_match;
DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS chat_participants;
DROP TABLE IF EXISTS chat;
DROP TABLE IF EXISTS author;


CREATE TABLE author (
	id INTEGER PRIMARY KEY AUTOINCREMENT, 
	name VARCHAR(100) NOT NULL, 
	age INTEGER, 
	gender VARCHAR(20), 
	first_language VARCHAR(50), 
	languages VARCHAR(200), 
	region VARCHAR(100), 
	job VARCHAR(100), 
	annotation text
);

CREATE TABLE chat (
	id INTEGER PRIMARY KEY AUTOINCREMENT, 
	groupname VARCHAR(100), 
	relation VARCHAR(255)
);

CREATE TABLE chat_participants (
	chat_id INTEGER NOT NULL, 
	author_id INTEGER NOT NULL, 
	PRIMARY KEY (chat_id, author_id), 
	FOREIGN KEY(chat_id) REFERENCES chat (id) ON DELETE CASCADE,
	FOREIGN KEY(author_id) REFERENCES author (id) ON DELETE CASCADE
);

CREATE TABLE message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    quoted_message_id INTEGER,
    FOREIGN KEY (chat_id) REFERENCES chat(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES author(id) ON DELETE CASCADE,
    FOREIGN KEY (quoted_message_id) REFERENCES message(id) ON DELETE SET NULL
);

CREATE TABLE annotation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER NOT NULL,
    start_pos INTEGER NOT NULL,
    end_pos INTEGER NOT NULL,
    annotation TEXT NOT NULL,
    reason TEXT,
    comment TEXT,
    FOREIGN KEY (message_id) REFERENCES message(id) ON DELETE CASCADE
);

CREATE TABLE lt_match (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER NOT NULL,
    chat_id    INTEGER NOT NULL,
    start_pos  INTEGER NOT NULL,
    end_pos    INTEGER NOT NULL,
    content    VARCHAR(100) NOT NULL,
    category   VARCHAR(100) NOT NULL,
    rule_id    VARCHAR(100) NOT NULL,
    FOREIGN KEY (message_id) REFERENCES message(id) ON DELETE CASCADE
);

CREATE TABLE spacy_match (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER NOT NULL,
    chat_id INTEGER NOT NULL,
    start_pos INTEGER NOT NULL,
    end_pos INTEGER NOT NULL,
    text TEXT NOT NULL,
    lemma TEXT,
    pos TEXT,
    tag TEXT,
    is_alpha BOOLEAN,
    is_stop BOOLEAN,
    tense TEXT,
    person TEXT,
    verb_form TEXT,
    voice TEXT,
    degree TEXT,
    gram_case TEXT,
    number TEXT,
    gender TEXT,
    mood TEXT,
    pron_type TEXT,
    FOREIGN KEY (message_id) REFERENCES message(id) ON DELETE CASCADE,
    FOREIGN KEY (chat_id) REFERENCES chat(id) ON DELETE CASCADE
);

CREATE VIEW author_with_chat_ids AS
SELECT
    author.id AS author_id,
    author.name,
    author.age,
    author.gender,
    author.first_language,
    author.languages,
    author.region,
    author.job,
    author.annotation,
    STRING_AGG(chat_participants.chat_id, ', ') AS chat_ids
FROM
    author
LEFT JOIN chat_participants ON author.id = chat_participants.author_id
GROUP BY
    author.id, author.name;

CREATE VIEW message_join_lt_match AS
SELECT * FROM message m
JOIN lt_match lm ON m.id = lm.message_id;

CREATE VIEW message_join_spacy_match AS
SELECT * FROM message m
JOIN spacy_match sm ON m.id = sm.message_id;

CREATE VIEW message_with_ltm_and_spacy_ids AS
SELECT
    m.*,  -- all columns from message
    (
      SELECT GROUP_CONCAT(id, ',')
      FROM (
        SELECT lm.id
        FROM lt_match AS lm
        WHERE lm.message_id = m.id
          AND lm.chat_id = m.chat_id
        ORDER BY lm.id
      )
    ) AS lt_match_ids,
    (
      SELECT GROUP_CONCAT(id, ',')
      FROM (
        SELECT sm.id
        FROM spacy_match AS sm
        WHERE sm.message_id = m.id
          AND sm.chat_id = m.chat_id
        ORDER BY sm.id
      )
    ) AS spacy_match_ids
FROM message AS m;



