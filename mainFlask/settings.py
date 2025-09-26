class Settings:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.__class__._initialized = True

    @classmethod
    def Instance(cls):
        return cls()
    
    highlight_colors = [
    "#0074D9",  # Teal
    "#e6194b",  # Red
    "#f58231",  # Orange
    "#d4b800",  # Yellow
    "#3cb44b",  # Green
    "#4363d8",  # Blue
    "#911eb4",  # Purple
    "#f032e6",  # Pink
    "#9A6324",  # Brown
    "#808080",  # Gray
    ]

    _color_index = 0

    def _get_next_color(self):
        cycled_color = self.highlight_colors[self._color_index % len(self.highlight_colors)]
        self._color_index = self._color_index + 1
        return cycled_color
    
