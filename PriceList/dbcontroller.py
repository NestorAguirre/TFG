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
        
        cursor.execute("SELECT id FROM productos WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            cursor.execute("INSERT INTO productos(nombre, familia) VALUES (?, ?)", (nombre, familia))
            conexion.commit()
        
        conexion.close()


if __name__ == "__main__":
    base = DBController("pricelist.db")
    base.insertarProducto("nombreProducto", "familiaProducto")