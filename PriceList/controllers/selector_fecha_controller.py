from akivymd.uix.datepicker import AKDatePicker
from datetime import date

class DatePickerController:
    def __init__(self, app):
        self.date = AKDatePicker(callback=self.callback, year_range=[2024, 2026])
        self.app = app
        self.screen = None
        self.fecha_seleccionada = None
        self.current_family = None

    def callback(self, date_obj):
        if self.screen and hasattr(self.screen.ids, 'date'):
            self.screen.ids.date.text = f"{date_obj.day}/{date_obj.month}/{date_obj.year}"
        
        self.fecha_seleccionada = f"{date_obj.year}-{date_obj.month:02d}-{date_obj.day:02d}"
        
        if self.current_family:
            self.app.mostrar_listado_productos(self.current_family, "listadoproductos")

    def open(self):
        if self.screen:
            self.date.open()

    def reset_fecha(self):
        hoy = date.today()
        self.fecha_seleccionada = f"{hoy.year}-{hoy.month:02d}-{hoy.day:02d}"
        if self.screen and hasattr(self.screen.ids, 'date'):
            self.screen.ids.date.text = f"{hoy.day}/{hoy.month}/{hoy.year}"