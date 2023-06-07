CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user', -- 'user' or 'admin'
    UNIQUE(username)
);

CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    is_secret BOOLEAN NOT NULL,
    UNIQUE(name)
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    area_id INTEGER,
    creator_id INTEGER,
    FOREIGN KEY (area_id) REFERENCES areas (id),
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

CREATE INDEX idx_threads_area_id ON threads(area_id);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    thread_id INTEGER,
    sender_id INTEGER,
    FOREIGN KEY (thread_id) REFERENCES threads (id),
    FOREIGN KEY (sender_id) REFERENCES users (id)
);

CREATE INDEX idx_messages_thread_id ON messages(thread_id);
CREATE INDEX idx_messages_sender_id ON messages(sender_id);

CREATE TABLE secret_areas (
    user_id INTEGER,
    area_id INTEGER,
    PRIMARY KEY(user_id, area_id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (area_id) REFERENCES areas (id)
);
