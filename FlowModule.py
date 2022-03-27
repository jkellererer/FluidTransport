import math as mt
import numpy as np
from scipy.optimize import root


class Flow:
    def __init__(self, q, d, nu, epsilon, g = 9.81):
        """

        :param q: flow-rate [m3/s]
        :param d: circular pipe inner diameter [m]
        :param nu: fluid dynamics viscosity [N-s/m2]
        :param epsilon: pipe surface roughness [m]
        :param g: gravitational acceleration [m/s2]
        """
        self.q = q
        self.d = d
        self.nu = nu
        self.epsilon = epsilon
        self.g = g

    def friction_factor_solve(self):
       """Colebrook equation root finding.

       :return: object
       """
       def f(x):
           return -2 * np.log10((2.51 / (Flow.re(self) * np.sqrt(x))) + (self.epsilon / (3.7 * self.d))) - 1.0 / np.sqrt(x)
       solution = root(f, .02)
       return solution

    def friction_factor(self):
        """Solution of Colebrook equation.

        :return: friction factor [-]
        """
        return float(Flow.friction_factor_solve(self).x)

    def friction_factor_success(self):
        """Success indicator of Colebrook equation solver.

        :return: boolean
        """
        return Flow.friction_factor_solve(self).success

    def a(self):  # only for circular pipes
        """

        :return: flow area [m2]
        """
        return mt.pi*self.d**2/4

    def v(self):
        """

        :return: average fluid velocity [m/s]
        """
        return self.q/Flow.a(self)

    def re(self):
        """

        :return: fluid Reynold's Number [-]
        """
        return Flow.v(self)*self.d/self.nu


class MinorLosses(Flow):
    def __init__(self, n_elb45 = 0, n_elb90 = 0, k_other = 0 , *args, **kwargs):  # Add more components here

        self.n_elb45 = n_elb45  # Number of 45 degree elbows.
        self.n_elb90 = n_elb90  # Number of 90 degree elbows.
        self.k_other = k_other  # Sum of loss coefficients not otherwise accounted for.

        super().__init__(*args, **kwargs)

    def k(self):
        """

        :return: summation of loss coefficients [-]
        """
        k_elb45 = self.n_elb45*self.friction_factor()*16
        k_elb90 = self.n_elb90*self.friction_factor()*30

        return k_elb45 + k_elb90 + self.k_other

    def l_m(self):  # Penoncello 4.15
        """

        :return: minor head loss [m]
        """
        return self.k()*self.v()**2/(2*self.g)


class MajorLosses(Flow):
    def __init__(self, lg, *args, **kwargs):
        """

        :param lg: length of straight pipe [m]
        """
        self.lg = lg
        super().__init__(*args, **kwargs)

    def l_f(self):
        """

        :return: frictional (AKA major) head loss [m]
        """
        return self.friction_factor()*self.lg/self.d*self.v()**2/(2*self.g)


class Segment(MinorLosses, MajorLosses):

    def __init__(self, h, *args, **kwargs):
        """

        :param h: static head loss [m]
        """
        self.h = h
        super().__init__(*args, **kwargs)

    def l_t(self):
        """

        :return: total head loss [m]
        """
        return self.l_m() + self.l_f() + self.h



pipe_size = {
    '1_10': 1.097/39.37,
    '1_40': 1.049/39.37,
    '1_80': 0.957/39.37
}
"""
Pipe size dictionary.

D_sc
where 'D' designates nominal pipe size
and 'sc' designates pipe schedule
"""

surface_roughness = {
    'Drawn tubing': 0.0000015,
    'Steel': 0.000046,
    'Concrete': 0.001705
}
"""surface roughness dictionary"""

class CumecConvert:
    def __init__(self, q):
        """

        :param q: input flow-rate
        """
        self.q = q  # input flow-rate

    def gpm(self):
        """Converts from [gpm].

        :return: flow-rate [m3/s]
        """
        return self.q*6.309E-5  # Converts gpm into m3/s.
