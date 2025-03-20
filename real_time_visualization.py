import numpy as np
import time
import open3d as o3d
from lidar_processor import filter_ground, cluster_objects

def visualize_frames(data_dir, num_frames=30, eps=0.5, min_samples=10):
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="LiDAR Video", width=800, height=600)

    pcd = o3d.geometry.PointCloud()
    vis.add_geometry(pcd)

    for i in range(num_frames):
        file_path = f"{data_dir}/{i:06d}.bin"  # KITTI format
        print(f"🔹 Loading frame: {file_path}")

        try:
            point_cloud = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
            xyz = point_cloud[:, :3]
            print(f"✅ Loaded {len(xyz)} points")
        except Exception as e:
            print(f"❌ Error loading frame {i}: {e}")
            continue

        if len(xyz) == 0:
            print(f"⚠️ Warning: Frame {i} has 0 points. Skipping...")
            continue

        # Process the frame
        filtered_xyz = filter_ground(xyz)
        print(f"📉 Points after ground filtering: {len(filtered_xyz)}")

        if len(filtered_xyz) == 0:
            print(f"⚠️ Warning: All points removed after ground filtering. Skipping frame {i}.")
            continue

        clustered_points, labels = cluster_objects(filtered_xyz, eps, min_samples)
        print(f"🔍 Points after clustering: {len(clustered_points)}")

        if len(clustered_points) == 0:
            print(f"⚠️ Warning: All points removed after clustering. Skipping frame {i}.")
            continue

        # 🛠️ Fix: Clear and Update Point Cloud Data
        pcd.clear()
        pcd.points = o3d.utility.Vector3dVector(clustered_points)
        pcd.colors = o3d.utility.Vector3dVector(np.random.rand(len(clustered_points), 3))

        # 🛠️ Fix: Update the visualizer correctly
        vis.update_geometry(pcd)
        vis.poll_events()
        vis.update_renderer()

        time.sleep(0.05)  # 🛠️ Fix: Small delay helps rendering

    print("🎥 Visualization complete!")
    vis.destroy_window()
