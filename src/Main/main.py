
from itertools import islice
from venv import create

import rekordbox_handler
import db_handler
from rekordbox_handler import create_new_playlist
from src.Main.audio_analyser import para_extract

def main(number_songs):
    failed_songs = []
    try:
        rdb, songs, failed_songs_xml = rekordbox_handler.get_songs()
        failed_songs.extend(failed_songs_xml)

        # limit songs for testing
        songs = dict(islice(songs.items(), number_songs))

        db_path = "/Users/oscardilkes/Documents/songSort/songSort.db"
        conn = db_handler.connect_sqlite(db_path)

        # split into new and existing (in database)
        new_songs, existing_songs = db_handler.dict_split_existing(conn, songs)

        print("dog")

        # extract audio features & calculate energy score
        failed_songs_analysis = para_extract(new_songs)
        print("cat")

        failed_songs.extend(failed_songs_analysis)

        combined_songs = {**new_songs, **existing_songs}

        db_handler.update_table(conn, new_songs)

        filtered_songs = {track_id: song for track_id, song in combined_songs.items() if song.energy_score is not None}

        sorted_songs = dict(sorted(filtered_songs.items(), key=lambda item: item[1].energy_score))
        sorted_items = list(sorted_songs.items())

        # determine split points for energy levels
        total_songs = len(sorted_items)
        split1 = total_songs // 3
        split2 = 2 * total_songs // 3

        low_energy = dict(sorted_items[:split1])
        medium_energy = dict(sorted_items[split1:split2])
        high_energy = dict(sorted_items[split2:])

        create_new_playlist(rdb, low_energy, "Low Energy")
        create_new_playlist(rdb, medium_energy, "Medium Energy")
        create_new_playlist(rdb, high_energy, "High Energy")

        return failed_songs

    except (FileNotFoundError, IOError) as e:
        print(f"Error processing XML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main(30)