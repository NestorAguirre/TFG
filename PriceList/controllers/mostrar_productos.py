from kivy.logger import Logger
from kivymd.toast import toast

from controllers.utils import get_db_path, get_familias_path

try:
    from controllers.dbcontroller import DBController
except:
    print("ERROR IMPORT DBCONTROLLER")
from datetime import date
import os
import json

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

def cargar_productos_generales(app):
    try:
        db = DBController(get_db_path())

        datos = db.getProductosFamilias()
        screen = app.sm.get_screen("listadoproductosgeneral")
        
        screen.ids.rv_general.data = []
        screen.ids.rv_general.refresh_from_data()
        screen.ids.rv_general.data = datos
        
    except Exception as e:
        Logger.error(f"Mostrar productos generales: Error al cargar datos -> {e}")
        
def guardar_productos_generales(app):
    # Accede al RecycleView
    screen = app.sm.get_screen("listadoproductosgeneral")
    rv = screen.ids.rv_general

    # rv.data es la lista de filas
    
        
    RUTA_JSON = get_familias_path()
        
    if os.path.exists(RUTA_JSON):
        with open(RUTA_JSON, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = {}
    
    for fila in rv.data:
        producto = str(fila.get('producto', ''))
        familia = str(fila.get('familia', ''))
        datos[producto] = familia
        db = DBController(get_db_path())
        db.actualizar_familia(producto, familia)

    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
        
    toast("Familias actualizadas correctamente")
        
def actualizar_familia(self, producto, nueva_familia):
    screen = self.sm.get_screen("listadoproductosgeneral")
    rv = screen.ids.rv_general

    for i, fila in enumerate(rv.data):
        if fila['producto'] == producto and fila['familia'] != nueva_familia:
            rv.data[i]['familia'] = nueva_familia
            break