-- Tabela Country
CREATE TABLE country (
    country_id INTEGER PRIMARY KEY,
    name TEXT
);

-- Tabela Person
CREATE TABLE person (
    person_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Tabela Type
CREATE TABLE type (
    type_id INTEGER PRIMARY KEY,
    designation TEXT NOT NULL UNIQUE
);

-- Tabela Genre
CREATE TABLE genre (
    genre_id INTEGER PRIMARY KEY,
    designation TEXT NOT NULL UNIQUE
);

-- Tabela Rating
CREATE TABLE rating (
    rating_id INTEGER PRIMARY KEY,
    designation TEXT NOT NULL UNIQUE
);

-- Tabela Content (tabela principal)
CREATE TABLE content (
    content_id INTEGER PRIMARY KEY,
    type_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    release_date DATE,
    date_added DATE,
    duration INTEGER,
    description TEXT,
    rating_id INTEGER,
    FOREIGN KEY (type_id) REFERENCES type(type_id),
    FOREIGN KEY (rating_id) REFERENCES rating(rating_id)
);

-- Tabela de junção Direction
CREATE TABLE direction (
    content_id INTEGER,
    person_id INTEGER,
    PRIMARY KEY (content_id, person_id),
    FOREIGN KEY (content_id) REFERENCES content(content_id),
    FOREIGN KEY (person_id) REFERENCES person(person_id)
);

-- Tabela de junção Cast
CREATE TABLE c_cast (
    content_id INTEGER,
    person_id INTEGER,
    PRIMARY KEY (content_id, person_id),
    FOREIGN KEY (content_id) REFERENCES content(content_id),
    FOREIGN KEY (person_id) REFERENCES person(person_id)
);

-- Tabela de junção Made_in
CREATE TABLE made_in (
    content_id INTEGER,
    country_id INTEGER,
    PRIMARY KEY (content_id, country_id),
    FOREIGN KEY (content_id) REFERENCES content(content_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);

-- Tabela de junção Classification
CREATE TABLE classification (
    content_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (content_id, genre_id),
    FOREIGN KEY (content_id) REFERENCES content(content_id),
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
);