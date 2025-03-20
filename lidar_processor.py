import numpy as np
from sklearn.cluster import DBSCAN

def load_point_cloud(file_path):
    """Load LiDAR data from a .bin file."""
    point_cloud = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
    xyz = point_cloud[:, :3]
    intensity = point_cloud[:, 3]
    return xyz, intensity

def filter_ground(xyz, z_threshold=-1.2):
    """Filter ground points based on a height threshold."""
    return xyz[xyz[:, 2] > z_threshold]

def cluster_objects(points, eps=0.5, min_samples=10):
    """Cluster objects using DBSCAN."""
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
    labels = clustering.labels_
    return points, labels

def find_closest_obstacle(points, labels):
    """Find the closest obstacle in front and behind."""
    unique_labels = set(labels)
    min_front, min_back = float('inf'), float('inf')
    cluster_sizes = []
    for label in unique_labels:
        if label == -1:  # Ignore noise
            continue
        cluster_points = points[labels == label]
        cluster_sizes.append(len(cluster_points))
        avg_x = np.mean(cluster_points[:, 0])  # X coordinate
        if avg_x > 0:
            min_front = min(min_front, avg_x)
        else:
            min_back = min(min_back, abs(avg_x))
    return min_front, min_back, cluster_sizes