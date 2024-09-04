import xmlHandler
import dbHandler

from itertools import islice

import m3uHandler

from src.Main.audioAnalyser import para_extract


def main():
    xml_file_path = "/Users/oscardilkes/Documents/collection.xml"

    songs = xmlHandler.parse_xml(xml_file_path)

    songs = dict(islice(songs.items(), 50))

    mydb = dbHandler.connect_mysql()

    songs = dbHandler.dict_remove_existing(mydb, songs)

    para_extract(songs)

    dbHandler.update_table(mydb, songs)

    filtered_songs = {track_id: song for track_id, song in songs.items() if song.energy_score is not None}

    sorted_songs = dict(sorted(filtered_songs.items(), key=lambda item: item[1].energy_score))

    sorted_items = list(sorted_songs.items())

    total_songs = len(sorted_items)
    split1 = total_songs // 3
    split2 = 2 * total_songs // 3

    low_energy = dict(sorted_items[:split1])
    medium_energy = dict(sorted_items[split1:split2])
    high_energy = dict(sorted_items[split2:])

    # low_energy_playlist = xmlHandler.create_playlist(low_energy, "Low Energy")
    # medium_energy_playlist = xmlHandler.create_playlist(medium_energy, "Medium Energy")
    # high_energy_playlist = xmlHandler.create_playlist(high_energy, "High Energy")
    #
    # xmlHandler.add_all_playlists(xml_file_path, [low_energy_playlist, medium_energy_playlist, high_energy_playlist])

    m3uHandler.create_m3u_playlist(low_energy, "Low Energy")
    m3uHandler.create_m3u_playlist(medium_energy, "Medium Energy")
    m3uHandler.create_m3u_playlist(high_energy, "High Energy")

if __name__ == "__main__":
        main()