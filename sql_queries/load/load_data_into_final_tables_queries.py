"""This module defines the queries to copy the data from the staging tables into the
final tables
"""
import configparser
import sys
table_names_config = configparser.ConfigParser()
table_names_config.read("sql_queries/table_names.cfg")


songplay_table_insert = ("""
SELECT temp_ts.start_time AS start_time,
       userId AS user_id,
       level,
       song_id AS song_id,
       artist_id AS artist_id,
       sessionId AS session_id,
       location,
       userId AS user_agent
INTO {}
FROM TABLE staging_events AS events, staging_songs AS songs, temp_ts_table AS temp_ts
WHERE events.song = songs.title AND
      events.artist = songs.artist_name AND
      events.ts = temp_ts.ts;
""".format(table_names_config["FINAL"]["songplays"]))

user_table_insert = ("""
SELECT DISTINCT(userId) AS user_id,
	   firstName AS first_name,
	   lAStName AS lASt_name,
	   gender,
	   level
INTO {} 
FROM TABLE staging_events;
""".format(table_names_config["FINAL"]["users"]))

song_table_insert = ("""
SELECT DISTINCT(song_id),
	   title,
	   artist_id,
	   year,
	   duration
INTO {} 
FROM staging_songs;
""".format(table_names_config["FINAL"]["songs"]))

artist_table_insert = ("""
SELECT DISTINCT(artist_id) AS artist_id,
	   artist_name AS name,
	   artist_location AS location,
	   artist_latitude AS latitude,
	   artist_longitude AS longitude
INTO {} 
FROM staging_songs;
""".format(table_names_config["FINAL"]["artists"]))

time_table_insert = ("""
SELECT start_time,
  	   extract(hour from start_time) AS hour,
  	   extract(day from start_time) AS day,
  	   extract(week from start_time) AS week,
  	   extract(month from start_time) AS month,
  	   extract(year from start_time) AS year,
  	   extract(weekday from start_time) AS weekday,
INTO {}
FROM temp_ts_table
""".format(table_names_config["FINAL"]["time"]))



insert_table_queries = [songplay_table_insert,
        user_table_insert,
        song_table_insert,
        artist_table_insert,
        time_table_insert]
