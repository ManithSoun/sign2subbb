class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        
        self.themes = {
            "light": {
                "bg": "#f0f0f0",
                "panel_bg": "#ffffff",
                "text": "#333333",
                "accent": "#4CAF50",
                "accent_hover": "#45a049",
                "error": "#f44336",
                "error_hover": "#d32f2f",
                "primary": "#2196F3",
                "secondary": "#FF9800",
                "border": "#e0e0e0"
            },
            "dark": {
                "bg": "#1a1a1a",
                "panel_bg": "#2d2d2d",
                "text": "#ffffff",
                "accent": "#4CAF50",
                "accent_hover": "#45a049",
                "error": "#f44336",
                "error_hover": "#d32f2f",
                "primary": "#2196F3",
                "secondary": "#FF9800",
                "border": "#404040"
            }
        }
    
    # current theme
    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            
    # get color from theme
    def get_color(self, color_name):
        return self.themes[self.current_theme].get(color_name, "#000000")
    
    # all color
    def get_all_colors(self):
        return self.themes[self.current_theme]