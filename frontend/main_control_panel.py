import tkinter as tk

class ControlPanel(tk.Frame):
    def __init__(self, parent, theme_manager, camera_frame):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.camera_frame = camera_frame
        self.setup_ui()

        # for control panel set up        
    def setup_ui(self):
        # Control buttons frame
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(expand=True)

        # Start button
        self.start_btn = tk.Button(
            self.buttons_frame, text="▶ Start Camera",
            font=('Arial', 14, 'bold'),
            command=self.start_camera,
            relief='flat', cursor='hand2',
            bg='#4CAF50', fg='white', activebackground='#45a049',
            padx=15, pady=8
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Stop button
        self.stop_btn = tk.Button(
            self.buttons_frame, text="⏹ Stop Camera",
            font=('Arial', 14, 'bold'),
            command=self.stop_camera,
            relief='flat', cursor='hand2',
            state='disabled',
            bg='#f44336', fg='white', activebackground='#d32f2f',
            padx=15, pady=8
        )
        self.stop_btn.pack(side=tk.LEFT)

        # Status label
        self.status_label = tk.Label(
            self, text="Camera: Stopped", font=('Arial', 12)
        )
        self.status_label.pack(pady=(10, 0))

    def start_camera(self):
        self.camera_frame.start_camera()
        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        self.status_label.configure(text="Camera: Running")

    def stop_camera(self):
        self.camera_frame.stop_camera()
        self.start_btn.configure(state='normal')
        self.stop_btn.configure(state='disabled')
        self.status_label.configure(text="Camera: Stopped")

    def apply_theme(self, colors):
        self.configure(bg=colors['bg'])
        self.buttons_frame.configure(bg=colors['bg'])
        self.start_btn.configure(bg=colors['accent'], fg='white',
                                 activebackground=colors['accent_hover'])
        self.stop_btn.configure(bg=colors['error'], fg='white',
                                activebackground=colors['error_hover'])
        self.status_label.configure(bg=colors['bg'], fg=colors['text'])