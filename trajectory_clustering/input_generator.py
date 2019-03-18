from itertools import combinations
from driver import index, lat, lon, criterion
import skip_algorithm
import distance_calculator
import pymongo

"""
input_generator converts trajectories into input data of direction estimating algorithm,
which results list[ list[ tuples(indexes of routes,intersection-points,last-points) ] ]

"""


def input_generate(mapinfo):

    # Combination
    comb = combinations(mapinfo, 2)
    connection = pymongo.MongoClient("mongodb://Localhost")
    db = connection.input
    users = db.inter
    number = 0

    # Each pair (route1, route2)
    for pair in comb:
        route1 = pair[0]
        route2 = pair[1]
        num1 = len(route1)
        num2 = len(route2)
        index1 = 1
        cluster = [ (route1[index], route2[index]) ]
        print route1[index], route2[index]

        # Each GPS point
        while index1 < num1:
            point1 = route1[index1]
            lat1 = point1[lat]
            lon1 = point1[lon]
            index2 = 1

            while index2 < num2:
                point2 = route2[index2]
                lat2 = point2[lat]
                lon2 = point2[lon]

                # Checking intersection
                if distance_calculator.haversine(lat1, lon1, lat2, lon2) < criterion:

                    # Skip
                    out = skip_algorithm.skip(route1, route2, index1, index2)
                    signal = out[0]
                    last_points = out[1]

                    # Skip check
                    if signal == 0:
                        # Add information of route index
                        cluster_tmp = cluster[:]

                        # Add information of intersection-points
                        cluster_tmp.append( (point1, point2) )

                        # Add information of last-points
                        cluster_tmp.append(last_points)
                        data = {'_id':number, 'index':cluster_tmp[0], 'intersection':cluster_tmp[1],
                                'last':cluster_tmp[2],
                                'route1':[route1[index1+1],route1[index1+2],route1[index1+3],route1[index1+4],route1[index1+5]],
                                'route2_front':[route2[index2+1],route2[index2+2],route2[index2+3],route2[index2+4],route2[index2+5]],
                                'route2_rear':[route2[index2-1],route2[index2-2],route2[index2-3],route2[index2-4],route2[index2-5]]
                        }
                        users.insert(data)
                        number += 1

                    index1 = last_points[0][index]
                    index2 = last_points[1][index]

                    # Reset of point1
                    point1 = route1[index1]
                    lat1 = point1[lat]
                    lon1 = point1[lon]

                index2 += 1

            index1 += 1
