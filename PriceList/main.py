from kivy.utils import platform

import os
if platform == "android":
    os.environ["SDL_AUDIODRIVER"] = "android"

if platform == "android":
    try:
        from android.storage import app_storage_path
        db_path = os.path.join(app_storage_path(), "pricelist.db")
    except ImportError:
        db_path = os.path.join("data", "pricelist.db")
else:
    db_path = os.path.join("data", "pricelist.db")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.core.window import Window
from kivy.metrics import Metrics
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy import require
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.pickers import MDDatePicker
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
        db = DBController(db_path)
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

class PriceList(MDApp):
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
        self.kv_loaded = set()  # Para trackear archivos .kv cargados

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        self.icon = 'assets/images/PriceListLogo.png'
        self.sm = ScreenManager()
        
        # Cargar solo la pantalla principal al inicio
        self.cargar_kv('main')
        self.sm.add_widget(MenuScreen(name="menu"))
        
        # No añadir otras pantallas aquí
        self.historial_pantallas.append("menu")
        Window.bind(on_resize=self.actualizar_fuentes)
        self.actualizar_fuentes()
        return self.sm

    def cargar_kv(self, nombre_kv):
        if nombre_kv not in self.kv_loaded:
            Builder.load_file(f"views/{nombre_kv}.kv")
            self.kv_loaded.add(nombre_kv)

    def get_date(self, instance, value, date_range):
        print(f"Fecha seleccionada: {str(value)}")

    def on_cancel(self, instance, value):
        print("Selección cancelada")

    def show_date_picker(self):
        date_dialog = MDDatePicker(size_hint=(0.8, 0.6))
        date_dialog.bind(on_save=self.get_date, on_cancel=self.on_cancel)
        date_dialog.open()

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

    def cambiar_pantalla(self, nombre_pantalla):
        if self.sm.current != nombre_pantalla:
            # Mapeo de nombres de pantalla a archivos .kv y clases
            pantallas_config = {
                "bebidas": ("bebidas", BebidasScreen),
                "cuidadopersonal": ("cuidadopersonal", CuidadoPersonalScreen),
                "limpieza": ("limpieza", LimpiezaScreen),
                "congelados": ("congelados", CongeladosScreen),
                "envasados": ("envasados", EnvasadosScreen),
                "frescos": ("frescos", FrescosScreen),
                "lacteos": ("lacteos", LacteosScreen),
                "desayuno": ("desayuno", DesayunoScreen),
                "listadoproductos": ("listadoproductos", ListadoProductosScreen)
            }

            # Cargar .kv y crear pantalla si no existe
            if nombre_pantalla in pantallas_config:
                kv_file, screen_class = pantallas_config[nombre_pantalla]
                
                # 1. Cargar el archivo .kv primero
                self.cargar_kv(kv_file)
                
                # 2. Crear y añadir pantalla solo si no existe
                if not self.sm.has_screen(nombre_pantalla):
                    screen = screen_class(name=nombre_pantalla)
                    self.sm.add_widget(screen)

            # Manejar pantallas especiales
            elif nombre_pantalla == "menu":
                # Pantalla principal ya existe
                pass
            else:
                print(f"Error: Pantalla {nombre_pantalla} no configurada")
                return

            # 3. Realizar transición
            self.historial_pantallas.append(self.sm.current)
            self.sm.transition.direction = 'left'
            self.sm.current = nombre_pantalla

    def familia(self, nombre_familia):
        # Primero asegúrate de que la pantalla existe y está configurada
        self.cambiar_pantalla('listadoproductos')
        
        # Ahora recupera la pantalla
        listado_screen = self.sm.get_screen('listadoproductos')
        listado_screen.cargar_productos_por_familia(nombre_familia)

    def volver_atras(self):
        if len(self.historial_pantallas) > 1:
            pantalla_anterior = self.historial_pantallas.pop()
            self.sm.transition.direction = 'right'
            self.sm.current = pantalla_anterior

    def abrir_filechooser(self):
        def al_seleccionar_pdf(ruta):
            lector = LectorTicket(ruta)
            db = DBController(db_path)
            
            db.insertarTicket(lector.getFechaTicket())
            ticket_id = db.getUltimoTicket()
            
            productos_nuevos = []
            
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
                    db.insertarPrecio(db.getProdutoPorNombre(producto), ticket_id, precio)
                else:
                    productos_nuevos.append(producto)
                
            for producto in productos_nuevos:
                print(f"¿A qué familia pertenece el producto {producto}?")
                familia = "SinClasificar"
                db.insertarProducto(producto, familia)
                db.insertarPrecio(db.getProdutoPorNombre(producto), ticket_id, precio)
                
        popup = PopupImportarArchivo(al_seleccionar_callback=al_seleccionar_pdf)
        popup.open()

if __name__ == "__main__":
    PriceList().run()