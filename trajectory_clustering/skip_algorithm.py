from driver import lat, lon, clustering_criterion, criterion, iter
import distance_calculator

"""
In skip_algorithm,
two GPS points are resulted,
which have skipped adjacent points from intersection-points

"""


def skip(route1, route2, idx1, idx2):
    last1 = len(route1)
    last2 = len(route2)
    index_cluster = []

    # Each point pair from intersection-points
    for index1 in range(idx1, last1):
        point1 = route1[index1]
        lat1 = point1[lat]
        lon1 = point1[lon]
        points = set()

        for index2 in range(1, last2):
            point2 = route2[index2]
            lat2 = point2[lat]
            lon2 = point2[lon]

            # Making a correlated set of point2_number with point1 : set(indexes of point2)
            if distance_calculator.haversine(lat1, lon1, lat2, lon2) < clustering_criterion:
                points.add(index2)

        # If a correlation has been made : list[ index of point1, set(indexes of point2) ]
        if points:
            current_cluster = [{index1}, points]

            # Check 1st iteration
            if index_cluster:

                # If current_cluster needs to be integrated
                # : list[ set(indexes of point1), set(indexes of point2) ]
                if index_cluster[1] & current_cluster[1]:
                    index_cluster[0].update(current_cluster[0])
                    index_cluster[1].update(current_cluster[1])

                # Or no intersection between two clusters
                else:
                    break

            # Set index_cluster
            else:
                index_cluster = current_cluster

        # Or no correlation
        else:
            break

    # Filtering bad clusters & Set to list
    if index_cluster:
        index_cluster[0] = list(index_cluster[0])
        index_cluster[1] = list(index_cluster[1])
        index_cluster[0].sort()
        index_cluster[1].sort()
        index_cluster[1] = sequential_check(index_cluster[1], idx2)

    # Check whether The cluster can be used in direction estimation
    signal = 0

    # If cluster includes first segment of route1
    if index_cluster[0][0] < iter + 1:
        signal = 1
        return [signal, back(route1, route2, index_cluster)]
    # Or if cluster includes last segment of route1
    if index_cluster[0][-1] > last1 - (iter + 1):
        signal = 1
        return [signal, (route1[-1], route2[-1])]

    # If cluster includes first segment or last segment of route2
    if index_cluster[1][0] < iter + 1 or index_cluster[1][-1] > last2 - (iter + 1):
        signal = 1

    return [signal, back(route1, route2, index_cluster)]


# The result removes clusters except only one cluster connected with intersection-point
def sequential_check(point2s, idx2):
    result = []

    for i in range(1, len(point2s)):
        if point2s[i] - point2s[i-1] == 1:
            result.append(point2s[i-1])

        else:
            result.append(point2s[i-1])

            if idx2 in result:
                return result
            else:
                result = []

    result.append(point2s[-1])

    if idx2 in result :
        return result
    else:
        print "seq error"
        exit()


# Back to the adjacent level
def back(route1, route2, cluster):
    points1 = cluster[0]
    points2 = cluster[1]
    points1.reverse()
    points2.reverse()

    for index1 in points1:
        lat1 = route1[index1][lat]
        lon1 = route1[index1][lon]

        for index2 in points2:
            lat2 = route2[index2][lat]
            lon2 = route2[index2][lon]

            if distance_calculator.haversine(lat1, lon1, lat2, lon2) < criterion:
                return route1[index1], route2[index2]

    return 0
