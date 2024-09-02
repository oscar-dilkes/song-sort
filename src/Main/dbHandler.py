import mysql.connector

def connect_mysql():
    with open('/Users/oscardilkes/PycharmProjects/songSort/pw', 'r') as file:
        mysql_password = file.read().rstrip()

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password,
        database="songSort"
    )

    mycursor = mydb.cursor()

    if not validate_table(mycursor):
        create_table(mycursor)

    return mycursor

def validate_table(mycursor):
    try:
        mycursor.execute(f"SELECT 1 FROM {"songs"} LIMIT 1;")
        return True
    except:
        return False


def create_table(mycursor):
    mycursor.execute("""
    CREATE TABLE songs (
        id INT PRIMARY KEY,
        title VARCHAR(255),
        filepath VARCHAR(255),
        tempo FLOAT,
        rms FLOAT,
        sc FLOAT,
        zcr FLOAT,
        energy_score INT
    )
    """)

def add_song(mycursor, song):
    sql = """
        INSERT INTO songs (id, title, filepath, tempo, rms, sc, zcr, energy_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
    values = (
        song.track_id,
        song.title,
        song.filepath,
        song.tempo,
        song.rms,
        song.sc,
        song.zcr,
        song.energy_score
    )
    mycursor.execute(sql, values)

def update_table(mycursor, songs):
    for song in songs.values():
        add_song(mycursor, song)


def validate_song(mycursor, track_id):
    sql = "SELECT COUNT(*) FROM songs WHERE id = %s"

    mycursor.execute(sql, (track_id,))

    result = mycursor.fetchone()

    return result[0] > 0

def dict_remove_existing(mycursor, songs):
    keys_to_remove = []

    for track_id in list(songs.keys()):
        if validate_song(mycursor, track_id):
            keys_to_remove.append(track_id)

    for key in keys_to_remove:
        del songs[key]

    return songs