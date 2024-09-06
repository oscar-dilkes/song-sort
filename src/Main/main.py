import os

import xmlHandler
import dbHandler
from itertools import islice
import m3uHandler
from src.Main.audioAnalyser import para_extract

def main(xml_path, output_dir):
    failed_songs = []
    try:
        songs, failed_songs_xml = xmlHandler.parse_xml(xml_path)
        failed_songs.extend(failed_songs_xml)

        # limit songs for testing
        songs = dict(islice(songs.items(), 30))

        db_path = os.path.join(output_dir, "songSort.db")
        conn = dbHandler.connect_sqlite(db_path)

        # split into new and existing (in database)
        new_songs, existing_songs = dbHandler.dict_split_existing(conn, songs)

        # extract audio features & calculate energy score
        failed_songs_analysis = para_extract(new_songs)
        failed_songs.extend(failed_songs_analysis)

        combined_songs = {**new_songs, **existing_songs}

        dbHandler.update_table(conn, new_songs)

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

        m3uHandler.create_m3u_playlist(low_energy, "Low Energy", output_dir)
        m3uHandler.create_m3u_playlist(medium_energy, "Medium Energy", output_dir)
        m3uHandler.create_m3u_playlist(high_energy, "High Energy", output_dir)

        return failed_songs

    except (FileNotFoundError, IOError) as e:
        print(f"Error processing XML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()