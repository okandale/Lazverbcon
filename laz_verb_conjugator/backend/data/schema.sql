CREATE TABLE verb(
    verb_id INT PRIMARY KEY,
    infinitive_form VARCHAR(255)
);

CREATE TABLE region(
    "code" TEXT PRIMARY KEY,
    "name" TEXT
);

INSERT INTO region VALUES
    ('AŞ', 'Ardeşen'),
    ('FA', 'Findıklı-Arhavi'),
    ('HO', 'Hopa'),
    ('PZ', 'Pazar')
;

CREATE TABLE region_verb(
    region_code TEXT NOT NULL,
    verb_id INT NOT NULL,
    verb_type TEXT NOT NULL CHECK (verb_type in ("ERGATIVE", "DATIVE", "NOMINATIVE")),
    verb_root TEXT,
    english_translation TEXT,
    turkish_verb TEXT
);