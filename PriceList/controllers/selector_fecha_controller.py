from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
from datetime import date
import logging
import traceback

logging.basicConfig(level=logging.DEBUG)

class KivyDatePicker(Popup):
    def __init__(self, on_date_selected, **kwargs):
        super().__init__(**kwargs)
        self.title = "Seleccionar fecha"
        self.size_hint = (0.85, None)
        self.height = dp(280)
        self.auto_dismiss = False
        self.background = ""
        self.on_date_selected = on_date_selected
        self.separator_color = [1, 0.4, 0.4, 1]
        self.title_color = [1, 1, 1, 1]
        self.title_size = dp(20)

        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=[dp(20), dp(10), dp(20), dp(20)],
            md_bg_color=[0.95, 0.95, 0.95, 1]
        )

        header = MDLabel(
            text=self.title,
            halign="center",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(30)
        )
        main_layout.add_widget(header)

        spinners_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(15),
            size_hint=(1, None),
            height=dp(60),
            pos_hint={"center_x": 0.5}
        )

        today = date.today()

        self.day_field = MDTextField(
            text=str(today.day),
            hint_text="Día",
            mode="rectangle",
            size_hint=(None, None),
            width=dp(80),
            height=dp(48),
            font_size=dp(18),
            padding=(dp(10), dp(12), dp(10), dp(12)),
            readonly=False
        )
        self.day_menu = MDDropdownMenu(
            caller=self.day_field,
            items=[{"text": str(d), "on_release": lambda x=str(d): self.set_day(x)} for d in range(1, 32)],
            width_mult=4
        )
        self.day_field.bind(on_release=self.day_menu.open)
        spinners_layout.add_widget(self.day_field)

        self.month_field = MDTextField(
            text=str(today.month),
            hint_text="Mes",
            mode="rectangle",
            size_hint=(None, None),
            width=dp(80),
            height=dp(48),
            font_size=dp(18),
            padding=(dp(10), dp(12), dp(10), dp(12)),
            readonly=False
        )
        self.month_menu = MDDropdownMenu(
            caller=self.month_field,
            items=[{"text": str(m), "on_release": lambda x=str(m): self.set_month(x)} for m in range(1, 13)],
            width_mult=4
        )
        self.month_field.bind(on_release=self.month_menu.open)
        spinners_layout.add_widget(self.month_field)

        self.year_field = MDTextField(
            text=str(today.year),
            hint_text="Año",
            mode="rectangle",
            size_hint=(None, None),
            width=dp(100),
            height=dp(48),
            font_size=dp(18),
            padding=(dp(10), dp(12), dp(10), dp(12)),
            readonly=False
        )
        self.year_menu = MDDropdownMenu(
            caller=self.year_field,
            items=[{"text": str(y), "on_release": lambda x=str(y): self.set_year(x)} for y in range(today.year - 5, today.year + 1)],
            width_mult=4
        )
        self.year_field.bind(on_release=self.year_menu.open)
        spinners_layout.add_widget(self.year_field)

        main_layout.add_widget(spinners_layout)

        btn_layout = MDBoxLayout(
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(50),
            pos_hint={"center_x": 0.5}
        )
        btn_ok = MDRaisedButton(
            text="ACEPTAR",
            on_release=self.select_date,
            size_hint=(0.5, None),
            height=dp(45),
            md_bg_color=[1, 0.4, 0.4, 1],
            theme_text_color="Custom",
            text_color=[1, 1, 1, 1]
        )
        btn_cancel = MDFlatButton(
            text="CANCELAR",
            on_release=self.dismiss,
            size_hint=(0.5, None),
            height=dp(45),
            theme_text_color="Custom",
            text_color=[1, 0.4, 0.4, 1]
        )
        btn_layout.add_widget(btn_ok)
        btn_layout.add_widget(btn_cancel)
        main_layout.add_widget(btn_layout)

        self.content = main_layout

    def set_day(self, day):
        self.day_field.text = day
        self.day_menu.dismiss()

    def set_month(self, month):
        self.month_field.text = month
        self.month_menu.dismiss()

    def set_year(self, year):
        self.year_field.text = year
        self.year_menu.dismiss()

    def select_date(self, instance):
        try:
            selected_date = date(
                int(self.year_field.text),
                int(self.month_field.text),
                int(self.day_field.text)
            )
            self.on_date_selected(selected_date)
            self.dismiss()
        except ValueError:
            self.show_error_dialog("Fecha no válida. Por favor verifique los valores.")

    def show_error_dialog(self, text):
        self.dialog = MDDialog(
            title="[color=#FF0000]Error[/color]",
            text=text,
            size_hint=(0.8, None),
            height=dp(150),
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=[1, 0.4, 0.4, 1],
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

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
