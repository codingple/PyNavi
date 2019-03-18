from math import fabs
from driver import lat, lon


def area(point1, point2, point3):
    a = float(point1[lat].encode('ascii'))
    b = float(point1[lon].encode('ascii'))
    c = float(point2[lat].encode('ascii'))
    d = float(point2[lon].encode('ascii'))
    e = float(point3[lat].encode('ascii'))
    f = float(point2[lon].encode('ascii'))

    return 0.5 * fabs((a*d) + (c*f) + (e*b) - (a*f) - (e*d) - (c*b))