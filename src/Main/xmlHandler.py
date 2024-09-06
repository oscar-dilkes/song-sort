import os
import xml.etree.ElementTree as ET
from typing import Dict
import song

def parse_xml(file_path):
    failed_songs = []
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

    # extract song data
    for track in root.findall(".//TRACK"):
        track_id = track.get("TrackID")
        title = track.get("Name")
        duration = track.get("TotalTime")
        filepath = track.get("Location")

        if track_id and title and filepath:
            if filepath.startswith("file://localhost"):
                filepath = filepath.replace("file://localhost", "")

            filepath = filepath.replace("%20", " ")

            if os.path.exists(filepath):
                this_song = song.Song(track_id, title, duration, filepath)
                songs.update({track_id: this_song})
            else:
                failed_songs.append({"Track ID": track_id, "Title": title, "Reason": "File not found", "Filepath": filepath})

    return songs, failed_songs

# subsequent two nodes potentially redundant - m3u method used now
def create_playlist(songs: Dict, name):
    # create playlist node
    length = str(len(songs))
    playlist = ET.Element('NODE', {'Name': name, 'Type': "1", 'KeyType': "0", 'Entries': length})

    # add each song to playlist
    for song in songs.values():
        track_id_string = str(song.track_id)
        ET.SubElement(playlist, 'TRACK', {'Key': track_id_string})

    return playlist

def add_all_playlists(file_path, playlists_to_add):
    try:
        # parse xml file to add playlists
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return
    except FileNotFoundError as e:
        print(f"XML not found: {e}")
        return

    playlists = root.find(".//PLAYLISTS")
    if playlists is None:
        print("PLAYLISTS node not found in the XML.")
        return

    # append new playlists
    for playlist in playlists_to_add:
        playlists.append(playlist)

    try:
        tree.write('wip.xml', encoding='utf-8', xml_declaration=True)
    except Exception as e:
        print(f"Error writing XML: {e}")