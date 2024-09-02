import retrieveXML
import dbHandler

from src.Main.audioAnalyser import para_extract

def main():
    xml_file_path = "/Users/oscardilkes/Documents/collection.xml"

    songs = retrieveXML.parse_xml(xml_file_path)

    mycursor = dbHandler.connect_mysql()

    songs = dbHandler.dict_remove_existing(mycursor, songs)

    para_extract(songs)

    dbHandler.update_table(mycursor, songs)

    # TODO implement playlist logic: don't use chatgpt (you can def do it yourself), check xml formatting, update rekordbox xml automatically


if __name__ == "__main__":
        main()