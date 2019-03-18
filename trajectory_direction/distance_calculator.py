from math import radians, cos, sin, asin, sqrt
import driver

"""
haversine calculates distances among GPS points
forked by
http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
"""


def haversine(point1, point2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    lat1 = float(point1[driver.lat].encode('ascii'))
    lon1 = float(point1[driver.lon].encode('ascii'))
    lat2 = float(point2[driver.lat].encode('ascii'))
    lon2 = float(point2[driver.lon].encode('ascii'))
    # convert string to double
    lon1, lat1, lon2, lat2 = float(lon1), float(lat1), float(lon2), float(lat2)
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    m = driver.earthR * c
    return m
