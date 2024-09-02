from typing import Dict

import retrieveXML
import audioAnalyser
import pandas as pd
import song

from src.Main.audioAnalyser import extract_features, para_extract

def main():
    xml_file_path = "/Users/oscardilkes/Documents/collection.xml"

    songs = retrieveXML.parse_xml(xml_file_path)

    processed_songs = para_extract(songs)

    energy_scores = [song.energy_score for song in processed_songs if song.energy_score is not None]

    print("low " + str(min(energy_scores)))
    print("mid " + str((max(energy_scores) + min(energy_scores))/2))
    print("high " + str(max(energy_scores)))

    # TODO implement SQL system: reintroduce dictionary, check for song id in xml versus sql, analyse for songs not in db, append to sql
    # TODO implement playlist logic: don't use chatgpt (you can def do it yourself), check xml formatting, update rekordbox xml automatically

    for song in processed_songs:
        print(song.title)

if __name__ == "__main__":
        main()