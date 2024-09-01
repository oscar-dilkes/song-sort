import retrieveXML
import audioAnalyser
import pandas as pd

def main():
    xml_file_path = "/Users/oscardilkes/Documents/collection.xml"

    song_file_dict = retrieveXML.parse_xml(xml_file_path)

    if not song_file_dict:
        print("XML parse error.")
        return

    df = pd.DataFrame(song_file_dict.items(), columns=['Title', 'Path'])

    features = audioAnalyser.extract_features(df.iloc[500, 1])

    print(features)


if __name__ == "__main__":
        main()