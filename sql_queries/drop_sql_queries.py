"""These are the SQL queries that are used to drop the tables that may have
already been created
"""

import configparser

table_names_config = configparser.ConfigParser()
table_names_config.read("table_names.cfg")

staging_events_table_drop = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["STAGING"]["events"])
staging_songs_table_drop = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["STAGING"]["songs"])
songplay_table_drop = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["FINAL"]["songplays"])
user_table_drop = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["FINAL"]["users"])
song_table_drop = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["FINAL"]["songs"])
artist_table_drop = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["FINAL"]["artists"])
time_table_drop = "DROP TABLE IF EXISTS {}"\
        .format(table_names_config["FINAL"]["time"])

drop_table_queries = [staging_events_table_drop,
        staging_songs_table_drop,
        songplay_table_drop, user_table_drop,
        song_table_drop,
        artist_table_drop,
        time_table_drop]
