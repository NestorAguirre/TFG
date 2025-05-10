from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

KV = '''
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        canvas.before:
            Color:
                rgba: 0.98, 0.95, 0.88, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "PriceList"
            font_size: app.title_font_size
            bold: True
            color: 0.2, 0.2, 0.2, 1
            size_hint_y: 0.12
            halign: 'center'
            valign: 'middle'
            font_name: "assets/fonts/DancingScript-VariableFont_wght.ttf"
            canvas.before:
                Color:
                    rgba: 0.73, 0.37, 0.27, 1
                Rectangle:
                    size: self.width, dp(4)
                    pos: self.x, self.y - dp(5)

        GridLayout:
            cols: 2
            spacing: dp(20)
            padding: dp(20)
            size_hint_y: 0.8

            Button:
                text: "Frescos"
                font_size: app.button_font_size
                bold: True
                color: 0.2, 0.2, 0.2, 1
                background_normal: ''
                background_color: 0.25, 0.65, 0.45, 0.3
                font_name: "assets/fonts/DancingScript-VariableFont_wght.ttf"

            Button:
                text: "Envasados"
                font_size: app.button_font_size
                bold: True
                color: 0.2, 0.2, 0.2, 1
                background_normal: ''
                background_color: 0.8, 0.5, 0.3, 0.3
                font_name: "assets/fonts/DancingScript-VariableFont_wght.ttf"

            Button:
                text: "Congelados"
                font_size: app.button_font_size
                bold: True
                color: 0.2, 0.2, 0.2, 1
                background_normal: ''
                background_color: 0.3, 0.4, 0.8, 0.3
                font_name: "assets/fonts/DancingScript-VariableFont_wght.ttf"

            Button:
                text: "Bebidas"
                font_size: app.button_font_size
                bold: True
                color: 0.2, 0.2, 0.2, 1
                background_normal: ''
                background_color: 0.8, 0.3, 0.4, 0.3
                font_name: "assets/fonts/DancingScript-VariableFont_wght.ttf"

            Button:
                text: "Cuidado personal"
                font_size: app.button_font_size
                bold: True
                color: 0.2, 0.2, 0.2, 1
                background_normal: ''
                background_color: 0.6, 0.3, 0.8, 0.3
                font_name: "assets/fonts/DancingScript-VariableFont_wght.ttf"

            Button:
                text: "Limpieza"
                font_size: app.button_font_size
                bold: True
                color: 0.2, 0.2, 0.2, 1
                background_normal: ''
                background_color: 0.85, 0.65, 0.2, 0.3
                font_name: "assets/fonts/DancingScript-VariableFont_wght.ttf"

        Button:
            text: "Importar Ticket"
            font_size: app.button_font_size
            bold: True
            size_hint_y: None
            height: dp(60)
            background_normal: ''
            background_color: 0.73, 0.37, 0.27, 1
            color: 1, 1, 1, 1 
            font_name: "assets/fonts/DancingScript-VariableFont_wght.ttf"
'''

class MenuScreen(Screen):
    pass

class PriceListApp(App):
    title_font_size = 40
    button_font_size = 20

    def build(self):
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        return sm

if __name__ == '__main__':
    PriceListApp().run()
