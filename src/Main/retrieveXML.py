import os
import xml.etree.ElementTree as ET

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return {}
    except FileNotFoundError as e:
        print(f"XML not found: {e}")
        return {}
    song_to_path = {}

    for track in root.findall(".//TRACK"):
        title = track.get("Name")
        location = track.get("Location")

        if title and location:
            if location.startswith("file://localhost"):
                location = location.replace("file://localhost", "")

            location = location.replace("%20", " ")

            if os.path.exists(location):
                song_to_path[title] = location
            else:
                print(f"File not found: {title}, {location}")

    return song_to_path
