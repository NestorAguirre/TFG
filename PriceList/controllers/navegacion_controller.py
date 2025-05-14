def cambiar_pantalla(app, nombre_pantalla):
    if app.sm.current != nombre_pantalla:
        app.historial_pantallas.append(app.sm.current)
        app.sm.transition.direction = 'left'
        app.sm.current = nombre_pantalla

def volver_atras(app):
    if len(app.historial_pantallas) > 1:
        pantalla_anterior = app.historial_pantallas.pop()
        app.sm.transition.direction = 'right'
        app.sm.current = pantalla_anterior
