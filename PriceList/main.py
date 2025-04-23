#from database.dbcontroller import DBController
#from lector_pdf import LectorTicket
#from datetime import date
#from listados import productos_por_familia
#
#if __name__ == "__main__":
#    contador = 1
#    while contador < 23:
#        lector = LectorTicket(f"tickets/ticket{contador}.pdf")
#        db = DBController("database/pricelist.db")
#        
#        db.insertarTicket(date.today())
#        ticket_id = db.getUltimoTicket()
#        
#        for producto, precio in lector.cargarDiccionario().items():
#            producto_normalizado = producto.strip().lower()
#            familia = "otraFamilia"
#            
#            for key, lista_productos in productos_por_familia.items():
#                for p in lista_productos:
#                    if p.strip().lower() == producto_normalizado:
#                        familia = key
#                        break
#                else:
#                    continue
#                break
#            
#            db.insertarProducto(producto, familia)
#            db.insertarPrecio(db.getProdutoPorNombre(producto), ticket_id, precio)
#        contador = contador + 1
#    #SplasScreenApp().run()
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import os

class PriceListRoot(BoxLayout):
    pass

class PriceListApp(App):
    def build(self):
        kv_path = os.path.join(os.path.dirname(__file__), 'views', 'pricelist.kv')
        Builder.load_file(kv_path)
        return PriceListRoot()

if __name__ == '__main__':
    PriceListApp().run()

