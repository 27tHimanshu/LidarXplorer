import numpy as np

file_path = "C:/Users/himan/Desktop/LIDAR/data/Kitti/training/velodyne/000000.bin"
point_cloud = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
print(f"First 5 points:\n{point_cloud[:5]}")