from kivy.logger import Logger

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
    for fila in rv.data:
        producto = fila.get('producto', '')
        familia = fila.get('familia', '')
        print(f"Producto: {producto}, Familia: {familia}")