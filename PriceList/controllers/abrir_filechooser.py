from kivy.clock import Clock
from kivymd.uix.snackbar import Snackbar
from kivy.logger import Logger
from plyer import filechooser

from controllers.dbcontroller import DBController
from controllers.utils import get_db_path
from modules.lector_pdf import LectorTicket
from modules.listados import productos_por_familia


def abrir_filechooser(app):
    try:
        filechooser.open_file(
            title="Selecciona un archivo PDF",
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
        db_path = get_db_path()
        db = DBController(db_path)

        db.insertarTicket(lector.getFechaTicket())
        ticket_id = db.getUltimoTicket()

        for producto, precio in lector.cargarDiccionario().items():
            producto_normalizado = producto.strip().lower()
            familia = "otraFamilia"

            for key, lista_productos in productos_por_familia.items():
                for p in lista_productos:
                    if p.strip().lower() == producto_normalizado:
                        familia = key
                        break
                else:
                    continue
                break

            if familia != "otraFamilia":
                db.insertarProducto(producto, familia)
                db.insertarPrecio(db.getProductoPorNombre(producto), ticket_id, precio)

        Logger.info("Archivo procesado correctamente.")
        Clock.schedule_once(lambda dt: Snackbar(text="Ticket importado correctamente", duration=2).open())

    except Exception as e:
        Logger.error(f"Procesamiento de PDF: Error -> {e}")
        Clock.schedule_once(lambda dt: Snackbar(text="Error al importar el ticket", duration=2).open())
