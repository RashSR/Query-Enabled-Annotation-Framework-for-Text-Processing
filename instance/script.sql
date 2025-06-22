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
    id INTEGER NOT NULL,
    chat_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    content TEXT NOT NULL,
    quoted_message_id INTEGER,
    error_dict_json TEXT,
    annotated_text TEXT,
    PRIMARY KEY (id, chat_id),
    FOREIGN KEY (chat_id) REFERENCES chat(id),
    FOREIGN KEY (sender_id) REFERENCES author(id),
    FOREIGN KEY (quoted_message_id) REFERENCES message(id)
);

INSERT INTO message VALUES ()

SELECT * FROM message;

DELETE FROM message;