"""
Parses a given XML file, containing parameters for the weight estimation of a commercial transport aircraft.
"""

from xml.etree.ElementTree import parse


def parse_xml():
    fp = parse('parameters.xml')
    for method in fp.findall('torenbeek'):
        w_g = method.findtext('w_g')
        print w_g

    # extract data

    # store in parsed data (dictionary)

    # return parsed_data

def main():
    parse_xml()


if __name__ == "__main__":
    main()
