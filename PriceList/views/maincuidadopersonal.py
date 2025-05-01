from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

class CuidadoPersonalScreen(Screen):
    pass

class CuidadoPersonalApp(App):
    def build(self):
        Builder.load_file('cuidadopersonal.kv')
        sm = ScreenManager()
        sm.add_widget(CuidadoPersonalScreen(name='Cuidado personal'))
        return sm

    def on_button_press(self, tipo):
        print(f"Seleccionaste: {tipo}")

if __name__ == '__main__':
    CuidadoPersonalApp().run()
