def cambiar_pantalla(app, nombre_pantalla):
    if app.sm.current != nombre_pantalla:
        if app.sm.current == "listadoproductos":
            app.date_picker.reset_fecha()

        app.historial_pantallas.append(app.sm.current)
        app.sm.transition.direction = 'left'
        app.sm.current = nombre_pantalla


def volver_atras(app):
    if len(app.historial_pantallas) > 1:
        app.historial_pantallas.pop()
        pantalla_anterior = app.historial_pantallas[-1]

        if app.sm.current == "listadoproductos":
            app.date_picker.reset_fecha()

        app.sm.transition.direction = 'right'
        app.sm.current = pantalla_anterior
        return True
    return False


def capturar_tecla_atras(window, key, *args):
    from kivy.app import App
    app = App.get_running_app()

    if key == 27:
        return volver_atras(app)
    return False
