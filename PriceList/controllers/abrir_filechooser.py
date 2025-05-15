from kivy.clock import Clock
from kivymd.uix.snackbar import Snackbar
from kivy.logger import Logger
from plyer import filechooser

from controllers.dbcontroller import DBController
from controllers.utils import get_db_path
try:
    from modules.lector_pdf import LectorTicket
except:
    pass
from modules.listados import productos_por_familia
from controllers.clasificador_controller import ClasificadorPopup

def abrir_filechooser(app):
    try:
        filechooser.open_file(
            title="Selecciona un ticket en formato PDF",
            filters=["*.pdf"],
            on_selection=lambda seleccion: on_archivo_seleccionado(seleccion, app)
        )
    except Exception as e:
        Logger.error(f"FileChooser: Error al abrir el selector de archivos: {e}")

def on_archivo_seleccionado(seleccion, app):
    if not seleccion:
        Logger.info("No se seleccionó ningún archivo.")
        return

    ruta = seleccion[0]
    Logger.info(f"Archivo seleccionado: {ruta}")

    try:
        lector = LectorTicket(ruta)
        db = DBController(get_db_path())

        db.insertarTicket(lector.getFechaTicket())
        ticket_id = db.getUltimoTicket()

        productos_no_clasificados = []

        for producto, precio in lector.cargarDiccionario().items():
            producto_normalizado = producto.strip().lower()
            familia = None

            for key, lista_productos in productos_por_familia.items():
                if any(p.strip().lower() == producto_normalizado for p in lista_productos):
                    familia = key
                    break

            if familia:
                db.insertarProducto(producto, familia)
                db.insertarPrecio(db.getProductoPorNombre(producto), ticket_id, precio)
            else:
                productos_no_clasificados.append((producto, precio))

        for producto, precio in productos_no_clasificados:
            Clock.schedule_once(lambda dt, prod=producto, pre=precio: ClasificadorPopup(app, prod, pre).mostrar(), 0.5)

        Logger.info("Archivo procesado correctamente.")
        Clock.schedule_once(lambda dt: Snackbar(text="Ticket importado correctamente", duration=2).open())

    except Exception as e:
        Logger.error(f"Procesamiento de PDF: Error -> {e}")
        Clock.schedule_once(lambda dt: Snackbar(text="Error al importar el ticket", duration=2).open())
