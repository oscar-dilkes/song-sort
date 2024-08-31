import xml.etree.ElementTree as ET
import pandas as pd

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    song_to_path = {}

    for track in root.findall(".//TRACK"):
        title = track.get("Name")
        location = track.get("Location")

        if title and location:
            song_to_path[title] = location

    return song_to_path

def main():
    xml_file_path = "/Users/oscardilkes/Documents/collection.xml"

    song_file_dict = parse_xml(xml_file_path)

    df = pd.DataFrame(song_file_dict.items(), columns=['Title', 'Path'])

    print(df)



if __name__ == "__main__":
        main()