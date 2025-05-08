from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.metrics import Metrics
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy import require
require('2.1.0')

from controllers.dbcontroller import DBController
from modules.lector_pdf import LectorTicket
from datetime import date
from modules.listados import productos_por_familia

class ProductosRecyclerView(BoxLayout):
    producto = StringProperty('')
    precio = StringProperty('')
    maximo = StringProperty('')
    minimo = StringProperty('')
    media = StringProperty('')

# Cargar archivos .kv
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

# Pantallas
class MenuScreen(Screen): pass
class BebidasScreen(Screen): pass
class CuidadoPersonalScreen(Screen): pass
class LimpiezaScreen(Screen): pass
class CongeladosScreen(Screen): pass
class EnvasadosScreen(Screen): pass
class FrescosScreen(Screen): pass
class LacteosScreen(Screen): pass
class DesayunoScreen(Screen): pass

class ListadoProductosScreen(Screen):
    familia_nombre = StringProperty('Familia Final')
    
    def cargar_productos_por_familia(self, familia):
        self.familia_nombre = familia
        db = DBController("pricelist.db")
        productos = db.getResumenProductosPorFamilia(familia)
        self.ids.rv.data = [{
            'producto': p['producto'],
            'precio': p['precio'],
            'maximo': p['maximo'],
            'minimo': p['minimo'],
            'media': p['media']
        } for p in productos]

class PopupImportarArchivo(Popup):
    def __init__(self, al_seleccionar_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.title = "Selecciona un archivo PDF"
        self.size_hint = (0.9, 0.9)
        self.al_seleccionar_callback = al_seleccionar_callback

        layout = BoxLayout(orientation='vertical')
        self.selector_archivos = FileChooserListView(filters=["*.pdf"])
        boton_importar = Button(text="Importar", size_hint_y=None, height=50)
        boton_importar.bind(on_release=self.importar_archivo)

        layout.add_widget(self.selector_archivos)
        layout.add_widget(boton_importar)
        self.add_widget(layout)

    def importar_archivo(self, instancia):
        if self.selector_archivos.selection:
            archivo_seleccionado = self.selector_archivos.selection[0]
            if self.al_seleccionar_callback:
                self.al_seleccionar_callback(archivo_seleccionado)
            self.dismiss()

# Clase principal
class PriceList(App):
    title_font_size = NumericProperty(28)
    button_font_size = NumericProperty(20)
    label_font_size = NumericProperty(16)
    content_button_size = NumericProperty(120)
    content_image_size = NumericProperty(100)
    back_button_size = NumericProperty(40)
    back_icon_size = NumericProperty(24)
    button_radius = NumericProperty(20)
    row_height = NumericProperty(150)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.historial_pantallas = []

    def build(self):
        self.icon = 'assets/images/PriceListLogo.jpg'
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name="menu"))
        self.sm.add_widget(BebidasScreen(name="bebidas"))
        self.sm.add_widget(CuidadoPersonalScreen(name="cuidadopersonal"))
        self.sm.add_widget(LimpiezaScreen(name="limpieza"))
        self.sm.add_widget(CongeladosScreen(name="congelados"))
        self.sm.add_widget(EnvasadosScreen(name="envasados"))
        self.sm.add_widget(FrescosScreen(name="frescos"))
        self.sm.add_widget(LacteosScreen(name="lacteos"))
        self.sm.add_widget(DesayunoScreen(name="desayuno"))
        self.sm.add_widget(ListadoProductosScreen(name="listadoproductos"))
        self.historial_pantallas.append("menu")
        Window.bind(on_resize=self.actualizar_fuentes)
        self.actualizar_fuentes()
        return self.sm

    def actualizar_fuentes(self, *args):
        base_ancho = 360
        ancho_actual = Window.width / Metrics.density
        escala = min(ancho_actual / base_ancho, 1.5)
        
        # Tamaños de texto
        self.title_font_size = 28 * escala
        self.button_font_size = 20 * escala
        self.label_font_size = 16 * escala
        
        # Tamaños de elementos gráficos
        self.content_button_size = 120 * escala
        self.content_image_size = 100 * escala
        self.back_button_size = 40 * escala
        self.back_icon_size = 24 * escala
        self.button_radius = 20 * escala
        self.row_height = 150 * escala

    def cambiar_pantalla(self, nombre_pantalla):
        if self.sm.current != nombre_pantalla:
            self.historial_pantallas.append(self.sm.current)
            self.sm.transition.direction = 'left'
            self.sm.current = nombre_pantalla

    def familia(self, nombre_familia):
        listado_screen = self.sm.get_screen('listadoproductos')
        listado_screen.cargar_productos_por_familia(nombre_familia)
        self.cambiar_pantalla('listadoproductos')

    def volver_atras(self):
        if len(self.historial_pantallas) > 1:
            pantalla_anterior = self.historial_pantallas.pop()
            self.sm.transition.direction = 'right'
            self.sm.current = pantalla_anterior

    def abrir_filechooser(self):
        def al_seleccionar_pdf(ruta):
            print(f"PDF seleccionado: {ruta}")
            lector = LectorTicket(ruta)
            db = DBController("pricelist.db")
            
            db.insertarTicket(date.today())
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
                
                db.insertarProducto(producto, familia)
                db.insertarPrecio(db.getProdutoPorNombre(producto), ticket_id, precio)

        popup = PopupImportarArchivo(al_seleccionar_callback=al_seleccionar_pdf)
        popup.open()

if __name__ == "__main__":
    PriceList().run()
