import os
from typing import Dict

from pyrekordbox import Rekordbox6Database
from pyrekordbox.db6 import DjmdPlaylist
from pyrekordbox.db6.aux_files import MasterPlaylistXml

import song

def get_songs():
    rdb = Rekordbox6Database()
    songs: Dict[str, song.Song] = dict()
    failed_songs = []
    for content in rdb.get_content():
        track_id = content.ID
        title = content.Title if content.Title else "Unknown Title"
        duration = content.Length
        file_path = content.FolderPath if content.FolderPath else ""

        if os.path.exists(file_path):
            this_song = song.Song(track_id, title, duration, file_path)
            songs.update({track_id: this_song})
        else:
            failed_songs.append(
                {"Track ID": track_id, "Title": title, "Reason": "File not found", "Filepath": file_path})

    return rdb, songs, failed_songs

def create_new_playlist(rdb: Rekordbox6Database, songs, playlist_name):
    playlist: DjmdPlaylist = rdb.create_playlist(playlist_name)
    mxml = MasterPlaylistXml()
    print(MasterPlaylistXml.get_playlists(mxml))
    rdb.commit()
    for track_id in songs:
        rdb.add_to_playlist(playlist, track_id)
        rdb

    rdb.commit()
    rdb.close()

