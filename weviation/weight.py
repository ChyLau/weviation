"""
The weight estimation is done by summing the necessary equations of each method.
"""

import parse as p
import methods

def weight(parsed_data):
    d = parsed_data
    torenbeek = methods.Torenbeek()
    print torenbeek.w_w(d['w_g'], 1, 1, 1, 1, 1, 1, 'im')

def main():
    data = p.parse_xml()
    weight(data)


if __name__ == "__main__":
    main()
