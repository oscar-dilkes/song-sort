import streamlit as st
import os
import subprocess
from main import main

st.title("SongSort")

collection_file_path = st.file_uploader("Choose your Rekordbox collection.xml file", type="xml")

playlist_output_dir = st.text_input("Enter the directory path to save playlists")

if st.button("Start Organising"):
    if collection_file_path and playlist_output_dir:
        # save uploaded files temporarily
        with open("collection.xml", "wb") as f:
            f.write(collection_file_path.getbuffer())

        if not os.path.exists(playlist_output_dir):
            os.makedirs(playlist_output_dir)

        try:
            failed_songs = main(xml_path="collection.xml", output_dir=playlist_output_dir)

            if failed_songs:
                # display failed songs in a table
                st.write("### Songs That Failed to Be Analysed or Loaded")
                st.table(failed_songs)

            st.success("Library organised and playlists created successfully!")

            if st.button("Open Playlist Directory"):
                if os.name == 'posix':
                    subprocess.run(['open', playlist_output_dir])
                elif os.name == 'nt':
                    subprocess.run(['explorer', playlist_output_dir])

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please provide all the required files and directory paths.")