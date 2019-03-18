import glob
import re

"""
map_info_extract extracts map information
which consists of list[ list[(number), (index, latitude, longitude, ele, time, hdop, speed)] ]
that is a sequence of GPS points in each trajectory of whole input files
"""


def map_info_extract(input):

    filelist = glob.glob(input + "/*.gpx")
    mapinfo = []
    point = ()
    number = 0
    tmp = [None] * 7

    # Each file
    for file in filelist:
        count = 1
        routeinfo = [number]
        number += 1

        # Each line
        for line in open(file):

            # (index, latitude, longitude, ele, time, hdop, speed)
            if "<trkpt" in line:
                segment = line.split("\"")
                tmp[1] = segment[1]
                tmp[2] = segment[3]

            elif "<ele>" in line:
                tmp[3] = (re.split('[><]', line)[2],)

            elif "<time>" in line:
                tmp[4] = (re.split('[><]', line)[2],)

            elif "<hdop>" in line:
                tmp[5] = (re.split('[><]', line)[2],)

            elif "<speed>" in line:
                tmp[0] = count
                tmp[6] = (re.split('[><]', line)[2],)
                point = tuple(tmp)
                routeinfo.append(point)
                count += 1

        mapinfo.append(routeinfo)

    return mapinfo
