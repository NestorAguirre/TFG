from kivy.logger import Logger
from kivy.utils import platform
import os

try:
    from controllers.dbcontroller import DBController
except:
    print("ERROR IMPORT DBCONTROLLER")
from datetime import date

def cargar_productos(app, familia, nombre_pantalla="listadoproductos"):
    try:
        if platform == "android":
            db = DBController("data/pricelist.db")
        else:
            ruta_absoluta_db = os.path.join(os.path.dirname(__file__), "..", "data", "pricelist.db")
            db = DBController(os.path.abspath(ruta_absoluta_db))

        app.date_picker.current_family = familia
        
        if app.date_picker.fecha_seleccionada:
            fecha_limite = app.date_picker.fecha_seleccionada
        else:
            fecha_limite = date.today().strftime("%Y-%m-%d")

        datos = db.getResumenProductosPorFamilia(familia, fecha_limite)
        screen = app.sm.get_screen(nombre_pantalla)
        
        screen.ids.rv.data = []
        screen.ids.rv.refresh_from_data()
        screen.ids.rv.data = datos
        
    except Exception as e:
        Logger.error(f"Mostrar productos: Error al cargar datos -> {e}")