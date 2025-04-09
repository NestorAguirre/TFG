import sqlite3 as sql

class DBController():
    
    def __init__(self, nombreDB):
        self.nombreDB = nombreDB
        self.crearDB()
        self.crearTablas()
        
    def crearDB(self):
        conexion = sql.connect(self.nombreDB)
        conexion.commit()
        conexion.close()
        
    def crearTablas(self):
        conexion = sql.connect(self.nombreDB)
        cursor = conexion.cursor()
        
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha DATE
                );
            """
        )
        
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    familia TEXT  -- Alimentos envasados, Frescos, Bebidas...
                );
            """
        )
        
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS precios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER,
                    ticket_id INTEGER,
                    precio REAL,
                    FOREIGN KEY (producto_id) REFERENCES productos(id),
                    FOREIGN KEY (ticket_id) REFERENCES tickets(id)
                );

            """
        )
        
        conexion.commit()
        conexion.close()
        
    def insertarProducto(self, nombre, familia):
        conexion = sql.connect(self.nombreDB)
        cursor = conexion.cursor()
        
        consulta = f"INSERT INTO productos(nombre, familia) VALUES ('{nombre}', '{familia}')"
        cursor.execute(consulta)
        
        conexion.commit()
        conexion.close()
        
    def clasificar_por_reglas(self, nombre_producto):
        nombre = nombre_producto.lower()

        if any(palabra in nombre for palabra in ["cerveza", "vino", "cola", "refresco", "agua"]):
            return "Bebidas"
        elif any(palabra in nombre for palabra in ["jamón", "pollo", "lechuga", "manzana", "pescado"]):
            return "AlimentosFrescos"
        elif any(palabra in nombre for palabra in ["galleta", "pasta", "arroz", "lata", "tomate frito"]):
            return "AlimentosEnvasados"
        elif any(palabra in nombre for palabra in ["pizza", "congelado", "helado"]):
            return "Congelados"
        elif any(palabra in nombre for palabra in ["champú", "gel", "crema", "dentífrico"]):
            return "CuidadoPersonal"
        elif any(palabra in nombre for palabra in ["lejía", "detergente", "limpiador"]):
            return "Limpieza/Hogar"
        elif any(palabra in nombre for palabra in ["pan", "bollería", "croissant"]):
            return "Panaderia/Reposteria"
        else:
            return "FamiliaDesconocida"


if __name__ == "__main__":
    base = DBController("pricelist.db")
    base.insertarProducto("nombreProducto", "familiaProducto")