# controllers/selector_fecha_controller.py

from akivymd.uix.datepicker import AKDatePicker

class DatePickerController:
    def __init__(self):
        self.date = AKDatePicker(callback=self.callback, year_range=[2024, 2026])
        self.root = None  # Se asignará desde main

    def callback(self, date):
        if self.root:
            self.root.ids.date.text = '' if not date else f"{date.day}/{date.month}/{date.year}"

    def open(self):
        self.date.open()
