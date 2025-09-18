import tkinter as tk
from tkinter import ttk

class SettingsPanel(tk.Frame):
    def __init__(self, parent, theme_manager, callback):
        super().__init__(parent, width=280)
        self.theme_manager = theme_manager
        self.callback = callback
        
        self.pack_propagate(False)
        self.setup_ui()
    
    # set up setting panel
    def setup_ui(self):
        # Title with icon
        title_frame = tk.Frame(self)
        title_frame.pack(fill=tk.X, pady=(20, 30))
        
        title_label = tk.Label(title_frame, text="⚙️ Settings", 
                             font=('Arial', 18, 'bold'))
        title_label.pack()
        
        # Create sections
        self.create_theme_section()
        self.create_language_section()
        self.create_ai_section()   # 👈 now valid
        self.create_confidence_section()
        self.create_subtitle_section()
        
        spacer = tk.Frame(self, height=20)
        spacer.pack()
        
    # 🎨 Theme section
    def create_theme_section(self):
        theme_frame = tk.LabelFrame(self, text="🎨 Appearance", 
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        theme_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.theme_var = tk.StringVar(value="light")
        
        theme_options = [("☀️ Light Mode", "light"), ("🌙 Dark Mode", "dark")]
        for text, value in theme_options:
            rb = tk.Radiobutton(theme_frame, text=text, variable=self.theme_var,
                              value=value, font=('Arial', 11),
                              command=lambda: self.callback('theme', self.theme_var.get()))
            rb.pack(anchor='w', pady=3)
            
    # 🌐 Language section 
    def create_language_section(self):
        lang_frame = tk.LabelFrame(
            self, text="🌐 Language", 
            font=('Arial', 12, 'bold'), padx=10, pady=10
        )
        lang_frame.pack(fill=tk.X, padx=15, pady=10)

        self.language_var = tk.StringVar(value="english")

        lang_options = [
            ("🇺🇸 English", "english"), 
            ("🇰🇭 ខ្មែរ (Khmer)", "khmer"),
        ]

        for text, value in lang_options:
            rb = tk.Radiobutton(
                lang_frame, text=text, variable=self.language_var,
                value=value, font=('Arial', 11),
                command=lambda: self.callback('language', self.language_var.get())
            )
            rb.pack(anchor='w', pady=3)

    # 🤖 AI Provider section
    def create_ai_section(self):
        ai_frame = tk.LabelFrame(
            self, text="🤖 AI Provider",
            font=('Arial', 12, 'bold'), padx=10, pady=10
        )
        ai_frame.pack(fill=tk.X, padx=15, pady=10)

        self.ai_var = tk.StringVar(value="sealion")  # default

        ai_options = [
            ("🌊  SEA-LION", "sealion"),
        ]

        for text, value in ai_options:
            rb = tk.Radiobutton(
                ai_frame, text=text, variable=self.ai_var,
                value=value, font=('Arial', 11),
                command=lambda: self.callback('ai_provider', self.ai_var.get())
            )
            rb.pack(anchor='w', pady=3)
            
    # 🎯 Confidence section
    def create_confidence_section(self):
        conf_frame = tk.LabelFrame(self, text="🎯 Detection Sensitivity", 
                                 font=('Arial', 12, 'bold'), padx=10, pady=10)
        conf_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.confidence_var = tk.DoubleVar(value=0.7)
        
        scale_frame = tk.Frame(conf_frame)
        scale_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(scale_frame, text="Low", font=('Arial', 9)).pack(side=tk.LEFT)
        tk.Label(scale_frame, text="High", font=('Arial', 9)).pack(side=tk.RIGHT)
        
        conf_scale = tk.Scale(conf_frame, from_=0.1, to=1.0, resolution=0.1,
                            orient=tk.HORIZONTAL, variable=self.confidence_var,
                            command=self.on_confidence_change, length=200)
        conf_scale.pack(fill=tk.X, pady=5)
        
        self.conf_label = tk.Label(conf_frame, text="70%", 
                                 font=('Arial', 11, 'bold'), fg='blue')
        self.conf_label.pack()
        
    # 📝 Subtitle size section
    def create_subtitle_section(self):
        subtitle_frame = tk.LabelFrame(self, text="📝 Subtitle Size", 
                                     font=('Arial', 12, 'bold'), padx=10, pady=10)
        subtitle_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.subtitle_var = tk.StringVar(value="medium")
        
        subtitle_options = [
            ("Small (18px)", "small"), 
            ("Medium (24px)", "medium"), 
            ("Large (32px)", "large")
        ]
        for text, value in subtitle_options:
            rb = tk.Radiobutton(subtitle_frame, text=text, variable=self.subtitle_var,
                              value=value, font=('Arial', 11),
                              command=lambda: self.callback('subtitle_size', self.subtitle_var.get()))
            rb.pack(anchor='w', pady=3)
            
    # Handle confidence change
    def on_confidence_change(self, value):
        confidence = float(value)
        percentage = int(confidence * 100)
        self.conf_label.configure(text=f"{percentage}%")
        self.callback('confidence', confidence)
        
    # Apply theme
    def apply_theme(self, colors):
        self.configure(bg=colors['panel_bg'])
        for widget in self.winfo_children():
            self.update_widget_theme(widget, colors)
            
    # Update widget theme
    def update_widget_theme(self, widget, colors):
        try:
            widget_class = widget.winfo_class()
            if widget_class in ['Frame', 'Labelframe']:
                widget.configure(bg=colors['panel_bg'])
                if widget_class == 'Labelframe':
                    widget.configure(fg=colors['text'])
            elif widget_class in ['Label', 'Radiobutton']:
                widget.configure(bg=colors['panel_bg'], fg=colors['text'])
                if widget_class == 'Radiobutton':
                    widget.configure(selectcolor=colors['panel_bg'])
            elif widget_class == 'Scale':
                widget.configure(
                    bg=colors['panel_bg'], 
                    fg=colors['text'],
                    troughcolor=colors['bg'], 
                    highlightbackground=colors['panel_bg'],
                    activebackground=colors['accent']
                )
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            self.update_widget_theme(child, colors)
