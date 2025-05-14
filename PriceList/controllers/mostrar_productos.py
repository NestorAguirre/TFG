from kivy.logger import Logger
from controllers.dbcontroller import DBController

def cargar_productos(app, familia, nombre_pantalla="listadoproductos"):
    try:
        db = DBController("data/pricelist.db")
        datos = db.getResumenProductosPorFamilia(familia)
        screen = app.sm.get_screen(nombre_pantalla)
        screen.ids.rv.data = datos
    except Exception as e:
        Logger.error(f"Mostrar productos: Error al cargar datos -> {e}")
