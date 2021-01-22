"""This module contains the SQL queries to create the staging tables
"""
import configparser
import sys

table_names_config = configparser.ConfigParser()
table_names_config.read("sql_queries/table_names.cfg")

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS {} (
        event_id      BIGINT IDENTITY(0,1) NOT NULL,
        artist        VARCHAR              NULL,
        auth          VARCHAR              NULL,
        firstName     VARCHAR              NULL,
        gender        VARCHAR              NULL,
        itemInSession VARCHAR              NULL,
        lastName      VARCHAR              NULL,
        length        VARCHAR              NULL,
        level         VARCHAR              NULL,
        location      VARCHAR              NULL,
        method        VARCHAR              NULL,
        page          VARCHAR              NULL,
        registration  VARCHAR              NULL,
        sessionId     INT                  NOT NULL SORTKEY DISTKEY,
        song          VARCHAR              NULL,
        status        INT                  NULL,
        ts            BIGINT               NOT NULL,
        userAgent     VARCHAR              NULL,
        userId        INT                  NULL
);
""".format(table_names_config["STAGING"]["events"]))

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS {} (
        artist_id        VARCHAR(50)       NOT NULL SORTKEY DISTKEY,
        artist_latitude  DOUBLE PRECISION  NULL,
        artist_longitude DOUBLE PRECISION  NULL,
        artist_location  VARCHAR(500)      NULL,
        artist_name      VARCHAR(500)      NULL,
        song_id          VARCHAR(50)       NOT NULL,
        title            VARCHAR(500)      NULL,
        duration         DECIMAL(9)        NULL,
        year             INT               NULL
);
""".format(table_names_config["STAGING"]["songs"]))

create_staging_tables_queries = [staging_events_table_create,
        staging_songs_table_create]
