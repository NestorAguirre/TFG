from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from datetime import date
from kivymd.toast import toast
import logging
import traceback

logging.basicConfig(level=logging.DEBUG)


class KivyDatePicker(Popup):
    def __init__(self, on_date_selected, **kwargs):
        super().__init__(**kwargs)
        self.title = "Seleccionar Fecha"
        self.size_hint = (0.85, 0.6)
        self.auto_dismiss = False
        self.on_date_selected = on_date_selected

        today = date.today()

        # Layout principal
        layout = BoxLayout(orientation='vertical', spacing=15, padding=(20,10,20,10))

        # Título personalizado
        layout.add_widget(Label(
            text="Selecciona una fecha",
            font_size='20sp',
            bold=True,
            size_hint=(1, 0.2),
            halign="center",
            valign="middle"
        ))

        # Cuadrícula para Día/Mes/Año
        grid = GridLayout(cols=2, spacing=10, size_hint=(1, 0.6))

        self.day_spinner = Spinner(
            text=str(today.day),
            values=[str(d) for d in range(1, 32)],
            size_hint=(1, None),
            height="48sp",
            halign='center'
        )
        self.month_spinner = Spinner(
            text=str(today.month),
            values=[str(m) for m in range(1, 13)],
            size_hint=(1, None),
            height="48sp",
            halign='center'
        )
        self.year_spinner = Spinner(
            text=str(today.year),
            values=[str(y) for y in range(today.year - 5, today.year + 1)],
            size_hint=(1, None),
            height="48sp",
            halign='center'
        )

        # Añadir etiquetas y spinners
        grid.add_widget(Label(
            text="Día:", 
            font_size="24sp", 
            size_hint=(1, None), 
            height="48sp",
            halign="center",
            valign="middle"
        ))
        grid.add_widget(self.day_spinner)
        grid.add_widget(Label(
            text="Mes:", 
            font_size="24sp", 
            size_hint=(1, None), 
            height="48sp",
            halign="center",
            valign="middle"
        ))
        grid.add_widget(self.month_spinner)
        grid.add_widget(Label(
            text="Año:", 
            font_size="24sp", 
            size_hint=(1, None), 
            height="48sp",
            halign="center",
            valign="middle"
        ))
        grid.add_widget(self.year_spinner)

        layout.add_widget(grid)

        # Botones
        btn_layout = BoxLayout(size_hint=(1, 0.3), spacing=15, padding=10)

        btn_ok = Button(
            text="Aceptar",
            background_color=(0, 0.6, 0, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True,
            on_release=self.select_date
        )
        btn_cancel = Button(
            text="Cancelar",
            background_color=(0.6, 0, 0, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            bold=True,
            on_release=self.dismiss
        )

        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_ok)

        layout.add_widget(btn_layout)

        self.content = layout

    def select_date(self, instance):
        try:
            selected_date = date(
                int(self.year_spinner.text),
                int(self.month_spinner.text),
                int(self.day_spinner.text)
            )
            self.on_date_selected(selected_date)
            self.dismiss()
        except ValueError:
            error_popup = Popup(
                title="Error",
                content=Label(text="Fecha no válida."),
                size_hint=(0.6, 0.3)
            )
            error_popup.open()

class DatePickerController:
    def __init__(self, app):
        self.app = app
        self.screen = None
        self.fecha_seleccionada = None
        self.current_family = None

    def on_date_selected(self, date_obj):
        try:
            if not isinstance(date_obj, date):
                toast("Error: Tipo de fecha inválido")
                logging.error("Fecha recibida no es instancia de datetime.date")
                return

            fecha_valida = date(date_obj.year, date_obj.month, date_obj.day)

            Clock.schedule_once(lambda dt: self._update_ui(fecha_valida))
            self.fecha_seleccionada = fecha_valida.strftime("%Y-%m-%d")

            if self.current_family:
                Clock.schedule_once(lambda dt: self.app.mostrar_listado_productos(
                    self.current_family,
                    "listadoproductos"
                ))

        except ValueError as ve:
            toast(f"Fecha inválida: {str(ve)}")
            logging.error(f"Error de valor: {ve}")
        except Exception as e:
            toast("Error inesperado")
            logging.critical(f"Error crítico: {str(e)}")
            traceback.print_exc()

    def _update_ui(self, fecha_valida):
        try:
            if self.screen and hasattr(self.screen.ids, 'date'):
                self.screen.ids.date.text = (
                    f"{fecha_valida.day}/{fecha_valida.month}/{fecha_valida.year}"
                )
        except AttributeError as ae:
            logging.error(f"Error actualizando UI: {str(ae)}")

    def open(self):
        try:
            picker = KivyDatePicker(on_date_selected=self.on_date_selected)
            picker.open()
        except Exception as e:
            toast("No se pudo abrir el calendario")
            logging.error(f"Error abriendo datepicker: {str(e)}")
            traceback.print_exc()

    def reset_fecha(self):
        try:
            hoy = date.today()
            self.fecha_seleccionada = hoy.strftime("%Y-%m-%d")
            if self.screen and hasattr(self.screen.ids, 'date'):
                Clock.schedule_once(
                    lambda dt: setattr(
                        self.screen.ids.date,
                        'text',
                        f"{hoy.day}/{hoy.month}/{hoy.year}"
                    )
                )
        except Exception as e:
            logging.error(f"Error reseteando fecha: {str(e)}")
            traceback.print_exc()
