from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

class BebidasScreen(Screen):
    pass

class BebidasApp(App):
    def build(self):
        Builder.load_file('bebidas.kv')
        sm = ScreenManager()
        sm.add_widget(BebidasScreen(name='bebidas'))
        return sm

    def on_button_press(self, tipo):
        print(f"Seleccionaste: {tipo}")

if __name__ == '__main__':
    BebidasApp().run()
