try:
    from android.permissions import request_permissions, Permission
    from android import activity
    from jnius import autoclass, cast
except:
    pass
from kivy.logger import Logger
from kivy.clock import Clock
from kivymd.toast import toast
from kivy.utils import platform

import os
import pdfplumber

from modules.lector_pdf import LectorTicket
from controllers.dbcontroller import DBController
from controllers.utils import get_db_path, get_familias_path
from controllers.clasificador_controller import ClasificadorPopup


def mostrar_siguiente_popup(app):
    if not app.productos_no_clasificados:
        Logger.info("Todos los productos han sido clasificados.")
        toast("Ticket importado correctamente")
        return

    producto, precio = app.productos_no_clasificados.pop(0)
    popup = ClasificadorPopup(app, producto, precio, callback=mostrar_siguiente_popup)
    Clock.schedule_once(lambda dt: popup.mostrar(), 0.1)
    
def cargar_familias_json():
    import json
    path = get_familias_path()
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if platform == "android":
    def abrir_filechooser(app):
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])
        activity.bind(on_activity_result=lambda requestCode, resultCode, intent: _on_activity_result(requestCode, resultCode, intent, app))

        Intent = autoclass('android.content.Intent')
        intent = Intent(Intent.ACTION_GET_CONTENT)
        intent.setType("application/pdf")
        intent.addCategory(Intent.CATEGORY_OPENABLE)

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivityForResult(intent, 1)


    def _on_activity_result(requestCode, resultCode, intent, app):
        if requestCode == 1 and resultCode == -1:  # RESULT_OK
            try:
                uri = intent.getData()
                context = autoclass('org.kivy.android.PythonActivity').mActivity
                contentResolver = context.getContentResolver()
                inputStream = contentResolver.openInputStream(uri)

                # Verificar tipo MIME
                mimeType = contentResolver.getType(uri)
                if not mimeType or "pdf" not in mimeType.lower():
                    raise Exception(f"Archivo no válido. Tipo detectado: {mimeType}")

                # Obtener nombre del archivo
                DocumentFile = autoclass('androidx.documentfile.provider.DocumentFile')
                docFile = DocumentFile.fromSingleUri(context, uri)
                fileName = docFile.getName()

                if not fileName.endswith(".pdf"):
                    raise Exception("El archivo seleccionado no es un PDF.")

                # Guardar en almacenamiento interno privado
                internal_dir = context.getFilesDir().getAbsolutePath()
                target_path = f"{internal_dir}/{fileName}"

                # Leer el archivo usando InputStream Java y bytearray Python
                buffer = bytearray(1024)
                data = bytearray()

                while True:
                    read_len = inputStream.read(buffer, 0, len(buffer))
                    if read_len == -1:
                        break
                    data.extend(buffer[:read_len])
                inputStream.close()

                with open(target_path, "wb") as f:
                    f.write(data)

                Logger.info(f"Archivo guardado en: {target_path}")
                Logger.info(f"Tamaño archivo guardado: {os.path.getsize(target_path)} bytes")

                with open(target_path, "rb") as f:
                    header = f.read(5)
                Logger.info(f"Encabezado del archivo: {header}")

                # Verificar si se puede abrir con pdfplumber
                try:
                    with pdfplumber.open(target_path) as pdf:
                        Logger.info(f"PDF abierto correctamente, páginas: {len(pdf.pages)}")
                except Exception as e:
                    Logger.error(f"Error al abrir PDF guardado: {e}")
                    raise Exception(f"Error al abrir PDF guardado: {e}")

                _procesar_archivo(target_path, app)

            except Exception as e:
                Logger.error(f"Procesamiento de PDF: Error al copiar archivo -> {e}")
                toast("Error al copiar el archivo")


    def _procesar_archivo(ruta, app):
        Logger.info(f"Procesando archivo: {ruta}")

        try:
            if not os.path.exists(ruta):
                raise FileNotFoundError(f"La ruta no existe: {ruta}")

            lector = LectorTicket(ruta)
            db = DBController(get_db_path())

            db.insertarTicket(lector.getFechaTicket())
            ticket_id = db.getUltimoTicket()

            productos_no_clasificados = []

            familias_dict = cargar_familias_json()

            for producto, precio in lector.cargarDiccionario().items():
                producto_normalizado = producto.strip()
                familia = familias_dict.get(producto_normalizado)

                if familia:
                    db.insertarProducto(producto, familia)
                    db.insertarPrecio(db.getProductoPorNombre(producto), ticket_id, precio)
                else:
                    productos_no_clasificados.append((producto, precio))

            app.productos_no_clasificados = productos_no_clasificados

            if app.productos_no_clasificados:
                Clock.schedule_once(lambda dt: mostrar_siguiente_popup(app))
            else:
                Logger.info("No hay productos sin clasificar.")
            
            toast("Ticket importado correctamente")

        except Exception as e:
            Logger.error(f"Procesamiento de PDF: Error -> {e}")
            toast("Error al importar el ticket")
else:
    from kivy.clock import Clock
    from kivymd.toast import toast
    from kivy.logger import Logger
    from plyer import filechooser

    from controllers.dbcontroller import DBController
    from controllers.utils import get_db_path
    try:
        from modules.lector_pdf import LectorTicket
    except:
        pass
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

            familias_dict = cargar_familias_json()

            for producto, precio in lector.cargarDiccionario().items():
                producto_normalizado = producto.strip()
                familia = familias_dict.get(producto_normalizado)

                if familia:
                    db.insertarProducto(producto, familia)
                    db.insertarPrecio(db.getProductoPorNombre(producto), ticket_id, precio)
                else:
                    productos_no_clasificados.append((producto, precio))

            app.productos_no_clasificados = productos_no_clasificados

            if app.productos_no_clasificados:
                Clock.schedule_once(lambda dt: mostrar_siguiente_popup(app))
            else:
                Logger.info("No hay productos sin clasificar.")
                toast("Ticket importado correctamente")

        except Exception as e:
            Logger.error(f"Procesamiento de PDF: Error -> {e}")
            toast("Error al importar el ticket")

