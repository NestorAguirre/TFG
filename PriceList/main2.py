from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.metrics import Metrics
from kivy.utils import platform
from kivy.logger import Logger

from plyer import filechooser

from views.main import KV_MAIN
from views.frescos import KV_FRESCOS
from views.bebidas import KV_BEBIDAS
from views.congelados import KV_CONGELADOS
from views.cuidadopersonal import KV_CUIDADOPERSONAL
from views.desayuno import KV_DESAYUNO
from views.envasados import KV_ENVASADOS
from views.lacteos import KV_LACTEOS
from views.limpieza import KV_LIMPIEZA
from views.listadoproductos import KV_LISTADOPRODUCTOS

from modules.listados import productos_por_familia
from controllers.dbcontroller import DBController

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
        Builder.load_string(KV_MAIN)
        Builder.load_string(KV_FRESCOS)
        Builder.load_string(KV_LIMPIEZA)
        Builder.load_string(KV_BEBIDAS)
        Builder.load_string(KV_CONGELADOS)
        Builder.load_string(KV_CUIDADOPERSONAL)
        Builder.load_string(KV_DESAYUNO)
        Builder.load_string(KV_ENVASADOS)
        Builder.load_string(KV_LACTEOS)
        Builder.load_string(KV_LISTADOPRODUCTOS)

        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(FrescosScreen(name='frescos'))
        self.sm.add_widget(LimpiezaScreen(name='limpieza'))
        self.sm.add_widget(BebidasScreen(name='bebidas'))
        self.sm.add_widget(CongeladosScreen(name='congelados'))
        self.sm.add_widget(CuidadoPersonalScreen(name='cuidadopersonal'))
        self.sm.add_widget(DesayunoScreen(name='desayuno'))
        self.sm.add_widget(EnvasadosScreen(name='envasados'))
        self.sm.add_widget(LacteosScreen(name='lacteos'))
        self.sm.add_widget(ListadoProductosScreen(name='listadoproductos'))

        self.historial_pantallas = ["menu"]
        Window.bind(on_resize=self.actualizar_fuentes)
        self.actualizar_fuentes()
        return self.sm

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
            db = DBController("data/pricelist.db")
            datos = db.getResumenProductosPorFamilia(familia)
            screen = self.sm.get_screen(screen_name)
            screen.ids.rv.data = datos
        except Exception as e:
            Logger.error(f"Mostrar productos: Error al cargar datos -> {e}")

    def actualizar_fuentes(self, *args):
        base_ancho = 360
        densidad = Metrics.density
        ancho_actual = Window.width / densidad
        escala = min(ancho_actual / base_ancho, 1.5)

        self.title_font_size = int(28 * escala)
        self.button_font_size = int(20 * escala)
        self.label_font_size = int(16 * escala)
        self.content_button_size = 120 * escala
        self.content_image_size = 100 * escala
        self.back_button_size = 40 * escala
        self.back_icon_size = 24 * escala
        self.button_radius = 20 * escala
        self.row_height = 150 * escala

    def abrir_filechooser(self):
        if platform == "android":
            try:
                filechooser.open_file(
                    title="Selecciona un archivo PDF",
                    filters=["*.pdf"],
                    on_selection=self.on_archivo_seleccionado
                )
            except Exception as e:
                Logger.error(f"FileChooser: Error al abrir el selector de archivos: {e}")
        else:
            Logger.info("FileChooser: Esta función solo está implementada para Android por ahora.")

    def on_archivo_seleccionado(self, seleccion):
        if not seleccion:
            Logger.info("No se seleccionó ningún archivo.")
            return

        ruta = seleccion[0]
        Logger.info(f"Archivo seleccionado: {ruta}")

        try:
            from controllers.dbcontroller import DBController
            from modules.lector_pdf import LectorTicket

            lector = LectorTicket(ruta)
            db = DBController("data/pricelist.db")

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

# Clase personalizada usada por RecycleView
class ProductosRecyclerView(BoxLayout):
    producto = StringProperty("")
    precio = StringProperty("")
    maximo = StringProperty("")
    minimo = StringProperty("")
    media = StringProperty("")

if __name__ == '__main__':
    PriceListApp().run()
