"""
Parses a given XML file, containing parameters for the weight estimation of a commercial transport aircraft.
"""

from xml.etree.ElementTree import parse


def parse_xml():
    """
    Stores all the parameters in a dictionary
    """
    fp = parse('parameters_nasa.xml')
    data = {}

    for method in fp.findall('torenbeek'):
        for element in method.findall('*'):
            if element.tag in data:
                raise ValueError("Key %r already exists."% element.tag)
            else:
                data[element.tag] = float(element.text)

    for method in fp.findall('raymer'):
        for element in method.findall('*'):
            if element.tag in data:
                raise ValueError("Key %r already exists." % element.tag)
            else:
                data[element.tag] = float(element.text)

    for method in fp.findall('gd'):
        for element in method.findall('*'):
            if element.tag in data:
                raise ValueError("Key %r already exists." % element.tag)
            else:
                data[element.tag] = float(element.text)

    return data

def main():
    print parse_xml()


if __name__ == "__main__":
    main()
