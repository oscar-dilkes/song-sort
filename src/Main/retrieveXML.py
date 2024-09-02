import os
import xml.etree.ElementTree as ET
from typing import Dict

import song

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return {}
    except FileNotFoundError as e:
        print(f"XML not found: {e}")
        return {}

    songs: Dict[str, song.Song] = dict()

    for track in root.findall(".//TRACK"):
        track_id = track.get("TrackID")
        title = track.get("Name")
        filepath = track.get("Location")

        if track_id and title and filepath:
            if filepath.startswith("file://localhost"):
                filepath = filepath.replace("file://localhost", "")

            filepath = filepath.replace("%20", " ")

            if os.path.exists(filepath):
                this_song = song.Song(track_id, title, filepath)
                songs.update({track_id : this_song})
            # else:
            #     print(f"File not found: {title}, {filepath}")

    return songs
