import os
from typing import Dict

def create_m3u_playlist(songs: Dict, name, output_dir):
    m3u_file_name = os.path.join(output_dir, f"{name}.m3u")

    try:
        with open(m3u_file_name, 'w', encoding='utf-8') as playlist:
            playlist.write('#EXTM3U\n')  # Write the M3U header

            for song in songs.values():
                # convert to absolute path
                if not os.path.isabs(song.filepath):
                    song.filepath = os.path.abspath(song.filepath)

                if song.duration:
                    playlist.write(f"#EXTINF:{song.duration},{song.title}\n")
                else:
                    # default duration if not provided
                    playlist.write(f"#EXTINF:-1,{song.title}\n")

                playlist.write(f"{song.filepath}\n")

        print(f"Playlist created: {m3u_file_name}")

    except (OSError, IOError) as e:
        print(f"Error creating playlist: {e}")