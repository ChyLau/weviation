def w_w(self, w_g, b_ref, Lambda, b, n_ult, s, t_r, unit):
	if unit == 'im':
            k_w = 0.0017
        elif unit == 'si':
            k_w = 0.00667
        else:
            print "USAGE: 'unit' is 'im' or 'si'."

        return k_w*w_g*(b_ref/cos(radians(Lambda)))**0.75*(1 + (b_ref*cos(radians(Lambda))/b)**0.5)*n_ult**0.55*(b*s/(w_g*t_r*cos(radians(Lambda))))**0.3
