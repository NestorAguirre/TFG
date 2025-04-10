from dbcontroller import DBController
from lector_pdf import LectorTicket

if __name__ == "__main__":
    lector = LectorTicket("ticket1.pdf")
    db = DBController("pricelist.db")
    
    for producto in lector.cargarDiccionario().keys():
        db.insertarProducto(producto, "familiaPrueba")