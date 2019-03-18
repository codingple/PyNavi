from pymongo import MongoClient
import area_triangle
import distance_calculator
import file_generator
from time import strftime, localtime

# GPX file directory path
input = "C:/trajectories"
output = "C:/output"
# Radius of the Earth
earthR = 6378100.0
# Index
index = 0; lat = 1; lon = 2; ele = 3
time = 4; hdop = 5; speed = 6
# Check iteration number
iter = 5
prob = iter - 2

if __name__ == "__main__":
    start_t = strftime("%Y-%m-%d %I:%M", localtime())
    # Read data from DB
    connection = MongoClient("localhost", 27017)
    db = connection.input
    cursor = db.inter.find()
    output = []
    count = [0,0,0,0]

    # '_id', 'index', 'intersection', 'last', 'route1', 'route2_front', 'route2_rear'
    for doc in cursor:
        intersection = doc['intersection']
        last = doc['last']
        route1 = doc['route1']
        route2_front = doc['route2_front']
        route2_rear = doc['route2_rear']
        index = doc['index']

        # The area of triangle & distance pattern
        area_front = []
        area_rear = []
        weight = []
        distance_front = []
        distance_rear = []
        point1 = intersection[0]
        point2 = route1[0]
        point3_front = route2_front[0]
        point3_rear = route2_rear[0]

        area_front.append(area_triangle.area(point1, point2, point3_front))
        area_rear.append(area_triangle.area(point1, point2, point3_rear))
        distance_front.append(distance_calculator.haversine(point1, point3_front) +
                              distance_calculator.haversine(point2, point3_front))
        distance_rear.append(distance_calculator.haversine(point1, point3_rear) +
                             distance_calculator.haversine(point2, point3_rear))
        weight.append(distance_calculator.haversine(point1, point2))

        # (index, latitude, longitude, ele, time, hdop, speed)
        for i in range(1, iter):
            point1 = route1[i-1]
            point2 = route1[i]
            point3_front = route2_front[i]
            point3_rear = route2_rear[i]

            weight.append(distance_calculator.haversine(point1, point2))
            area_front.append(area_triangle.area(point1, point2, point3_front) * (weight[i - 1] / weight[i]))
            area_rear.append(area_triangle.area(point1, point2, point3_rear) * (weight[i - 1] / weight[i]))
            distance_front.append(distance_calculator.haversine(point1, point3_front) +
                                  distance_calculator.haversine(point2, point3_front))
            distance_rear.append(distance_calculator.haversine(point1, point3_rear) +
                                 distance_calculator.haversine(point2, point3_rear))

        # Correlated direction estimation
        check_front = 0
        check_rear = 0
        dis_front = 0
        dis_rear = 0

        # 0 = F:D, R:D, 1 = F:S, R:D, 2 = F:D, R:S, 3 = F:S, R:S
        result = 0

        for i in range(0,4):
            if area_front[i+1] - area_front[i] > 0:
                check_front += 1
            if area_rear[i+1] - area_rear[i] > 0:
                check_rear += 1
            if distance_front[i+1] - distance_front[i] > 0:
                dis_front += 1
            if distance_rear[i+1] - distance_rear[i] > 0:
                dis_rear += 1

        # Different direction
        if check_front >= prob:
            result += 0
        elif dis_front >= prob:
            result += 0
        # Same direction
        else:
            result += 1

        # Different direction
        if check_rear >= prob:
            result += 0
        elif dis_rear >= prob:
            result += 0
        else:
            result += 2

        # Output
        # (comb_route_index, other_route_index, comb_point_of_route1, comb_point_of_route2)
        if result == 0:
            output.append((index[0], index[1], intersection[0], intersection[1]))
            output.append((index[1], index[0], intersection[1], intersection[0]))
            count[0] += 1

        elif result == 1:
            output.append((index[0], index[1], last[0], last[1]))
            output.append((index[1], index[0], last[1], last[0]))
            count[1] += 1

        elif result == 2:
            output.append((index[0], index[1], intersection[0], intersection[1]))
            output.append((index[1], index[0], last[1], last[0]))
            count[2] += 1
        elif result == 3:
            count[3] += 1
        else:
            print "result error"
            exit(0)

    file_generator.file_generate(output)

    print count
    print "Start Time   ", start_t
    print "Finish Time   ", strftime("%Y-%m-%d %I:%M", localtime())