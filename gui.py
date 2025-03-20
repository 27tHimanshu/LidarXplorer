import tkinter as tk
from tkinter import ttk
import winsound
from lidar_processor import load_point_cloud, filter_ground, cluster_objects, find_closest_obstacle
from visualization import visualize_point_cloud, plot_intensity_histogram, plot_data_analysis

class PointCloudAnalyzerGUI:
    def __init__(self, root, file_path):
        self.root = root
        self.file_path = file_path
        self.xyz, self.intensity = load_point_cloud(file_path)
        self.filtered_xyz = filter_ground(self.xyz)
        self.setup_gui()

    def setup_gui(self):
        self.root.title("PointCloud Analyzer")
        self.root.geometry("550x650")
        self.root.configure(bg="#2c3e50")

        # Set theme
        style = ttk.Style()
        style.theme_use('clam')

        # Configure styles
        style.configure("TFrame", background="#2c3e50")
        style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Segoe UI", 10))
        style.configure("TButton", background="#3498db", foreground="#ecf0f1", font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#2980b9")])
        style.configure("TScale", background="#2c3e50", troughcolor="#34495e")

        # Header
        header_label = tk.Label(self.root, text="PointCloud Analyzer",
                                font=("Segoe UI", 20, "bold"),
                                fg="#ecf0f1", bg="#2c3e50",
                                pady=20)
        header_label.pack(fill=tk.X)

        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Parameters frame
        param_frame = ttk.Frame(main_frame)
        param_frame.pack(fill=tk.X, pady=10)

        # Epsilon slider
        eps_frame = ttk.Frame(param_frame)
        eps_frame.pack(fill=tk.X, pady=5)

        eps_label = ttk.Label(eps_frame, text="Epsilon", font=("Segoe UI", 10))
        eps_label.pack(side=tk.LEFT, padx=5)

        self.eps_slider = ttk.Scale(eps_frame, from_=0.1, to=2.0, orient=tk.HORIZONTAL, length=400)
        self.eps_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.eps_slider.set(0.5)  # Default value

        # Min samples slider
        samples_frame = ttk.Frame(param_frame)
        samples_frame.pack(fill=tk.X, pady=5)

        samples_label = ttk.Label(samples_frame, text="Min Samples", font=("Segoe UI", 10))
        samples_label.pack(side=tk.LEFT, padx=5)

        self.min_samples_slider = ttk.Scale(samples_frame, from_=5, to=50, orient=tk.HORIZONTAL, length=400)
        self.min_samples_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.min_samples_slider.set(10)  # Default value

        # Alert display
        self.alert_frame = tk.Frame(main_frame, bg="#44cc44", relief=tk.RAISED, bd=2, padx=10, pady=10)
        self.alert_frame.pack(fill=tk.X, pady=15)

        self.alert_label = tk.Label(self.alert_frame, text="Initializing...",
                                    font=("Segoe UI", 16, "bold"),
                                    bg="#44cc44",
                                    pady=15)
        self.alert_label.pack(fill=tk.X)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create a style for buttons
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=10)

        # Left and right frames for buttons
        left_button_frame = ttk.Frame(button_frame)
        left_button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        right_button_frame = ttk.Frame(button_frame)
        right_button_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        # Visualization buttons
        viz_label = ttk.Label(left_button_frame, text="Visualization", font=("Segoe UI", 12, "bold"))
        viz_label.pack(pady=(0, 10))

        ttk.Button(left_button_frame, text="Raw Point Cloud", command=lambda: visualize_point_cloud(self.xyz, "raw"), style="Action.TButton").pack(fill=tk.X, pady=5)
        ttk.Button(left_button_frame, text="Filtered Point Cloud", command=lambda: visualize_point_cloud(self.filtered_xyz, "filtered"), style="Action.TButton").pack(fill=tk.X, pady=5)
        ttk.Button(left_button_frame, text="Clustered Objects", command=lambda: visualize_point_cloud(self.filtered_xyz, "clustered"), style="Action.TButton").pack(fill=tk.X, pady=5)

        # Analysis buttons
        analysis_label = ttk.Label(right_button_frame, text="Analysis", font=("Segoe UI", 12, "bold"))
        analysis_label.pack(pady=(0, 10))

        ttk.Button(right_button_frame, text="Data Analysis", command=self.run_data_analysis, style="Action.TButton").pack(fill=tk.X, pady=5)
        ttk.Button(right_button_frame, text="Intensity Histogram", command=self.run_intensity_histogram, style="Action.TButton").pack(fill=tk.X, pady=5)

        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        status_label = ttk.Label(status_frame, text=f"File: {self.file_path}", font=("Segoe UI", 8))
        status_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Update alert initially
        self.update_alert()

        # Add slider value displays
        def update_slider_values(event=None):
            eps_value_label.config(text=f"{self.eps_slider.get():.2f}")
            min_samples_value_label.config(text=f"{int(self.min_samples_slider.get())}")
            self.update_alert()

        eps_value_label = tk.Label(eps_frame, text=f"{self.eps_slider.get():.2f}", bg="#2c3e50", fg="#ecf0f1", width=5)
        eps_value_label.pack(side=tk.RIGHT, padx=10)

        min_samples_value_label = tk.Label(samples_frame, text=f"{int(self.min_samples_slider.get())}", bg="#2c3e50", fg="#ecf0f1", width=5)
        min_samples_value_label.pack(side=tk.RIGHT, padx=10)

        self.eps_slider.bind("<Motion>", update_slider_values)
        self.min_samples_slider.bind("<Motion>", update_slider_values)

    def update_alert(self):
        eps = float(self.eps_slider.get())
        min_samples = int(self.min_samples_slider.get())
        _, labels = cluster_objects(self.filtered_xyz, eps, min_samples)
        min_front, min_back, _ = find_closest_obstacle(self.filtered_xyz, labels)

        if min_front < 5 or min_back < 5:
            self.alert_label.config(text=f"🚨 DANGER! STOP!\nFront: {min_front:.2f}m | Back: {min_back:.2f}m")
            self.alert_frame.config(bg="#ff3333")
            winsound.Beep(1000, 500)
        elif min_front < 10 or min_back < 10:
            self.alert_label.config(text=f"⚠️ CAUTION! SLOW DOWN!\nFront: {min_front:.2f}m | Back: {min_back:.2f}m")
            self.alert_frame.config(bg="#ffcc00")
        else:
            self.alert_label.config(text=f"✅ SAFE\nFront: {min_front:.2f}m | Back: {min_back:.2f}m")
            self.alert_frame.config(bg="#44cc44")

        self.alert_label.update()

    def run_data_analysis(self):
        _, labels = cluster_objects(self.filtered_xyz)
        _, _, cluster_sizes = find_closest_obstacle(self.filtered_xyz, labels)
        plot_data_analysis(self.filtered_xyz, labels, cluster_sizes)

    def run_intensity_histogram(self):
        plot_intensity_histogram(self.intensity)