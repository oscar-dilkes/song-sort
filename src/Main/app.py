import streamlit as st
import os
import subprocess
from main import main  # Import your main processing function

# Title for the UI
st.title("SongSort")

# File selector for the collection.xml file
collection_file_path = st.file_uploader("Choose your Rekordbox collection.xml file", type="xml")

# File selector for the password config file
password_file_path = st.file_uploader("Choose your MySQL password configuration file", type="txt")

# Directory selector for where to save created playlists
playlist_output_dir = st.text_input("Enter the directory path to save playlists")

# Button to start the process
if st.button("Start Organising"):
    if collection_file_path and password_file_path and playlist_output_dir:
        # Save uploaded files temporarily
        with open("collection.xml", "wb") as f:
            f.write(collection_file_path.getbuffer())

        with open("pw", "wb") as f:
            f.write(password_file_path.getbuffer())

        # Make sure the output directory exists
        if not os.path.exists(playlist_output_dir):
            os.makedirs(playlist_output_dir)

        try:
            # Call the main function and capture any songs that failed to load/analyze
            failed_songs = main(xml_path="collection.xml", password_path="pw", output_dir=playlist_output_dir)

            if failed_songs:
                # Display failed songs in a table
                st.write("### Songs That Failed to Be Analyzed or Loaded")
                st.table(failed_songs)

            st.success("Library organized and playlists created successfully!")

            # Button to open the output directory
            if st.button("Open Playlist Directory"):
                if os.name == 'posix':  # For MacOS and Linux
                    subprocess.run(['open', playlist_output_dir])
                elif os.name == 'nt':  # For Windows
                    subprocess.run(['explorer', playlist_output_dir])

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please provide all the required files and directory paths.")