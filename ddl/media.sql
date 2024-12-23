DROP TYPE IF EXISTS category;
CREATE TYPE category AS (
    id VARCHAR,
    name VARCHAR
);

DROP TYPE IF EXISTS feed;
CREATE TYPE feed AS (
    id VARCHAR,
    name VARCHAR
);

DROP TYPE IF EXISTS source;
CREATE TYPE source AS (
    title VARCHAR
);


DROP TABLE IF EXISTS raw_media;
CREATE TABLE raw_media (
    id VARCHAR,
    sentiment VARCHAR,
    categories category[],  
    feed feed,               
    date TIMESTAMP,
    msgId VARCHAR,
    type VARCHAR,
    title TEXT,
    summary TEXT,
    text TEXT,
    source source,
    link TEXT
);
