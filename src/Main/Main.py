import retrieveXML
import audioAnalyser
import pandas as pd

from src.Main.audioAnalyser import extract_features, para_extract


def main():
    xml_file_path = "/Users/oscardilkes/Documents/collection.xml"

    songs = retrieveXML.parse_xml(xml_file_path)

    processed_songs = para_extract(songs)

    for song in processed_songs:
        print(song.title)

if __name__ == "__main__":
        main()