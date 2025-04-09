from dbcontroller import DBController
from lector_pdf import LectorTicket

if __name__ == "__main__":
    lector = LectorTicket("ticket1.pdf")
    db = DBController("pricelist.db")
    
    for producto in lector.cargarDiccionario().keys():
        familia = db.clasificar_por_reglas(producto)
        db.insertarProducto(producto, familia)