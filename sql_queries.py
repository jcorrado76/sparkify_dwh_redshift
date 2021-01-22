"""This module defines the queries to copy the data from the S3 buckets into the
staging tables
"""

import configparser
config = configparser.ConfigParser()
config.read('dwh.cfg')

table_names_config = configparser.ConfigParser()
table_names_config.read("table_names.cfg")

# DROP ALL TABLES
STAGING_EVENTS_TABLE_DROP = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["STAGING"]["events"])
STAGING_SONGS_TABLE_DROP = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["STAGING"]["songs"])
SONGPLAY_TABLE_DROP = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["FINAL"]["songplays"])
USER_TABLE_DROP = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["FINAL"]["users"])
SONG_TABLE_DROP = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["FINAL"]["songs"])
ARTIST_TABLE_DROP = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["FINAL"]["artists"])
TIME_TABLE_DROP = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["FINAL"]["time"])


# CREATE STAGING TABLES
STAGING_EVENTS_TABLE_CREATE= ("""
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

STAGING_SONGS_TABLE_CREATE = ("""
    CREATE TABLE IF NOT EXISTS {} (
        artist_id        VARCHAR(50)       NOT NULL SORTKEY DISTKEY,
        artist_latitude  DOUBLE PRECISION  NULL,
        artist_longitude DOUBLE PRECISION  NULL,
        artist_location  VARCHAR(500)      NULL,
        artist_name      VARCHAR(500)      NULL,
        song_id          VARCHAR(50)       NOT NULL,
        title            VARCHAR(500)      NULL,
        duration         DECIMAL(9)        NULL,
        year             INT               NULL,
);
""".format(table_names_config["STAGING"]["songs"]))

# CREATE FINAL TABLES
SONGPLAY_TABLE_CREATE = ("""
    CREATE TABLE IF NOT EXISTS {} (
        songplay_id  INT IDENTITY(0, 1) NOT NULL SORTKEY,
        start_time   TIMESTAMP          NOT NULL,
        user_id      INT                NOT NULL DISTKEY,
        level        VARCHAR(10)        NOT NULL,
        song_id      VARCHAR(50)        NOT NULL,
        artist_id    VARCHAR(50)        NOT NULL,
        session_id   INT                NOT NULL,
        location     VARCHAR(100)       NULL,
        user_agent   VARCHAR(255)       NULL,
        PRIMARY KEY(songplay_id)
);""".format(table_names_config["FINAL"]["songplays"]))

USER_TABLE_CREATE = ("""
    CREATE TABLE IF NOT EXISTS {} (
        user_id    INT               NOT NULL SORTKEY,
        first_name VARCHAR(50)       NULL,
        last_name  VARCHAR(50)       NULL,
        gender     VARCHAR(5)        NULL,
        level      VARCHAR(10)       NULL,
        PRIMARY KEY (user_id)
) diststyle all;
""".format(table_names_config["FINAL"]["users"]))

SONG_TABLE_CREATE = ("""
    CREATE TABLE IF NOT EXISTS {} (
        song_id   VARCHAR(50)       NOT NULL SORTKEY,
        title     VARCHAR(500)      NOT NULL,
        artist_id VARCHAR(50)       NOT NULL,
        year      INT               NOT NULL,
        duration  DECIMAL(9)        NOT NULL,
        PRIMARY KEY (song_id)
);
""".format(table_names_config["FINAL"]["songs"]))

ARTIST_TABLE_CREATE = ("""
    CREATE TABLE IF NOT EXISTS {} (
        artist_id VARCHAR(50)    NOT NULL SORTKEY,
        name      VARCHAR(500)   NULL,
        location  VARCHAR(500)   NULL,
        latitude  DECIMAL(9)     NULL,
        longitude DECIMAL(9)     NULL,
        PRIMARY KEY (artist_id)
) diststyle all;
""".format(table_names_config["FINAL"]["artists"]))

TIME_TABLE_CREATE = ("""
    CREATE TABLE IF NOT EXISTS {} (
        start_time TIMESTAMP NOT NULL SORTKEY,
        hour       SMALLINT  NULL,
        day        SMALLINT  NULL,
        week       SMALLINT  NULL,
        month      SMALLINT  NULL,
        year       SMALLINT  NULL,
        weekday    SMALLINT  NULL,
        PRIMARY KEY (start_time)
) diststyle all;
""".format(table_names_config["FINAL"]["time"]))

# COPY DATA FROM S3 INTO STAGING TABLES
STAGING_EVENTS_COPY = ("""
    copy {} from '{}'
    iam_role '{}'
    format as json '{}'
    region 'us-west-2';
""").format(table_names_config["STAGING"]["events"],
            config["S3"]["LOG_DATA"],
            config["IAM_ROLE"]["ARN"],
            config["S3"]["LOG_JSONPATH"])

STAGING_SONGS_COPY = ("""
    copy {} from '{}'
    iam_role '{}'
    format as json 'auto'
    acceptinvchars as '^'
    region 'us-west-2';
""").format(table_names_config["STAGING"]["songs"],
            config["S3"]["SONG_DATA"],
            config["IAM_ROLE"]["ARN"])


# COPY DATA FROM STAGING TABLES INTO FINAL TABLES
SONGPLAY_TABLE_INSERT = ("""
    INSERT INTO {} (
        start_time, 
        user_id,
        level,
        song_id,
        artist_id,
        session_id,
        location,
        user_agent)
    SELECT (timestamp 'epoch' + events.ts/1000 * interval '1 second') AS start_time,
           events.userId AS user_id,
           events.level,
           songs.song_id AS song_id,
           songs.artist_id AS artist_id,
           events.sessionId AS session_id,
           events.location,
           events.userId AS user_agent
    FROM staging_events AS events
    JOIN staging_songs AS songs on events.song=songs.title
    WHERE events.page = 'NextSong';
""".format(table_names_config["FINAL"]["songplays"]))

USER_TABLE_INSERT = ("""
    INSERT INTO {} (
        user_id,
        first_name,
        last_name,
        gender,
        level)
    SELECT DISTINCT(events.userId) AS user_id,
           events.firstName        AS first_name,
           events.lastName         AS last_name,
           events.gender           AS gender,
           events.level            AS level
    FROM staging_events as events
    WHERE events.page = 'NextSong';
""".format(table_names_config["FINAL"]["users"]))

SONG_TABLE_INSERT = ("""
    INSERT INTO {} (
        song_id,
        title,
        artist_id,
        year,
        duration)
    SELECT DISTINCT(song_id),
           title,
           artist_id,
           year,
           duration
    FROM staging_songs;
""".format(table_names_config["FINAL"]["songs"]))

ARTIST_TABLE_INSERT = ("""
    INSERT INTO {} (
        artist_id,
        name,
        location,
        latitude,
        longitude)
    SELECT DISTINCT(artist_id) AS artist_id,
	   artist_name AS name,
	   artist_location AS location,
	   artist_latitude AS latitude,
	   artist_longitude AS longitude
    FROM staging_songs;
""".format(table_names_config["FINAL"]["artists"]))

TIME_TABLE_INSERT = ("""
    INSERT INTO {} (
        start_time,
        hour,
        day,
        week,
        month,
        year,
        weekday)
    SELECT DISTINCT(timestamp 'epoch' + ts/1000 * interval '1 second') AS start_time,
  	   extract(hour from start_time) AS hour,
  	   extract(day from start_time) AS day,
  	   extract(week from start_time) AS week,
  	   extract(month from start_time) AS month,
  	   extract(year from start_time) AS year,
  	   extract(weekday from start_time) AS weekday
    FROM staging_events
    WHERE page = 'NextSong';
""".format(table_names_config["FINAL"]["time"]))

# DEFINE LISTS OF QUERIES TO EXECUTE IN LOOP
insert_table_queries = [
    SONGPLAY_TABLE_INSERT,
    USER_TABLE_INSERT,
    SONG_TABLE_INSERT,
    ARTIST_TABLE_INSERT,
    TIME_TABLE_INSERT
]

drop_table_queries = [
    STAGING_EVENTS_TABLE_DROP,
    STAGING_SONGS_TABLE_DROP,
    SONGPLAY_TABLE_DROP,
    USER_TABLE_DROP,
    SONG_TABLE_DROP,
    ARTIST_TABLE_DROP,
    TIME_TABLE_DROP
]

create_staging_tables_queries = [
    STAGING_EVENTS_TABLE_CREATE,
    STAGING_SONGS_TABLE_CREATE
]

create_final_tables_queries = [
    SONGPLAY_TABLE_CREATE,
    USER_TABLE_CREATE,
    SONG_TABLE_CREATE,
    ARTIST_TABLE_CREATE,
    TIME_TABLE_CREATE
]

copy_table_queries = [
    STAGING_EVENTS_COPY,
    STAGING_SONGS_COPY
]
