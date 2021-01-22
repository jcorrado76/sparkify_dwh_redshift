"""This module defines the queries to copy the data from the staging tables into the
final tables
"""
import configparser
table_names_config = configparser.ConfigParser()
table_names_config.read("sql_queries/table_names.cfg")


songplay_table_insert = ("""
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

user_table_insert = ("""
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

song_table_insert = ("""
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

artist_table_insert = ("""
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

time_table_insert = ("""
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

insert_table_queries = [songplay_table_insert,
        user_table_insert,
        song_table_insert,
        artist_table_insert,
        time_table_insert]
