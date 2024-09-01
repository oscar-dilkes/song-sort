import os
import xml.etree.ElementTree as ET
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

    songs = []

    for track in root.findall(".//TRACK"):
        title = track.get("Name")
        filepath = track.get("Location")

        if title and filepath:
            if filepath.startswith("file://localhost"):
                filepath = filepath.replace("file://localhost", "")

            filepath = filepath.replace("%20", " ")

            if os.path.exists(filepath):
                this_song = song.Song(title, filepath)
                songs.append(this_song)
            # else:
            #     print(f"File not found: {title}, {filepath}")

    return songs
