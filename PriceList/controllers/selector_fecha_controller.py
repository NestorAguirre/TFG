from kivymd.uix.pickers import MDDatePicker
from datetime import date
from kivymd.uix.snackbar import Snackbar

class DatePickerController:
    def __init__(self, app):
        self.app = app
        self.screen = None
        self.fecha_seleccionada = None
        self.current_family = None

    def on_date_selected(self, date_obj):
        if not date_obj:
            Snackbar(text="No se seleccionó una fecha válida.").open()
            return

        try:
            fecha_valida = date(date_obj.year, date_obj.month, date_obj.day)
        except ValueError:
            Snackbar(text="Fecha inválida seleccionada.").open()
            return

        if self.screen and hasattr(self.screen.ids, 'date'):
            self.screen.ids.date.text = f"{fecha_valida.day}/{fecha_valida.month}/{fecha_valida.year}"

        self.fecha_seleccionada = fecha_valida.strftime("%Y-%m-%d")

        if self.current_family:
            self.app.mostrar_listado_productos(self.current_family, "listadoproductos")

    def open(self):
        date_picker = MDDatePicker(
            year=date.today().year,
            month=date.today().month,
            day=date.today().day,
        )
        date_picker.bind(on_save=lambda instance, value, date_range: self.on_date_selected(value))
        date_picker.open()

    def reset_fecha(self):
        hoy = date.today()
        self.fecha_seleccionada = hoy.strftime("%Y-%m-%d")
        if self.screen and hasattr(self.screen.ids, 'date'):
            self.screen.ids.date.text = f"{hoy.day}/{hoy.month}/{hoy.year}"
