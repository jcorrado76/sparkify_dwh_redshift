"""This module contains the SQL queries to create the staging tables
"""
import configparser
import sys
sys.path.insert("..")

table_names_config = configparser.ConfigParser()
table_names_config.read("table_names.cfg")

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS {} (
        artist VARCHAR(50),
        auth VARCHAR(50),
        firstName VARCHAR(50),
        lastName VARCHAR(50),
        gender VARCHAR(5),
        itemInSession INT,
        length DOUBLE PRECISION,
        level VARCHAR(10),
        location VARCHAR(50),
        method VARCHAR(10),
        page VARCHAR(50),
        registration DOUBLE PRECISION,
        sessionId INT,
        song VARCHAR(50),
        status INT,
        ts BIGINT,
        userAgent VARCHAR(50),
        userId INT
);
""".format(table_names_config["STAGING"]["events"]))

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS {} (
        artist_id VARCHAR(50),
        artist_latitude DOUBLE PRECISION,
        artist_longitude DOUBLE PRECISION,
        artist_location VARCHAR(50),
        artist_name VARCHAR(50),
        song_id VARCHAR(50),
        title VARCHAR(50),
        duration DOUBLE PRECISION,
        year INT
);
""".format(table_names_config["STAGING"]["songs"]))

create_staging_tables_queries = [staging_events_table_create,
        staging_songs_table_create]
