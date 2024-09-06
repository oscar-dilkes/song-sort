import sqlite3
import os

def connect_sqlite(db_path="songSort.db"):
    """
    Connect to SQLite database, creating it if it doesn't exist.
    Args:
        db_path (str): The path to the SQLite database file.
    Returns:
        sqlite3.Connection: SQLite database connection object.
    """
    try:
        # Connect to the SQLite database (creates file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        print(f"Connected to SQLite database at {db_path}")

        # Create the 'songs' table if it doesn't exist
        create_table(conn)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
        return None

def create_table(conn):
    """
    Create the 'songs' table in SQLite if it doesn't exist.
    Args:
        conn (sqlite3.Connection): SQLite database connection object.
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            title TEXT,
            duration INTEGER,
            filepath TEXT,
            tempo REAL,
            rms REAL,
            sc REAL,
            zcr REAL,
            energy_score INTEGER
        )
        """)
        conn.commit()
        print("Table 'songs' checked/created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def add_song(conn, song):
    """
    Add a song to the SQLite database.
    Args:
        conn (sqlite3.Connection): SQLite database connection object.
        song (Song): Song object containing song details.
    """
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO songs (id, title, duration, filepath, tempo, rms, sc, zcr, energy_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            song.track_id,
            song.title,
            int(song.duration) if song.duration is not None else 0,
            song.filepath,
            float(song.tempo) if song.tempo is not None else 0.0,
            float(song.rms) if song.rms is not None else 0.0,
            float(song.sc) if song.sc is not None else 0.0,
            float(song.zcr) if song.zcr is not None else 0.0,
            int(song.energy_score) if song.energy_score is not None else 0
        )
        cursor.execute(sql, values)
        conn.commit()
        print(f"Song added to the database: {song.title}")
    except sqlite3.Error as e:
        print(f"Error adding song: {e}")

def update_table(conn, songs):
    """
    Update the SQLite table with new songs.
    Args:
        conn (sqlite3.Connection): SQLite database connection object.
        songs (dict): Dictionary of Song objects keyed by their track IDs.
    """
    for song in songs.values():
        add_song(conn, song)

def validate_song(conn, track_id):
    """
    Validate if a song exists in the SQLite database.
    Args:
        conn (sqlite3.Connection): SQLite database connection object.
        track_id (str): Track ID of the song to validate.
    Returns:
        bool: True if the song exists, False otherwise.
    """
    cursor = conn.cursor()
    try:
        sql = "SELECT COUNT(*) FROM songs WHERE id = ?"
        cursor.execute(sql, (track_id,))
        result = cursor.fetchone()
        return result[0] > 0
    except sqlite3.Error as e:
        print(f"Error validating song: {e}")
        return False
    finally:
        cursor.close()

def dict_split_existing(conn, songs):
    """
    Split songs into new and existing based on their existence in the SQLite database.
    Args:
        conn (sqlite3.Connection): SQLite database connection object.
        songs (dict): Dictionary of Song objects keyed by their track IDs.
    Returns:
        tuple: (new_songs, existing_songs) where each is a dictionary of Song objects.
    """
    new_songs = {}
    existing_songs = {}

    for track_id, song in songs.items():
        if validate_song(conn, track_id):
            existing_songs[track_id] = song
        else:
            new_songs[track_id] = song

    # Fetch energy scores for the songs that are already in the database
    existing_songs = fetch_energy_scores(conn, existing_songs)

    return new_songs, existing_songs

def fetch_energy_scores(conn, existing_songs):
    """
    Fetch energy scores for existing songs from the SQLite database.
    Args:
        conn (sqlite3.Connection): SQLite database connection object.
        existing_songs (dict): Dictionary of Song objects keyed by their track IDs.
    Returns:
        dict: Updated dictionary of existing Song objects with fetched energy scores.
    """
    track_ids = list(existing_songs.keys())

    if not track_ids:
        return existing_songs

    query = "SELECT id, filepath, energy_score FROM songs WHERE id IN (%s)" % ','.join('?' * len(track_ids))

    cursor = conn.cursor()
    try:
        cursor.execute(query, track_ids)
        results = cursor.fetchall()

        updates_needed = []

        for track_id, db_filepath, energy_score in results:
            track_id = str(track_id)
            if track_id in existing_songs:
                song = existing_songs[track_id]
                song.set_energy_score(energy_score)
                if song.filepath != db_filepath:
                    updates_needed.append((song.filepath, track_id))

        if updates_needed:
            update_filepaths(conn, updates_needed)

    except sqlite3.Error as e:
        print(f"Error fetching energy scores: {e}")
    finally:
        cursor.close()

    return existing_songs

def update_filepaths(conn, updates):
    """
    Update file paths for songs in the SQLite database.
    Args:
        conn (sqlite3.Connection): SQLite database connection object.
        updates (list): List of tuples containing (filepath, track_id) for updates.
    """
    sql = "UPDATE songs SET filepath = ? WHERE id = ?"
    cursor = conn.cursor()
    try:
        cursor.executemany(sql, updates)
        conn.commit()
        print(f"Batch updated {len(updates)} file paths.")
    except sqlite3.Error as e:
        print(f"Error updating file paths: {e}")
    finally:
        cursor.close()