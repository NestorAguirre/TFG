from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

class LimpiezaScreen(Screen):
    pass

class LimpiezaApp(App):
    def build(self):
        Builder.load_file('limpieza.kv')
        sm = ScreenManager()
        sm.add_widget(LimpiezaScreen(name='Limpieza'))
        return sm

    def on_button_press(self, tipo):
        print(f"Seleccionaste: {tipo}")

if __name__ == '__main__':
    LimpiezaApp().run()
