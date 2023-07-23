""" SQL queries to create tables in Redshift. """
# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"


# Create Tables

staging_events_table_create = """
CREATE TABLE IF NOT EXISTS staging_events (
    event_id INTEGER IDENTITY(0,1) PRIMARY KEY,
    artist VARCHAR(256),
    auth VARCHAR(20),
    firstName VARCHAR(50),
    gender CHAR,
    itemInSession INTEGER,
    lastName VARCHAR(50),
    length DECIMAL,
    level VARCHAR(10),
    location VARCHAR(256),
    method VARCHAR(10),
    page VARCHAR(30),
    registration DECIMAL,
    sessionId INTEGER,
    song VARCHAR(256),
    status INTEGER,
    ts BIGINT,
    userAgent VARCHAR(256),
    userId INTEGER
)
diststyle auto
sortkey auto;
"""

staging_songs_table_create = """
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs INTEGER,
    artist_id VARCHAR(256),
    artist_latitude DECIMAL,
    artist_longitude DECIMAL,
    artist_location VARCHAR(500),
    artist_name VARCHAR(500),
    song_id VARCHAR(256),
    title VARCHAR(256),
    duration DECIMAL,
    year INTEGER
)        
diststyle auto
sortkey auto;                       
"""

songplay_table_create = """
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id VARCHAR(56  ),
    start_time TIMESTAMP,
    user_id INTEGER,
    level VARCHAR(10),
    song_id VARCHAR(256),
    artist_id VARCHAR(256),
    session_id INTEGER,
    location VARCHAR(256),
    user_agent VARCHAR(256)
)
distkey(song_id)
sortkey(start_time);
"""

user_table_create = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50), 
    last_name VARCHAR(50),
    gender CHAR,
    level VARCHAR(10)
) 
diststyle all
sortkey(user_id);
"""

song_table_create = """
CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR(256) PRIMARY KEY,
    title VARCHAR(256),
    artist_id VARCHAR(256),
    location VARCHAR(256),
    latitude DECIMAL,
    longitude DECIMAL
)
diststyle all
sortkey(song_id);
"""

artist_table_create = """
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR(256) PRIMARY KEY,
    name VARCHAR(256),
    location VARCHAR(256),
    latitude DECIMAL,
    longitude DECIMAL
)
diststyle all
sortkey(artist_id);
"""

time_table_create = """
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP PRIMARY KEY,
    hour INTEGER,
    day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday VARCHAR(10)
)
diststyle all
sortkey(start_time);
"""


create_table_queries = [
    staging_events_table_create,
    staging_songs_table_create,
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
]

drop_table_queries = [
    staging_events_table_drop,
    staging_songs_table_drop,
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop,
]
