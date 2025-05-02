from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

Builder.load_file("main.kv")
Builder.load_file("bebidas.kv")
Builder.load_file("cuidadopersonal.kv")
Builder.load_file("limpieza.kv")
Builder.load_file("congelados.kv")
Builder.load_file("envasados.kv")
Builder.load_file("listadoproductos.kv")

class MenuScreen(Screen):
    pass

class BebidasScreen(Screen):
    pass

class CuidadoPersonalScreen(Screen):
    pass

class LimpiezaScreen(Screen):
    pass

class ListadoProductosScreen(Screen):
    pass

class CongeladosScreen(Screen):
    pass

class EnvasadosScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        self.icon = 'assets/images/PriceListLogo.jpg'
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(BebidasScreen(name="bebidas"))
        sm.add_widget(CuidadoPersonalScreen(name="cuidadopersonal"))
        sm.add_widget(LimpiezaScreen(name="limpieza"))
        sm.add_widget(CongeladosScreen(name="congelados"))
        sm.add_widget(EnvasadosScreen(name="envasados"))
        sm.add_widget(ListadoProductosScreen(name="listadoproductos"))
        return sm

if __name__ == "__main__":
    MyApp().run()
