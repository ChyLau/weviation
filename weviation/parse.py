"""
Parses a given XML file, containing parameters for the weight estimation of a commercial transport aircraft.
"""

from xml.etree.ElementTree import parse


def parse_xml():
    """
    Stores all the parameters in a dictionary
    """
    fp = parse('parameters.xml')
    data = {}

    for method in fp.findall('torenbeek'):
        for element in method.findall('*'):
            data[element.tag] = float(element.text)

    return data

def main():
    parse_xml()


if __name__ == "__main__":
    main()
