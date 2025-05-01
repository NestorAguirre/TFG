from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.core.text import LabelBase

# Registrar la fuente personalizada
LabelBase.register(
    name='DancingScript',
    fn_regular='assets/fonts/DancingScript-VariableFont_wght.ttf'
)

class TableRow(BoxLayout):
    texto_producto = StringProperty('')
    texto_precio = StringProperty('')
    texto_maximo = StringProperty('')
    texto_minimo = StringProperty('')
    texto_media = StringProperty('')

class MainScreen(BoxLayout):
    familia = StringProperty("Familia: Panadería")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.productos = [
            {"producto": "Pan", "precio": "1.00", "maximo": "1.20", "minimo": "0.80", "media": "1.00"},
            {"producto": "Panka", "precio": "0.90", "maximo": "1.10", "minimo": "0.70", "media": "0.90"},
        ]
        self.actualizar_tabla()

    def actualizar_tabla(self):
        data = []
        seen = set()
        for p in self.productos:
            key = (p['producto'], p['precio'])
            if key not in seen:
                seen.add(key)
                data.append({
                    'texto_producto': p['producto'],
                    'texto_precio': p['precio'],
                    'texto_maximo': p['maximo'],
                    'texto_minimo': p['minimo'],
                    'texto_media': p['media']
                })
        self.ids.table_rv.data = data

class ListadoDatosApp(App):
    def build(self):
        Builder.load_file('ui.kv')
        return MainScreen()

if __name__ == '__main__':
    ListadoDatosApp().run()
