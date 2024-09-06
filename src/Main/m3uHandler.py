import os
from typing import Dict

def create_m3u_playlist(songs: Dict, name, output_dir):
    # Generate the playlist file name with the user-defined output directory
    m3u_file_name = os.path.join(output_dir, f"{name}.m3u")

    try:
        # Open the M3U file for writing in the specified output directory
        with open(m3u_file_name, 'w', encoding='utf-8') as playlist:
            playlist.write('#EXTM3U\n')  # Write the M3U header

            for song in songs.values():
                # Convert to absolute path if necessary
                if not os.path.isabs(song.filepath):
                    song.filepath = os.path.abspath(song.filepath)

                # Write song duration and title
                if song.duration:
                    playlist.write(f"#EXTINF:{song.duration},{song.title}\n")
                else:
                    playlist.write(f"#EXTINF:-1,{song.title}\n")  # Default duration if not provided

                # Write the file path of the song
                playlist.write(f"{song.filepath}\n")

        print(f"Playlist created: {m3u_file_name}")

    except (OSError, IOError) as e:
        print(f"Error creating playlist: {e}")  # Handle file I/O errors