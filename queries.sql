'Movies Table

id: number
key: name+year
year: year
name: unique for each Movies
main_page: link to the webpage
last_updated: timestamp
'

CREATE TABLE movies(
key TEXT PRIMARY KEY NOT NULL,
name TEXT NOT NULL,
year INT,
main_page TEXT,
last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

'Links Table

id: incrementally generated id,
key: foreign-key from movies table
link: actual link
link_type: magnet|torrent_file
quality: quality of the print,
language: language 
last_updated : updated time


'

CREATE TABLE Links(
id INTEGER PRIMARY KEY AUTOINCREMENT,
key TEXT  NOT NULL,
link TEXT,
link_type TEXT,
quality TEXT,
language TEXT,
last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_movies
    FOREIGN KEY (key)
    REFERENCES movies(key)
);

'PRAGMA foreign_keys = 1'