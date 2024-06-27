import sys
import math
from collections import deque
data = []
def get_distance(point1, point2):
    return math.sqrt((point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)

def range_query(point, eps):
    neighbors = []
    for p in data:
        if get_distance(point, p) <= eps:
            neighbors.append(p)
    return neighbors

def DBSCAN(eps, min_pts):
    clusters = []
    noise = set()
    label = {point: None for point in data}
    cluster_id = 0

    for point in data:
        if label[point] is not None:
            continue

        neighbors = range_query(point, eps)
        if len(neighbors) < min_pts:
            label[point] = 'Noise'
            noise.add(point)
            continue

        cluster_id += 1# 클러스터id 증가시키기
        cluster = []
        clusters.append(cluster)
        cluster.append(point)
        label[point] = cluster_id

        seed_set = deque(neighbors)
        seed_set.remove(point) # 본인 제거

        while seed_set:
            current_point = seed_set.popleft() #큐에서 하나 꺼내기
            if label[current_point] == 'Noise': #Noise면 클러스터에 추가
                label[current_point] = cluster_id
                cluster.append(current_point)
            if label[current_point] is not None:#이미 클러스터에 속해있으면
                continue
            label[current_point] = cluster_id
            cluster.append(current_point)

            current_neighbors = range_query(current_point, eps)
            if len(current_neighbors) >= min_pts:
                for neighbor in current_neighbors:
                    seed_set.append(neighbor)

    return clusters

def main():
    if len(sys.argv) != 5:
        print("ERROR: Please input 4 arguments. data file name, n, Eps and MinPts are required!!")
        return
    
    input_filename = sys.argv[1]
    n = int(sys.argv[2])
    eps = float(sys.argv[3])
    min_pts = int(sys.argv[4])
    
    with open(input_filename, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            object_id = parts[0]
            x = float(parts[1])
            y = float(parts[2])
            data.append((object_id, x, y))
            
    #Density Based Clustering 시작
    clusters = DBSCAN(eps, min_pts)

    #top-n cluster만 남기기
    clusters.sort(key=len, reverse=True)
    clusters = clusters[:n]
    
    base_filename = input_filename.rsplit('.', 1)[0]  # Remove file extension
    for i in range(min(n, len(clusters))):
        with open(f'{base_filename}_cluster_{i}.txt', 'w') as file:
            for point in clusters[i]:
                file.write(f'{point[0]}\n')

if __name__ == "__main__":
    main()
