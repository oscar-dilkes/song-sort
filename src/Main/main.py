import xmlHandler
import dbHandler
from itertools import islice
import m3uHandler
from src.Main.audioAnalyser import para_extract

def main():
    xml_file_path = "/Users/oscardilkes/Documents/collection.xml"

    try:
        songs = xmlHandler.parse_xml(xml_file_path)

        # limit songs for testing
        songs = dict(islice(songs.items(), 30))

        mydb = dbHandler.connect_mysql()

        # split into new and existing (in database)
        new_songs, existing_songs = dbHandler.dict_split_existing(mydb, songs)

        # extract audio features & calculate energy score
        para_extract(new_songs)

        combined_songs = {**new_songs, **existing_songs}

        dbHandler.update_table(mydb, new_songs)

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

        m3uHandler.create_m3u_playlist(low_energy, "Low Energy")
        m3uHandler.create_m3u_playlist(medium_energy, "Medium Energy")
        m3uHandler.create_m3u_playlist(high_energy, "High Energy")

    except (FileNotFoundError, IOError) as e:
        print(f"Error processing XML file: {e}")
    except dbHandler.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()