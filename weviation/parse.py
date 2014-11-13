"""
Parses a given XML file, containing parameters for the weight estimation of a commercial transport aircraft.
"""

from xml.etree.ElementTree import parse


def parse_xml():
    """
    Stores all the parameters in a dictionary
    """
    fp = parse('parameters.xml')
    data1 = {}
    data2 = {}
    data3 = {}

    for method in fp.findall('torenbeek'):
        for element in method.findall('*'):
            if element.tag in data1:
                raise ValueError("In <torenbeek> key %r already exists."% element.tag)
            else:
                data1[element.tag] = float(element.text)

    for method in fp.findall('raymer'):
        for element in method.findall('*'):
            if element.tag in data2:
                raise ValueError("In <raymer> key %r already exists." % element.tag)
            else:
                data2[element.tag] = float(element.text)

    for method in fp.findall('gd'):
        for element in method.findall('*'):
            if element.tag in data3:
                raise ValueError("In <gd> key %r already exists." % element.tag)
            else:
                data3[element.tag] = float(element.text)

    return data1, data2, data3

def main():
    print parse_xml()


if __name__ == "__main__":
    main()
