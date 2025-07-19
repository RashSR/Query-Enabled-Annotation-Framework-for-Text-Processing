SELECT * FROM author;

DELETE FROM chat WHERE id = 4;

INSERT INTO author VALUES (1, 'Reinhold', 30, 'Male', 'Deutsch', 'Russisch, Englisch', 'Bayern', 'Softwareentwickler');
INSERT INTO author VALUES (2, 'Ben Vector', 24, 'Male', 'Deutsch', 'Englisch', 'Bayern', 'Bachelorant');
INSERT INTO author VALUES (3, 'Johannes Rösner', 22, 'Male', 'Deutsch', 'Englisch', 'Bayern', 'Praktikant');
INSERT INTO author VALUES (4, 'Martina', 37, 'Female', 'Deutsch', 'Englisch, Französisch', 'Hessen', 'Gärtnerin');
INSERT INTO author VALUES (5, 'Marc', 34, 'Male', 'Deutsch', 'English', 'Nordrhein-Westfalen', 'Theaterleiter');

-- Chat_id:1 -> Reinhold und Ben
INSERT INTO chat_participants VALUES (1, 1);
INSERT INTO chat_participants VALUES (1, 2);

-- Chat_id:2 -> Reinhold und Johannes
INSERT INTO chat_participants VALUES(2, 1);
INSERT INTO chat_participants VALUES(2, 3);

-- Chat_id:3 -> Reinhold und Martina
INSERT INTO chat_participants VALUES(3, 1);
INSERT INTO chat_participants VALUES(3, 4);

SELECT * FROM chat_participants cp;

-- added chat 1 to 3
INSERT INTO chat VALUES (1);
INSERT INTO chat VALUES (2);
INSERT INTO chat VALUES (3);

SELECT * FROM message;
DROP TABLE message;

CREATE TABLE message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    quoted_message_id INTEGER,
    annotated_text TEXT,
    FOREIGN KEY (chat_id) REFERENCES chat(id),
    FOREIGN KEY (sender_id) REFERENCES author(id),
    FOREIGN KEY (quoted_message_id) REFERENCES message(id)
);


INSERT INTO message VALUES ()

SELECT * FROM message;

DELETE FROM message;

CREATE TABLE lt_match(
    id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    chat_id INTEGER NOT NULL,
    start_pos INTEGER NOT NULL,
    end_pos INTEGER NOT NULL,
    content VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    rule_id VARCHAR(100) NOT NULL,
    PRIMARY KEY (id, message_id, chat_id),
    FOREIGN KEY (message_id, chat_id) REFERENCES message(id, chat_id)
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

CREATE VIEW message_join_spacy_match AS
SELECT * FROM message m
JOIN spacy_match sm ON m.id = sm.message_id;