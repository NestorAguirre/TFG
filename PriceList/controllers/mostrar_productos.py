from kivy.logger import Logger
from kivy.utils import platform

import os

from controllers.utils import get_db_path

try:
    from controllers.dbcontroller import DBController
except:
    print("ERROR IMPORT DBCONTROLLER")
from datetime import date

def cargar_productos(app, familia, nombre_pantalla="listadoproductos"):
    try:
        db = DBController(get_db_path())

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