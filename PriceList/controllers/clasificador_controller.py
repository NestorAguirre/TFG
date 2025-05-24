from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.logger import Logger
from kivy.utils import platform
from kivy.factory import Factory
from kivymd.uix.list import OneLineListItem

from modules.listados import productos_por_familia, FAMILIAS_FIJAS
from controllers.dbcontroller import DBController
from controllers.utils import get_db_path

Builder.load_file("views/clasificador_popup.kv")


class ClasificadorPopup:
    def __init__(self, app, producto, precio, callback=None):
        self.app = app
        self.producto = producto
        self.precio = precio
        self.callback = callback
        self.dialog = None
        self.menu = None
        self.familia_seleccionada = None
        self.button_select = None
        self.label = None

    def mostrar(self):
        self.app.clasificador_popup = self

        layout = Factory.ClasificadorPopupLayout()
        self.label = layout.ids.producto_label
        self.label.text = f"Producto: {self.producto}"
        self.button_select = layout.ids.button_select

        self.dialog = MDDialog(
            title=f"Asignar familia a '{self.producto}'",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=self.cerrar),
                MDFlatButton(text="GUARDAR", on_release=self.guardar)
            ]
        )
        self.dialog.scrim_color = [0, 0, 0, 0]
        self.dialog.elevation = 0
        self.dialog.radius = [0, 0, 0, 0]
        self.dialog.background_color = [0, 0, 0, 0]
        self.dialog.open()

    def abrir_menu(self, instance):
        if not self.menu:
            self.menu = MDDropdownMenu(
                caller=self.button_select,
                items=[
                    {
                        "viewclass": "OneLineListItem",
                        "text": familia,
                        "on_release": lambda x=familia: self.seleccionar_familia(x),
                        "theme_text_color": "Custom",
                        "text_color": [0.1, 0.1, 0.1, 1],
                        "bg_color": [0.9, 0.9, 0.9, 1],
                    }
                    for familia in FAMILIAS_FIJAS
                ],
                width_mult=3,
                background_color=[0, 0, 0, 0],
                max_height=dp(200),
                elevation=0
            )
        self.button_select.parent.do_layout()
        Clock.schedule_once(lambda dt: self.menu.open(), 0.3)

    def seleccionar_familia(self, familia):
        self.familia_seleccionada = familia
        self.button_select.text = familia
        self.menu.dismiss()

    def guardar(self, *args):
        if not self.familia_seleccionada:
            Logger.warning("ClasificadorPopup: No se seleccionó familia.")
            return

        productos_por_familia.setdefault(self.familia_seleccionada, []).append(self.producto)

        if platform == "android":
            db = DBController("data/pricelist.db")
        else:
            db = DBController(get_db_path())
        db.insertarProducto(self.producto, self.familia_seleccionada)
        db.insertarPrecio(db.getProductoPorNombre(self.producto), db.getUltimoTicket(), self.precio)

        Logger.info(f"ClasificadorPopup: '{self.producto}' asignado a familia '{self.familia_seleccionada}'")
        self.cerrar()

    def cerrar(self, *args):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog.bind(on_dismiss=self._al_cerrar_dialogo)

    def _al_cerrar_dialogo(self, *args):
        if self.callback:
            Clock.schedule_once(lambda dt: self.callback(self.app), 0.2)
