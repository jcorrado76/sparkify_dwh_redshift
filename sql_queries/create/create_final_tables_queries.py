"""This module contains the SQL queries to create the final tables used
"""
import configparser
import sys

table_names_config = configparser.ConfigParser()
table_names_config.read("sql_queries/table_names.cfg")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS {} (
    songplay_id  INT IDENTITY(0, 1) NOT NULL SORTKEY,
    start_time   TIMESTAMP          NOT NULL,
    user_id      INT                NOT NULL DISTKEY,
    level        VARCHAR(10)        NOT NULL,
    song_id      VARCHAR(50)        NOT NULL,
    artist_id    VARCHAR(50)        NOT NULL,
    session_id   INT                NOT NULL,
    location     VARCHAR(100)       NULL,
    user_agent   VARCHAR(255)       NULL
);""".format(table_names_config["FINAL"]["songplays"]))

user_table_create = ("""
CREATE TABLE IF NOT EXISTS {} (
    user_id    INT               NOT NULL SORTKEY,
    first_name VARCHAR(50)       NULL,
    last_name  VARCHAR(50)       NULL,
    gender     VARCHAR(5)        NULL,
    level      VARCHAR(10)       NULL
) diststyle all;
""".format(table_names_config["FINAL"]["users"]))

song_table_create = ("""
CREATE TABLE IF NOT EXISTS {} (
    song_id   VARCHAR(50)       NOT NULL SORTKEY,
    title     VARCHAR(500)      NOT NULL,
    artist_id VARCHAR(50)       NOT NULL,
    year      INT               NOT NULL,
    duration  DECIMAL(9)        NOT NULL
);
""".format(table_names_config["FINAL"]["songs"]))

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS {} (
    artist_id VARCHAR(50)    NOT NULL SORTKEY,
    name      VARCHAR(500)   NULL,
    location  VARCHAR(500)   NULL,
    latitude  DECIMAL(9)     NULL,
    longitude DECIMAL(9)     NULL
) diststyle all;
""".format(table_names_config["FINAL"]["artists"]))

time_table_create = ("""
CREATE TABLE IF NOT EXISTS {} (
    start_time TIMESTAMP NOT NULL SORTKEY,
    hour       SMALLINT  NULL,
    day        SMALLINT  NULL,
    week       SMALLINT  NULL,
    month      SMALLINT  NULL,
    year       SMALLINT  NULL,
    weekday    SMALLINT  NULL
) diststyle all;
""".format(table_names_config["FINAL"]["time"]))

create_final_tables_queries = [songplay_table_create,
        user_table_create, song_table_create, artist_table_create,
        time_table_create]
