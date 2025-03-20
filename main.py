# main.py
import tkinter as tk
from tkinter import filedialog, messagebox
from gui import PointCloudAnalyzerGUI
from real_time_visualization import visualize_frames

def main():
    root = tk.Tk()
    root.withdraw()

    # Ask the user what they want to do
    choice = messagebox.askyesno("Choose Mode", "Do you want real-time visualization? (Yes) or GUI mode? (No)")

    if choice:  # Real-time visualization
        data_dir = filedialog.askdirectory(title="Select the folder containing LiDAR .bin files")
        if not data_dir:
            print("❌ No folder selected. Exiting...")
            exit()
        visualize_frames(data_dir, num_frames=30)  # Adjust num_frames as needed
    else:  # GUI mode
        file_path = filedialog.askopenfilename(
            title="Select a KITTI LiDAR .bin file",
            filetypes=[("LiDAR Files", "*.bin")]
        )
        if not file_path:
            print("❌ No file selected. Exiting...")
            exit()

        gui_root = tk.Tk()
        app = PointCloudAnalyzerGUI(gui_root, file_path)
        gui_root.mainloop()

if __name__ == "__main__":
    main()