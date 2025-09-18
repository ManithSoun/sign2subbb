import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading
from tkinter import ttk 

class CameraFrame(tk.Frame):
    def __init__(self, parent, theme_manager, gesture_detector):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.gesture_detector = gesture_detector

        self.is_running = False
        self.cap = None
        self.current_subtitle = ""
        self.current_confidence = 0.0
        self.subtitle_size = "medium"
        self.language = "english"

        self.setup_ui()

    def setup_ui(self):
        self.camera_container = tk.Frame(self, bg='black', relief='solid', bd=2)
        self.camera_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.camera_label = tk.Label(self.camera_container, bg='black', text="📷 Camera Off",
                                   font=('Arial', 18), fg='white')
        self.camera_label.pack(fill=tk.BOTH, expand=True)

        # Subtitle container (semi-transparent style)
        self.subtitle_container = tk.Frame(self, height=80, bg='#000000')
        self.subtitle_container.pack(fill=tk.X, side=tk.BOTTOM)
        self.subtitle_container.pack_propagate(False)
        
        self.subtitle_label = tk.Label(
            self.subtitle_container,
            text="Ready for gesture recognition...",
            font=('Arial', 24, 'bold'),
            fg='white', bg='#000000', wraplength=800, justify='center'
        )
        self.subtitle_label.pack(expand=True, pady=5)

        # Confidence as a progress bar
        self.confidence_bar = ttk.Progressbar(
            self.subtitle_container, orient="horizontal",
            length=400, mode="determinate"
        )
        self.confidence_bar.pack(pady=5)


    def set_language(self, language):
        self.language = language

    def start_camera(self):
        if not self.is_running:
            self.is_running = True
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.update_subtitle("Camera error", 0.0)
                return

            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            self.camera_thread = threading.Thread(target=self.camera_loop)
            self.camera_thread.daemon = True
            self.camera_thread.start()

            self.update_subtitle("Camera started - Show your hand gesture", 0.0)

    def stop_camera(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.camera_label.configure(image='', text="📷 Camera Off")
        self.update_subtitle("Camera stopped", 0.0)

    def camera_loop(self):
        gesture_history = []
        stable_gesture = None
        stable_count = 0
        frame_count = 0

        while self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                continue

            frame_count += 1
            frame = cv2.flip(frame, 1)

            processed_frame, detected_gesture, confidence = self.gesture_detector.process_frame(frame)

            if detected_gesture is not None:
                gesture_history.append(detected_gesture)
                if len(gesture_history) > 5:
                    gesture_history.pop(0)

                most_common = max(set(gesture_history), key=gesture_history.count)
                if gesture_history.count(most_common) >= 2:
                    if stable_gesture != most_common:
                        stable_gesture = most_common
                        stable_count = 0
                    stable_count += 1

                    if stable_count >= 2:
                        gesture_text = self.gesture_detector.get_gesture_text(stable_gesture, self.language)
                        self.current_subtitle = gesture_text
                        self.current_confidence = confidence
            else:
                gesture_history.clear()
                stable_gesture = None
                stable_count = 0
                if frame_count % 30 == 0:
                    self.current_subtitle = "Show your hand gesture..."
                    self.current_confidence = 0.0

            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb).resize((640, 480))
            frame_tk = ImageTk.PhotoImage(frame_pil)

            try:
                self.camera_label.configure(image=frame_tk, text="")
                self.camera_label.image = frame_tk
                self.update_subtitle(self.current_subtitle, self.current_confidence)
            except tk.TclError:
                break

    def update_subtitle(self, text, confidence):
        try:
            if text:
                self.subtitle_label.configure(text=text)
                if confidence > 0:
                    self.confidence_bar["value"] = confidence * 100
                else:
                    self.confidence_bar["value"] = 0
            else:
                self.subtitle_label.configure(text="Ready for gesture recognition...")
                self.confidence_bar["value"] = 0
        except tk.TclError:
            pass


    def apply_theme(self, colors):
        self.configure(bg=colors['bg'])
        self.camera_container.configure(bg='black', highlightbackground=colors['border'])
        self.subtitle_container.configure(bg=colors['panel_bg'], highlightbackground=colors['border'])
        self.subtitle_label.configure(bg=colors['panel_bg'], fg=colors['text'])

        # Style ttk.Progressbar to match theme
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=colors['panel_bg'],
            background=colors['accent'],  # bar color
            thickness=20
        )
        self.confidence_bar.configure(style="Custom.Horizontal.TProgressbar")

