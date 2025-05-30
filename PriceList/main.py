from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.properties import NumericProperty, ObjectProperty
from kivy.core.window import Window

from controllers.abrir_filechooser import abrir_filechooser
from controllers.mostrar_productos import cargar_productos
from controllers.screens_controller import MenuScreen, cargar_vistas
from controllers.navegacion_controller import (
    cambiar_pantalla as cambiar_pantalla_controller,
    volver_atras as volver_atras_controller,
    capturar_tecla_atras,
)
from controllers.utils import actualizar_fuentes
from controllers.selector_fecha_controller import DatePickerController

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
    date_picker = ObjectProperty()

    def build(self):

        Window.clearcolor = (0.98, 0.95, 0.88, 1)
        Window.bind(on_keyboard=capturar_tecla_atras)

        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name="menu"))

        self.date_picker = DatePickerController(app=self)
        self.historial_pantallas = []
        Window.bind(on_resize=lambda *_: actualizar_fuentes(self))
        actualizar_fuentes(self)

        Clock.schedule_once(self.post_carga_vistas, 0)
        Clock.schedule_once(self.forzar_redibujado, 0.1)

        return self.sm

    def post_carga_vistas(self, dt):
        cargar_vistas(self.sm)
        listado_screen = self.sm.get_screen("listadoproductos")
        self.date_picker.screen = listado_screen

    def forzar_redibujado(self, dt):
        self.sm.transition.duration = 0
        self.sm.current = "menu"
        Window.canvas.ask_update()
        self.sm.canvas.ask_update()
        Clock.schedule_once(self.restaurar_transicion, 0.5)

    def restaurar_transicion(self, dt):
        self.sm.transition = SlideTransition(duration=0.3)

    def cambiar_pantalla(self, nombre_pantalla):
        cambiar_pantalla_controller(self, nombre_pantalla)

    def volver_atras(self):
        volver_atras_controller(self)

    def familia(self, nombre_familia):
        pantalla = self.sm.get_screen("listadoproductos")
        pantalla.familia_nombre = nombre_familia
        self.mostrar_listado_productos(nombre_familia, "listadoproductos")

    def mostrar_listado_productos(self, familia, nombre_pantalla):
        cargar_productos(self, familia, nombre_pantalla)

    def abrir_filechooser(self):
        abrir_filechooser(self)

    def open_date_picker(self):
        self.date_picker.open()


if __name__ == "__main__":
    PriceListApp().run()
