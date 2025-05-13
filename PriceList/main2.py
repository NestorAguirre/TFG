from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.utils import platform
from kivy.logger import Logger

from plyer import filechooser
import os

from modules.listados import productos_por_familia
from controllers.dbcontroller import DBController

# Pantallas
class MenuScreen(Screen): pass
class BebidasScreen(Screen): familia_nombre = StringProperty("Bebidas")
class CuidadoPersonalScreen(Screen): familia_nombre = StringProperty("Cuidado Personal")
class LimpiezaScreen(Screen): familia_nombre = StringProperty("Limpieza")
class CongeladosScreen(Screen): familia_nombre = StringProperty("Congelados")
class EnvasadosScreen(Screen): familia_nombre = StringProperty("Envasados")
class FrescosScreen(Screen): familia_nombre = StringProperty("Frescos")
class LacteosScreen(Screen): familia_nombre = StringProperty("Lácteos")
class DesayunoScreen(Screen): familia_nombre = StringProperty("Desayuno")
class ListadoProductosScreen(Screen): familia_nombre = StringProperty("")
class ProductosRecyclerView(BoxLayout):
    producto = StringProperty("")
    precio = StringProperty("")
    maximo = StringProperty("")
    minimo = StringProperty("")
    media = StringProperty("")

# Cargar archivos KV
Builder.load_file("views/main.kv")
Builder.load_file("views/bebidas.kv")
Builder.load_file("views/cuidadopersonal.kv")
Builder.load_file("views/limpieza.kv")
Builder.load_file("views/congelados.kv")
Builder.load_file("views/envasados.kv")
Builder.load_file("views/frescos.kv")
Builder.load_file("views/lacteos.kv")
Builder.load_file("views/desayuno.kv")
Builder.load_file("views/listadoproductos.kv")

# Función para obtener la ruta a la base de datos de forma compatible
def get_db_path():
    if platform == "android":
        from android.storage import app_storage_path
        ruta_base = app_storage_path()
    else:
        ruta_base = os.path.dirname(os.path.abspath(__file__))

    data_dir = os.path.join(ruta_base, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return os.path.join(data_dir, "pricelist.db")

class PriceListApp(MDApp):
    title_font_size = NumericProperty(28)
    button_font_size = NumericProperty(20)
    label_font_size = NumericProperty(16)
    content_button_size = NumericProperty(120)
    content_image_size = NumericProperty(100)
    back_button_size = NumericProperty(40)
    back_icon_size = NumericProperty(24)
    button_radius = NumericProperty(20)
    row_height = NumericProperty(150)

    def build(self):
        Window.clearcolor = (0.98, 0.95, 0.88, 1)
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name='menu'))

        Clock.schedule_once(self.cargar_vistas, 0)

        self.historial_pantallas = ["menu"]
        Window.bind(on_resize=self.actualizar_fuentes)
        self.actualizar_fuentes()
        return self.sm

    def cargar_vistas(self, dt):
        self.sm.add_widget(FrescosScreen(name='frescos'))
        self.sm.add_widget(LimpiezaScreen(name='limpieza'))
        self.sm.add_widget(BebidasScreen(name='bebidas'))
        self.sm.add_widget(CongeladosScreen(name='congelados'))
        self.sm.add_widget(CuidadoPersonalScreen(name='cuidadopersonal'))
        self.sm.add_widget(DesayunoScreen(name='desayuno'))
        self.sm.add_widget(EnvasadosScreen(name='envasados'))
        self.sm.add_widget(LacteosScreen(name='lacteos'))
        self.sm.add_widget(ListadoProductosScreen(name='listadoproductos'))

    def cambiar_pantalla(self, nombre_pantalla):
        if self.sm.current != nombre_pantalla:
            self.historial_pantallas.append(self.sm.current)
            self.sm.transition.direction = 'left'
            self.sm.current = nombre_pantalla

    def volver_atras(self):
        if len(self.historial_pantallas) > 1:
            pantalla_anterior = self.historial_pantallas.pop()
            self.sm.transition.direction = 'right'
            self.sm.current = pantalla_anterior

    def familia(self, nombre_familia):
        pantalla = self.sm.get_screen("listadoproductos")
        pantalla.familia_nombre = nombre_familia
        self.mostrar_listado_productos(nombre_familia, "listadoproductos")

    def mostrar_listado_productos(self, familia, screen_name):
        try:
            db_path = get_db_path()
            db = DBController(db_path)
            datos = db.getResumenProductosPorFamilia(familia)
            screen = self.sm.get_screen(screen_name)
            screen.ids.rv.data = datos
        except Exception as e:
            Logger.error(f"Mostrar productos: Error al cargar datos -> {e}")

    def actualizar_fuentes(self, *args):
        base_ancho = 360
        ancho_actual = Window.width
        escala = max(min(ancho_actual / base_ancho, 1.8), 1.0)

        self.title_font_size = int(40 * escala)
        self.button_font_size = int(30 * escala)
        self.label_font_size = int(26 * escala)
        self.content_button_size = 120 * escala
        self.content_image_size = 100 * escala
        self.back_button_size = 40 * escala
        self.back_icon_size = 24 * escala
        self.button_radius = 20 * escala
        self.row_height = 150 * escala

    def abrir_filechooser(self):
        try:
            filechooser.open_file(
                title="Selecciona un archivo PDF",
                filters=["*.pdf"],
                on_selection=self.on_archivo_seleccionado
            )
        except Exception as e:
            Logger.error(f"FileChooser: Error al abrir el selector de archivos: {e}")

    def on_archivo_seleccionado(self, seleccion):
        if not seleccion:
            Logger.info("No se seleccionó ningún archivo.")
            return

        ruta = seleccion[0]
        Logger.info(f"Archivo seleccionado: {ruta}")

        try:
            from modules.lector_pdf import LectorTicket

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

if __name__ == '__main__':
    PriceListApp().run()
