"""
Parses a given XML file, containing parameters for the weight estimation of a commercial transport aircraft.
"""

from xml.etree.ElementTree import parse


def parse_xml():
    """
    Stores all the parameters in a dictionary
    """
    fp = parse('test.xml')
    data1 = {}

    for method in fp.findall('test'):
        for element in method.findall('*'):
            data1['tor_' + element.tag + '_unit'] = element.get('unit')
        for subelement in method.findall('**'):
            if subelement.tag in data1:
                raise ValueError("In <torenbeek> key %r already exists."% subelement.tag)
            else:
                data1[subelement.tag] = float(subelement.text)


    return data1

def main():
    print parse_xml()


if __name__ == "__main__":
    main()
