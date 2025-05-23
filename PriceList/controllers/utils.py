import os
from kivy.utils import platform
from kivy.core.window import Window

def get_db_path():
    if platform == "android":
        ruta_base = "data/pricelist.db"
    else:
        ruta_base = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(ruta_base, "..", "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return os.path.join(data_dir, "pricelist.db")


def actualizar_fuentes(app):
    base_ancho = 360
    ancho_actual = Window.width
    escala = max(min(ancho_actual / base_ancho, 1.8), 1.0)

    app.title_font_size = int(40 * escala)
    app.button_font_size = int(30 * escala)
    app.label_font_size = int(26 * escala)
    app.content_button_size = 120 * escala
    app.content_image_size = 100 * escala
    app.back_button_size = 40 * escala
    app.back_icon_size = 24 * escala
    app.button_radius = 20 * escala
    app.row_height = 150 * escala
