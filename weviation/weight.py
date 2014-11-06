"""
The weight estimation is done by summing the necessary equations of each method.
"""

import parse as p
import methods

def weight(parsed_data):
    d = parsed_data
    torenbeek = methods.Torenbeek()

    print torenbeek.w_w(d['w_g'], d['b_ref'], d['Lambda'], d['b'], d['n_ult'], d['s'], d['t_r'], 'si')

    print torenbeek.w_tail(d['n_ult'], d['s_vtail'], d['s_htail'], 'si')

def main():
    data = p.parse_xml()
    weight(data)


if __name__ == "__main__":
    main()
