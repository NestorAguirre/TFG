KV_LACTEOS = """
<LacteosScreen>:
    canvas:
        Color:
            rgba: 0.98, 0.98, 0.98, 1
        Rectangle:
            size: self.size
            pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        
        canvas.before:
            Color:
                rgba: 0.98, 0.95, 0.88, 1
            Rectangle:
                size: self.size
                pos: self.pos

        RelativeLayout:
            size_hint_y: 0.12

            canvas.before:
                Color:
                    rgba: 0.73, 0.37, 0.27, 1
                Rectangle:
                    size: self.width, dp(4)
                    pos: self.x, self.y - dp(5)

            RelativeLayout:
                size_hint: None, None
                size: dp(40), dp(40)
                pos: dp(4), self.height - dp(25)

                Button:
                    size: dp(40), dp(40)
                    pos: 0, 0
                    background_normal: ''
                    background_color: 0, 0, 0, 0
                    on_release: app.volver_atras()

                Image:
                    source: 'assets/images/botones/btnatras.png'
                    size_hint: None, None
                    size: dp(24), dp(24)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            Label:
                text: "Lácteos"
                font_size: app.title_font_size
                bold: True
                color: 0.2, 0.2, 0.2, 1
                halign: 'center'
                valign: 'middle'
                font_name: "assets/fonts/DancingScript-VariableFont_wght.ttf"

        ScrollView:
            size_hint_y: 1
            bar_width: dp(10)
            do_scroll_x: False
            scroll_type: ['bars', 'content']

            GridLayout:
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(20)
                padding: dp(10)

                # Primera fila
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(20)
                    size_hint_y: None
                    height: 1.25 * (root.width / 2 - dp(20))

                    # Botón Yogures y postres
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 0.5
                        size_hint_y: None
                        height: 1.25 * self.width
                        
                        RelativeLayout:
                            size_hint_y: 0.8
                            
                            Button:
                                size_hint: 1, 1
                                background_normal: ''
                                background_color: 0.25, 0.65, 0.45, 0.3
                                on_release:
                                    app.familia('Yogures y postres')
                                    app.cambiar_pantalla('listadoproductos')
                            
                            Image:
                                source: 'assets/images/familias/Frescos/YoguresPostres.png'
                                size_hint: 0.85, 0.85
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                        
                        Label:
                            text: "Yogures y postres"
                            font_size: app.label_font_size
                            bold: True
                            size_hint_y: 0.2
                            color: 0.2, 0.2, 0.2, 1
                            halign: 'center'
                            valign: 'middle'
                            font_name: "assets/fonts/DancingScript-VariableFont_wght.ttf"

                    # Botón Leche y derivados
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 0.5
                        size_hint_y: None
                        height: 1.25 * self.width
                        
                        RelativeLayout:
                            size_hint_y: 0.8
                            
                            Button:
                                size_hint: 1, 1
                                background_normal: ''
                                background_color: 0.8, 0.5, 0.3, 0.3
                                on_release:
                                    app.familia('Leche y derivados')
                                    app.cambiar_pantalla('listadoproductos')
                            
                            Image:
                                source: 'assets/images/familias/Frescos/LecheDerivados.png'
                                size_hint: 0.85, 0.85
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                        
                        Label:
                            text: "Leche y derivados"
                            font_size: app.label_font_size
                            bold: True
                            size_hint_y: 0.2
                            color: 0.2, 0.2, 0.2, 1
                            halign: 'center'
                            valign: 'middle'
                            font_name: "assets/fonts/DancingScript-VariableFont_wght.ttf"

                # Segunda fila
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(20)
                    size_hint_y: None
                    height: 1.25 * (root.width / 2 - dp(20))

                    # Botón Quesos
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 0.5
                        size_hint_y: None
                        height: 1.25 * self.width
                        
                        RelativeLayout:
                            size_hint_y: 0.8
                            
                            Button:
                                size_hint: 1, 1
                                background_normal: ''
                                background_color: 0.3, 0.4, 0.8, 0.3
                                on_release:
                                    app.familia('Quesos')
                                    app.cambiar_pantalla('listadoproductos')
                            
                            Image:
                                source: 'assets/images/familias/Frescos/Quesos.png'
                                size_hint: 0.85, 0.85
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                        
                        Label:
                            text: "Quesos"
                            font_size: app.label_font_size
                            bold: True
                            size_hint_y: 0.2
                            color: 0.2, 0.2, 0.2, 1
                            halign: 'center'
                            valign: 'middle'
                            font_name: "assets/fonts/DancingScript-VariableFont_wght.ttf"

                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 0.5
                        size_hint_y: None
                        height: 1.25 * self.width
"""