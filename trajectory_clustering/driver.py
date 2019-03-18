import extractor
import input_generator
from time import strftime, localtime

# GPX file directory path
input = "C:/trajectories"
# Radius of the Earth
earthR = 6378100.0
# Index
index = 0; lat = 1; lon = 2; ele = 3
time = 4; hdop = 5; speed = 6
# Distance criterion
criterion = 10
clustering_criterion = 100
# Check iteration number
iter = 5


if __name__ == "__main__":
    start_t = strftime("%Y-%m-%d %I:%M", localtime())

    # Map information
    mapinfo = extractor.map_info_extract(input)

    # Clustering
    result = input_generator.input_generate(mapinfo)

    print "Start Time   ", start_t
    print "Finish Time   ", strftime("%Y-%m-%d %I:%M", localtime())
    print "done"
