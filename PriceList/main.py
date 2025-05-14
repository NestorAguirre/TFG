from kivymd.app import MDApp

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import NumericProperty
from kivy.core.window import Window

from controllers.abrir_filechooser import abrir_filechooser
from controllers.mostrar_productos import cargar_productos
from controllers.screens_controller import (MenuScreen, cargar_vistas)
from controllers.navegacion_controller import cambiar_pantalla as cambiar_pantalla_controller, volver_atras as volver_atras_controller
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

    def build(self):
        Window.clearcolor = (0.98, 0.95, 0.88, 1)
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name='menu'))

        Clock.schedule_once(self.post_carga_vistas, 0)

        self.historial_pantallas = ["menu"]
        Window.bind(on_resize=lambda *_: actualizar_fuentes(self))
        actualizar_fuentes(self)

        self.date_picker = None

        return self.sm

    def post_carga_vistas(self, dt):
        cargar_vistas(self.sm)

        listado_screen = self.sm.get_screen('listadoproductos')
        self.date_picker = DatePickerController()
        self.date_picker.root = listado_screen

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

    def open(self):
        if self.date_picker:
            self.date_picker.open()


if __name__ == '__main__':
    PriceListApp().run()
