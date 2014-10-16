"""
Parses a given XML file, containing parameters for the weight estimation of a commercial transport aircraft.
"""

from xml.etree.ElementTree import parse


def parse_xml():
    fp = parse('paramters.xml')

    # extract data

    # store in parsed data (dictionary)

    return parsed_data

def main():
    parse_xml()


if __name__ == "__main__":
    main()
