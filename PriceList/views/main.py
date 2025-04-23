from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class PriceListRoot(BoxLayout):
    pass

class PriceListApp(App):
    def build(self):
        return PriceListRoot()

if __name__ == '__main__':
    PriceListApp().run()
