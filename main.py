import tkinter as tk
from tkinter import filedialog
from gui import PointCloudAnalyzerGUI

def main():
    root = tk.Tk()
    root.withdraw()
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