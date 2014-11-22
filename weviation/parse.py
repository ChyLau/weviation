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
        for element in method.findall('**'):
            if ('tunit' in element.tag) and (element.tag not in data1):
                data1[element.tag] = element.text
            elif ('ttype' in element.tag) and (element.tag not in data1):
                data1[element.tag] = element.text
            elif (('tunit' and 'ttype') not in element.tag) and (element.tag not in data1):
                data1[element.tag] = float(element.text)
            else:
                raise ValueError("In <torenbeek>, key %r already exists." % element.tag)

    for method in fp.findall('raymer'):
        for element in method.findall('**'):
            if ('rtype' in element.tag) and (element.tag not in data2):
                data2[element.tag] = element.text
            elif ('rtype' not in element.tag) and (element.tag not in data2):
                data2[element.tag] = float(element.text)
            else:
                raise ValueError("In <raymer> key, %r already exists." % element.tag)

    for method in fp.findall('gd'):
        for element in method.findall('**'):
            if ('gtype' in element.tag) and (element.tag not in data3):
                data3[element.tag] = element.text
            elif ('gtype' not in element.tag) and (element.tag not in data3):
                data3[element.tag] = float(element.text)
            else:
                raise ValueError("In <gd> key, %r already exists." % element.tag)

    return data1, data2, data3

def main():
    print parse_xml()


if __name__ == "__main__":
    main()
