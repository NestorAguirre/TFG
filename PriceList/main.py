from dbcontroller import DBController
from lector_pdf import LectorTicket
from datetime import date

if __name__ == "__main__":
    lector = LectorTicket("ticket2.pdf")
    db = DBController("pricelist.db")
    
    db.insertarTicket(date.today())
    ticket_id = db.getUltimoTicket()
    
    for producto, precio in lector.cargarDiccionario().items():
        db.insertarProducto(producto, "familiaPrueba")
        db.insertarPrecio(db.getProdutoPorNombre(producto), ticket_id, precio)