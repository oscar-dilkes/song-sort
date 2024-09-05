# SongSort

A Python-based tool designed to analyse and organise your Rekordbox music library. This tool parses an XML export from Rekordbox, extracts audio features from each track, computes energy scores, and creates custom playlists based on those scores.

## Features

- **Parse Rekordbox XML Exports**: Reads and processes XML files exported from Rekordbox to extract track metadata.
- **Audio Feature Extraction**: Uses `librosa` to analyse audio files and extract features like tempo, RMS energy, spectral centroid, and zero-crossing rate.
- **Energy Score Calculation**: Computes an energy score for each track based on extracted audio features.
- **Database Management**: Stores and manages track metadata in a MySQL database to keep the library up-to-date.
- **Playlist Creation**: Creates energy-based playlists and exports them back into a format compatible with Rekordbox.

## Requirements

- Python 3.7 or higher
- MySQL Server
- `librosa` library
- `numpy` library
- `mysql-connector-python` library

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/oscar-dilkes/song-sort
   cd song-sort

2. **Install Packages:**

   ```bash
   pip install librosa numpy mysql-connector-python
   
3. **Set Up MySQL Database:**
Make sure you have a MySQL server running and create a database named songSort. Create a user with appropriate permissions and store the password in a file named pw in the project’s root directory:
   ```bash
   /path/to/song-sort/pw
This should contain the password only.

## Usage
1.	**Prepare Rekordbox XML Export:**
Export your Rekordbox library as collection.xml and place in same directory as MySQL password.
2. **Run the Script**:
Run the main script to start organising your Rekordbox library:

   ```bash
   python main.py
   
3.	**Check Outputs:**
- Database: Your tracks will be added to the MySQL database. This ensures that nothing is analysed more that once.
- Playlists: New playlists will be created based on energy scores and exported to .m3u format.

4. **Import to Rekordbox:**
Import the .m3u files to Rekordbox through their UI.

## Project Structure
- main.py: Entry point for running the project.
- xmlHandler.py: Handles XML parsing and playlist creation.
- dbHandler.py: Manages interactions with the MySQL database.
- audioAnalyser.py: Extracts audio features and computes energy scores.
- song.py: Defines the Song class, which represents a track and its attributes.

## Development TODO
- Switch to using [Pyrekordbox]("https://github.com/dylanljones/pyrekordbox") for more seamless integration with Rekordbox.
  - Negates the need to export collection.xml from Rekordbox/import .m3u files back in.
- Use ML to more accurately calculate energy scores.
