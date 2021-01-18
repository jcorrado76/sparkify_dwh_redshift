"""This module contains the SQL queries to create the final tables used
"""
import configparser

table_names_config = configparser.ConfigParser()
table_names_config.read("table_names.cfg")


songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id BIGINT IDENTITY(0, 1),
        start_time TIMESTAMP,
        user_id INT,
        level VARCHAR(10),
        song_id VARCHAR(50),
        artist_id VARCHAR(50),
        session_id INT,
        location VARCHAR(50),
        user_agent VARCHAR(50),
        PRIMARY KEY (songplay_id));
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        gender VARCHAR(5),
        level VARCHAR(10),
        PRIMARY KEY(user_id)
);
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs(
	song_id VARCHAR(50),
	title VARCHAR(50),
	artist_id VARCHAR(50),
	year INT,
	duration DOUBLE PRECISION,
	FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
	PRIMARY KEY (artist_id, song_id)
);

""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR(50),
        name VARCHAR(50),
        location VARCHAR(50),
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        PRIMARY KEY(artist_id)
);
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP NOT NULL,
        hour INT NOT NULL,
        day INT NOT NULL,
        week INT NOT NULL,
        month INT NOT NULL,
        year INT NOT NULL,
        weekday INT NOT NULL,
        PRIMARY KEY (start_time)
);
""")

create_final_tables_queries = [songplay_table_create,
        user_table_create, song_table_create, artist_table_create,
        time_table_create]
