from database.dbcontroller import DBController
from lector_pdf import LectorTicket
from datetime import date
from listados import productos_por_familia
from splash import SplasScreenApp

if __name__ == "__main__":
    contador = 1
    while contador < 23:
        lector = LectorTicket(f"tickets/ticket{contador}.pdf")
        db = DBController("database/pricelist.db")
        
        db.insertarTicket(date.today())
        ticket_id = db.getUltimoTicket()
        
        for producto, precio in lector.cargarDiccionario().items():
            producto_normalizado = producto.strip().lower()
            familia = "otraFamilia"
            
            for key, lista_productos in productos_por_familia.items():
                for p in lista_productos:
                    if p.strip().lower() == producto_normalizado:
                        familia = key
                        break
                else:
                    continue
                break
            
            db.insertarProducto(producto, familia)
            db.insertarPrecio(db.getProdutoPorNombre(producto), ticket_id, precio)
        contador = contador + 1
    #SplasScreenApp().run()