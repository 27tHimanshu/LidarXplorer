import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np
def visualize_point_cloud(points, mode="raw"):
    """Visualize the point cloud in 3D."""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    mesh_car = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])
    
    if mode == "raw":
        o3d.visualization.draw_geometries([pcd, mesh_car], window_name="Raw Point Cloud")
    elif mode == "filtered":
        o3d.visualization.draw_geometries([pcd, mesh_car], window_name="Ground Filtered Point Cloud")
    elif mode == "clustered":
        pcd.colors = o3d.utility.Vector3dVector(np.random.rand(len(points), 3))
        o3d.visualization.draw_geometries([pcd, mesh_car], window_name="Clustered Objects")

def plot_intensity_histogram(intensity):
    """Plot the intensity histogram."""
    plt.figure(figsize=(6, 4))
    plt.hist(intensity, bins=30, color='purple', alpha=0.7)
    plt.xlabel("Intensity")
    plt.ylabel("Frequency")
    plt.title("Intensity Histogram")
    plt.show()

def plot_data_analysis(filtered_xyz, labels, cluster_sizes):
    """Plot data analysis (height distribution and cluster sizes)."""
    heights = filtered_xyz[:, 2]
    
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 3, 1)
    plt.hist(heights, bins=30, color='blue', alpha=0.7)
    plt.xlabel("Height (Z)")
    plt.ylabel("Frequency")
    plt.title("Height Distribution of LiDAR Points")
    
    plt.subplot(1, 3, 2)
    plt.bar(range(len(cluster_sizes)), cluster_sizes, color='red', alpha=0.7)
    plt.xlabel("Cluster Index")
    plt.ylabel("Number of Points")
    plt.title("Cluster Size Distribution")
    
    plt.tight_layout()
    plt.show()