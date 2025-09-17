import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import threading
import queue
from gui.main_window import MainWindow

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()