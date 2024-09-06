import mysql.connector

def connect_mysql(mysql_password):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="songSort"
        )

        if not validate_table(mydb):
            create_table(mydb)

        return mydb

    except FileNotFoundError as e:
        print(f"Password file not found: {e}")
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")

def validate_table(mydb):
    cursor = mydb.cursor(buffered=True)
    try:
        # check if table exists
        cursor.execute("SELECT 1 FROM songs LIMIT 1;")
        return True
    except mysql.connector.Error as err:
        print(f"Error validating table: {err}")
        return False
    finally:
        cursor.close()

def create_table(mydb):
    try:
        cursor = mydb.cursor()
        cursor.execute("""
        CREATE TABLE songs (
            id INT PRIMARY KEY,
            title VARCHAR(255),
            duration INT,
            filepath VARCHAR(255),
            tempo FLOAT,
            rms FLOAT,
            sc FLOAT,
            zcr FLOAT,
            energy_score INT
        )
        """)
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

def add_song(mydb, song):
    try:
        cursor = mydb.cursor()
        sql = """
            INSERT INTO songs (id, title, duration, filepath, tempo, rms, sc, zcr, energy_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # handle none values here to prep for sql and m3u writing
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
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error adding song: {err}")
    finally:
        cursor.close()

def update_table(mydb, songs):
    for song in songs.values():
        add_song(mydb, song)

def validate_song(mydb, track_id):
    cursor = mydb.cursor(buffered=True)
    try:
        # check if song exists in table
        sql = "SELECT COUNT(*) FROM songs WHERE id = %s"
        cursor.execute(sql, (track_id,))
        result = cursor.fetchone()
        return result[0] > 0
    except mysql.connector.Error as err:
        print(f"Error validating song: {err}")
        return False
    finally:
        cursor.close()

def dict_split_existing(mydb, songs):
    new_songs = {}
    existing_songs = {}

    for track_id, song in songs.items():
        if validate_song(mydb, track_id):
            existing_songs[track_id] = song
        else:
            new_songs[track_id] = song

    existing_songs = fetch_energy_scores(mydb, existing_songs)

    return new_songs, existing_songs

def fetch_energy_scores(mydb, existing_songs):
    track_ids = list(existing_songs.keys())

    if not track_ids:
        return existing_songs

    try:
        query = "SELECT id, filepath, energy_score FROM songs WHERE id IN (%s)" % ','.join(['%s'] * len(track_ids))
        cursor = mydb.cursor()
        cursor.execute(query, track_ids)
        results = cursor.fetchall()

        updates_needed = []

        # update energy scores and check if filepaths have changed
        for track_id, db_filepath, energy_score in results:
            track_id = str(track_id)
            if track_id in existing_songs:
                song = existing_songs[track_id]
                song.set_energy_score(energy_score)
                if song.filepath != db_filepath:
                    updates_needed.append((song.filepath, track_id))

        if updates_needed:
            update_filepaths(mydb, updates_needed)

    except mysql.connector.Error as err:
        print(f"Error fetching energy scores: {err}")
    finally:
        cursor.close()

    return existing_songs

def update_filepaths(mydb, updates):
    try:
        sql = "UPDATE songs SET filepath = %s WHERE id = %s"
        cursor = mydb.cursor()
        cursor.executemany(sql, updates)
        mydb.commit()
        print(f"Batch updated {len(updates)} file paths.")
    except mysql.connector.Error as err:
        print(f"Error updating file paths: {err}")
    finally:
        cursor.close()