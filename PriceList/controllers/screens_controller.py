from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

class MenuScreen(Screen): pass
class BebidasScreen(Screen): familia_nombre = "Bebidas"
class CuidadoPersonalScreen(Screen): familia_nombre = "Cuidado Personal"
class LimpiezaScreen(Screen): familia_nombre = "Limpieza"
class CongeladosScreen(Screen): familia_nombre = "Congelados"
class EnvasadosScreen(Screen): familia_nombre = "Envasados"
class FrescosScreen(Screen): familia_nombre = "Frescos"
class LacteosScreen(Screen): familia_nombre = "Lácteos"
class DesayunoScreen(Screen): familia_nombre = "Desayuno"
class ListadoProductosScreen(Screen): familia_nombre = StringProperty("")
class ListadoProductosGeneralScreen(Screen): familia_nombre = StringProperty("")
class ProductosRecyclerView(BoxLayout):
    producto = StringProperty("")
    precio = StringProperty("")
    maximo = StringProperty("")
    minimo = StringProperty("")
    media = StringProperty("")

def cargar_vistas(sm):
    sm.add_widget(FrescosScreen(name='frescos'))
    sm.add_widget(LimpiezaScreen(name='limpieza'))
    sm.add_widget(BebidasScreen(name='bebidas'))
    sm.add_widget(CongeladosScreen(name='congelados'))
    sm.add_widget(CuidadoPersonalScreen(name='cuidadopersonal'))
    sm.add_widget(DesayunoScreen(name='desayuno'))
    sm.add_widget(EnvasadosScreen(name='envasados'))
    sm.add_widget(LacteosScreen(name='lacteos'))
    sm.add_widget(ListadoProductosScreen(name='listadoproductos'))
    sm.add_widget(ListadoProductosGeneralScreen(name='listadoproductosgeneral'))
