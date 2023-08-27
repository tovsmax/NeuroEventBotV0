CREATE TABLE Sessions (
    id INTEGER PRIMARY KEY UNIQUE AUTOINCREMENT,
    start_datetime TEXT NOT NULL,
    end_datetime TEXT CHECK(end_datetime >= start_datetime)
);

CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY UNIQUE,
    nickname TEXT NOT NULL UNIQUE,
);

CREATE TABLE Voters (
    voter_type TEXT NOT NULL CHECK(voter_type in ("spectator", "artist"))
)

CREATE TABLE Arts (
    id INTEGER PRIMARY KEY UNIQUE AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    image_url TEXT NOT NULL,
    file_name TEXT UNIQUE,
    author_id INTEGER,
    session_id INTEGER,
    FOREIGN KEY (session_id) REFERENCES Sessions (id) RESTRICT,
    FOREIGN KEY (author_id) REFERENCES Voters (user_id) RESTRICT
);

-- CREATE TABLE TopLists (
--     id INTEGER PRIMARY KEY UNIQUE AUTOINCREMENT,
--     session_id INTEGER NOT NULL,
--     voter_id INTEGER NOT NULL,
--     FOREIGN KEY (session_id) REFERENCES Sessions (id) RESTRICT,
--     FOREIGN KEY (voter_id) REFERENCES Voters (user_id) RESTRICT,
-- );

-- CREATE TABLE TopItems (
--     id INTEGER PRIMARY KEY UNIQUE AUTOINCREMENT,
--     rank INTEGER NOT NULL,
--     art_id INTEGER NOT NULL,
--     FOREIGN KEY (art_id) REFERENCES Arts (id) RESTRICT
-- );