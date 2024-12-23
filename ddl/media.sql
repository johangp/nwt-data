DROP TABLE IF EXISTS raw_media;
CREATE TABLE raw_media (
    id VARCHAR,
    sentiment VARCHAR,
    categories JSONB,
    feed_id VARCHAR,
    feed_name VARCHAR,
    date TIMESTAMP,
    msg_id VARCHAR,
    type VARCHAR,
    title TEXT,
    summary TEXT,
    text TEXT,
    source_title TEXT,
    link TEXT
);
