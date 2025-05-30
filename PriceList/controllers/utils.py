import os
import shutil

from kivy.utils import platform
from kivy.core.window import Window


import os
from kivy.utils import platform

def get_db_path():
    if platform == "android":
        from android.storage import app_storage_path
        ruta_base = app_storage_path()
    else:
        ruta_base = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(ruta_base, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "pricelist.db")


def get_familias_path():
    if platform == "android":
        from android.storage import app_storage_path
        ruta_base = app_storage_path()
        default_path = "assets/familias_default.json"
    else:
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        default_path = os.path.join(ruta_base, "..", "assets", "familias_default.json")

    data_dir = os.path.join(ruta_base, "data")
    os.makedirs(data_dir, exist_ok=True)

    familias_path = os.path.join(data_dir, "familias.json")

    if not os.path.exists(familias_path):
        try:
            shutil.copy(default_path, familias_path)
        except Exception as e:
            print(f"Error copiando archivo por primera vez: {e}")

    return familias_path

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
