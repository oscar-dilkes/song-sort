import os
from typing import Dict

def create_m3u_playlist(songs: Dict, name):
    # generate playlist file name
    m3u_file_name = f"{name}.m3u"

    try:
        with open(m3u_file_name, 'w', encoding='utf-8') as playlist:
            playlist.write('#EXTM3U\n')

            for song in songs.values():
                # if not absolute convert to absolute
                if not os.path.isabs(song.filepath):
                    song.filepath = os.path.abspath(song.filepath)

                if song.duration:
                    playlist.write(f"#EXTINF:{song.duration},{song.title}\n")
                else:
                    playlist.write(f"#EXTINF:-1,{song.title}\n")

                playlist.write(f"{song.filepath}\n")

    except (OSError, IOError) as e:
        print(f"Error creating playlist: {e}")