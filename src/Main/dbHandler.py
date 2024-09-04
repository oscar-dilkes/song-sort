import mysql.connector

def connect_mysql():
    with open('/Users/oscardilkes/PycharmProjects/songSort/pw', 'r') as file:
        mysql_password = file.read().rstrip()

    # Establish database connection
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="songSort"
    )

    # Check if the table exists, if not, create it
    if not validate_table(mydb):
        create_table(mydb)

    return mydb

def validate_table(mydb):
    # Use a buffered cursor to handle the result set properly
    mycursor = mydb.cursor(buffered=True)
    try:
        # Check if the 'songs' table exists
        mycursor.execute("SELECT 1 FROM songs LIMIT 1;")
        mycursor.close()  # Close cursor after use
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mycursor.close()  # Ensure cursor is closed in case of error
        return False

def create_table(mydb):
    mycursor = mydb.cursor()
    # Create the 'songs' table if it doesn't exist
    mycursor.execute("""
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
    mycursor.close()  # Close cursor after use

def add_song(mydb, song):
    mycursor = mydb.cursor()
    # Insert song data into the table
    sql = """
        INSERT INTO songs (id, title, duration, filepath, tempo, rms, sc, zcr, energy_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        song.track_id,
        song.title,
        int(song.duration) if song.duration is not None else 0,
        song.filepath,
        float(song.tempo) if song.tempo is not None else 0.0,  # Default to 0.0 if None
        float(song.rms) if song.rms is not None else 0.0,      # Default to 0.0 if None
        float(song.sc) if song.sc is not None else 0.0,        # Default to 0.0 if None
        float(song.zcr) if song.zcr is not None else 0.0,      # Default to 0.0 if None
        int(song.energy_score) if song.energy_score is not None else 0  # Default to 0 if None
    )
    mycursor.execute(sql, values)
    mydb.commit()  # Commit the transaction
    mycursor.close()  # Close cursor after use

def update_table(mydb, songs):
    for song in songs.values():
        add_song(mydb, song)

def validate_song(mydb, track_id):
    # Use a buffered cursor to handle the result set properly
    mycursor = mydb.cursor(buffered=True)
    sql = "SELECT COUNT(*) FROM songs WHERE id = %s"
    mycursor.execute(sql, (track_id,))
    result = mycursor.fetchone()
    mycursor.close()  # Close cursor after fetching result
    return result[0] > 0

def dict_split_existing(mydb, songs):
    # Initialize two dictionaries
    new_songs = {}
    existing_songs = {}

    # Iterate through the songs and split them based on their existence in the database
    for track_id, song in songs.items():
        if validate_song(mydb, track_id):
            # Song exists in the database
            existing_songs[track_id] = song
        else:
            # Song does not exist in the database
            new_songs[track_id] = song

    # Fetch energy scores for the songs that are already in the database
    existing_songs = fetch_energy_scores(mydb, existing_songs)

    return new_songs, existing_songs

def fetch_energy_scores(mydb, existing_songs):
    track_ids = list(existing_songs.keys())

    if not track_ids:
        return existing_songs

    query = "SELECT id, filepath, energy_score FROM songs WHERE id IN (%s)" % ','.join(['%s'] * len(track_ids))

    cursor = mydb.cursor()
    cursor.execute(query, track_ids)
    results = cursor.fetchall()
    cursor.close()

    updates_needed = []

    for track_id, db_filepath, energy_score in results:
        track_id = str(track_id)
        if track_id in existing_songs:
            song = existing_songs[track_id]
            song.set_energy_score(energy_score)
            if song.filepath != db_filepath:
                updates_needed.append((song.filepath, track_id))

    if updates_needed:
        update_filepaths(mydb, updates_needed)
    return existing_songs

def update_filepaths(mydb, updates):
    sql = "UPDATE songs SET filepath = %s WHERE id = %s"
    cursor = mydb.cursor()

    cursor.executemany(sql, updates)
    mydb.commit()
    cursor.close()
    print(f"Batch updated {len(updates)} file paths.")
