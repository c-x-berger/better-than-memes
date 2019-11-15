CREATE TABLE users
(
    username text PRIMARY KEY,
    password text      NOT NULL,
    joined   timestamp NOT NULL DEFAULT (now())::timestamp
);

CREATE TABLE boards
(
    path    ltree PRIMARY KEY,
    creator text REFERENCES users (username) NOT NULL
);

CREATE TABLE posts
(
    id        text PRIMARY KEY,
    author    text REFERENCES users (username),
    timestamp timestamp NOT NULL,
    content   text,
    title     text      NOT NULL,
    board     ltree REFERENCES boards (path)
);

CREATE TABLE comments
(
    id        text PRIMARY KEY,
    author    text      NOT NULL,
    timestamp timestamp NOT NULL,
    content   text      NOT NULL,
    parent    text,
    children  text[],
    post      text REFERENCES posts (id)
);