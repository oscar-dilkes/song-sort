import sqlite3

def connect_sqlite(db_path="songSort.db"):
    try:
        conn = sqlite3.connect(db_path)
        print(f"Connected to SQLite database at {db_path}")

        create_table(conn)
        truncate_table(conn)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
        return None

def truncate_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM songs")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error truncating table: {e}")

def create_table(conn):
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
    except sqlite3.Error as e:
        print(f"Error adding song: {e}")

def update_table(conn, songs):
    for song in songs.values():
        add_song(conn, song)

def validate_song(conn, track_id):
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
    new_songs = {}
    existing_songs = {}

    for track_id, song in songs.items():
        if validate_song(conn, track_id):
            existing_songs[track_id] = song
        else:
            new_songs[track_id] = song

    existing_songs = fetch_energy_scores(conn, existing_songs)

    return new_songs, existing_songs

def fetch_energy_scores(conn, existing_songs):
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