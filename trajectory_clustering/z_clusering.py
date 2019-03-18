from itertools import combinations
from driver import index, lat, lon, clustering_criterion, time
import distance_calculator

"""
In clustering, every distance among GPS points are supposed to be calculated,
and GPS clusters based on close interval are produced between two trajectories of each pair,
which are comprised of route number and GPS index.
( route_number1, route_number2, list[ tuple( set(GPS indexes of route1), set(GPS indexes of route2) ) ] ),
in which the tuple means GPS cluster and the list means list of the clusters between route1 and route2.
"""


def clustering(mapinfo):
    # Combination
    comb = combinations(mapinfo, 2)
    correlation_list = []

    # Each pair (route1, route2)
    for pair in comb:
        route1 = pair[0]
        route2 = pair[1]
        route1_num = route1[index]
        route2_num = route2[index]
        del route1[index]
        del route2[index]
        index_cluster = ()
        cluster_list = []

        # Each GPS point
        for point1 in route1:
            index1 = point1[index]
            lat1 = point1[lat]
            lon1 = point1[lon]
            points = set()

            for point2 in route2:
                lat2 = point2[lat]
                lon2 = point2[lon]

                # Making a correlated set of point2_number with point1 : set(indexes of point2)
                if distance_calculator.haversine(lat1, lon1, lat2, lon2) < clustering_criterion:
                    points.add(point2[index])

            # If the correlation has been made : tuple( index of point1, set(indexes of point2) )
            if points:
                current_cluster = ({index1}, points)

                # Check index_cluster
                if index_cluster:

                    # If current_cluster needs to be integrated
                    # : tuple( set(indexes of point1), set(indexes of point2) )
                    if index_cluster[1] & current_cluster[1]:
                        index_cluster = (index_cluster[0] | current_cluster[0], index_cluster[1] | current_cluster[1])

                    # Or new cluster created
                    else:
                        cluster_list.append(index_cluster)
                        index_cluster = current_cluster

                else:
                    index_cluster = current_cluster

        # Last cluster added
        if index_cluster:
            cluster_list.append(index_cluster)

        # Filtering bad clusters
        if cluster_list:
            cluster_list = filter(sequential_check, cluster_list)

        # Correlation completed
        if cluster_list:
            correlation_list.append( (route1_num, route2_num, cluster_list) )

        for test in cluster_list:
            one = list(test[0])
            two = list(test[1])
            one.sort()
            two.sort()

            for x in one:
                print route1[x][time]
            print ".........."
            for y in two:
                print route2[y][time]
            print '\n'

        break


def sequential_check(tupl):
    c_list = list(tupl[1])
    c_list.sort()
    return c_list[-1] - c_list[0] + 1 == len(c_list)