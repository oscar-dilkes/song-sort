import streamlit as st

from main import main

st.title("SongSort")

number_songs = st.number_input('How many songs would you like to analyse?', min_value=0, max_value=100, value=0, step=1, format='%d')

if st.button("Start Organising"):
    if number_songs:
        try:
            failed_songs = main(number_songs)

            if failed_songs:
                # display failed songs in a table
                st.write("### Songs That Failed to Be Analysed or Loaded")
                st.table(failed_songs)

            st.success("Library organised and playlists created successfully!")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please provide all the required files and directory paths.")