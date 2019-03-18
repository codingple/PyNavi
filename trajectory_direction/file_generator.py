import glob
import driver

# Index
index = 0; lat = 1; lon = 2; ele = 3
time = 4; hdop = 5; speed = 6


# (comb_route_index, other_route_index, comb_point_of_route1, comb_point_of_route2)
def file_generate(info):
    count = 0
    filelist = glob.glob(driver.input + "/*.gpx")

    # Each file
    for comb in info:
        route1 = filelist[comb[0]]
        route2 = filelist[comb[1]]
        lat1 = comb[2][lat]
        lon1 = comb[2][lon]
        lat2 = comb[3][lat]
        lon2 = comb[3][lon]
        file = open(driver.output + "/" + str(count) + ".gpx", 'w')
        switch = 0

        # Route1
        for line in open(route1):
            if "<trkpt" in line:
                segment = line.split("\"")
                if lat1 == segment[1] and lon1 == segment[3]:
                    break
            file.write(line.encode('ascii'))

        # Route2
        for line in open(route2):
            if switch == 0:
                if "<trkpt" in line:
                    segment = line.split("\"")
                    if lat2 == segment[1] and lon2 == segment[3]:
                        switch = 1
                        file.write(line.encode('ascii'))

            else:
                file.write(line.encode('ascii'))

        file.close()
        count += 1
        print count
