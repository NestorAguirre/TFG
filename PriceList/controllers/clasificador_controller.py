from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.utils import platform
from kivy.logger import Logger

from functools import partial
import json
import os

from modules.listados import FAMILIAS_FIJAS
from controllers.dbcontroller import DBController
from controllers.utils import get_db_path, get_familias_path


class ClasificadorPopup:
    def __init__(self, app, producto, precio, callback=None):
        self.app = app
        self.producto = producto
        self.precio = precio
        self.callback = callback
        self.familia_seleccionada = None
        self.popup = None
        self.spinner = None

    def mostrar(self):
        layout = BoxLayout(orientation='vertical', spacing=15, padding=20)

        label = Label(
            text=f"Producto: {self.producto}",
            size_hint=(1, 0.2),
            font_size="16sp",
            halign='center',
            valign='middle'
        )

        layout.add_widget(label)

        self.spinner = Spinner(
            text="Selecciona familia",
            values=FAMILIAS_FIJAS,
            size_hint=(1, 0.2),
            background_color=(0.9, 0.9, 1, 1)
        )
        self.spinner.bind(text=self.seleccionar_familia)

        layout.add_widget(self.spinner)

        botones = BoxLayout(size_hint=(1, 0.3), spacing=15)

        btn_cancelar = Button(
            text="Cancelar",
            background_color=(0.6, 0, 0, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            on_release=partial(self.cerrar)
        )

        btn_guardar = Button(
            text="Guardar",
            background_color=(0, 0.6, 0, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            on_release=partial(self.guardar)
        )


        botones.add_widget(btn_cancelar)
        botones.add_widget(btn_guardar)
        layout.add_widget(botones)

        self.popup = Popup(
            title=f"Asignar familia a '{self.producto}'",
            content=layout,
            size_hint=(0.9, 0.5),
            auto_dismiss=False
        )
        self.popup.open()

    def seleccionar_familia(self, spinner, value):
        self.familia_seleccionada = value
        Logger.info(f"Familia seleccionada: {value}")

    def guardar(self, *args):
        if not self.familia_seleccionada:
            Logger.warning("ClasificadorPopup: No se seleccionó familia.")
            return
        
        db = DBController(get_db_path())

        db.insertarProducto(self.producto, self.familia_seleccionada)
        db.insertarPrecio(db.getProductoPorNombre(self.producto), db.getUltimoTicket(), self.precio)
        
        RUTA_JSON = get_familias_path()
            
        if os.path.exists(RUTA_JSON):
            with open(RUTA_JSON, "r", encoding="utf-8") as f:
                datos = json.load(f)
        else:
            datos = {}

        datos[self.producto] = self.familia_seleccionada

        with open(RUTA_JSON, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

        Logger.info(f"'{self.producto}' asignado a familia '{self.familia_seleccionada}'")
        self.cerrar()

    def cerrar(self, *args):
        if self.popup:
            self.popup.dismiss()
            Clock.schedule_once(lambda dt: self._al_cerrar_popup(), 0.1)

    def _al_cerrar_popup(self):
        if self.callback:
            self.callback(self.app)
