import sqlite3 as sql
import os

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
                    familia TEXT
                );
            """
        )
        
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS precios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER,
                    ticket_id INTEGER,
                    precio FLOAT,
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
        
    def insertarTicket(self, fecha):
        conexion = sql.connect(self.nombreDB)
        cursor = conexion.cursor()
        
        cursor.execute("INSERT INTO tickets(fecha) VALUES (?)", (fecha,))
        
        conexion.commit()
        conexion.close()
        
    def insertarPrecio(self, producto_id, ticket_id, precio):
        conexion = sql.connect(self.nombreDB)
        cursor = conexion.cursor()
        
        cursor.execute("INSERT INTO precios(producto_id, ticket_id, precio) VALUES (?, ?, ?)", (producto_id, ticket_id, precio))
        
        conexion.commit()
        conexion.close()
        
    def getProductoPorNombre(self, nombre_producto):
        conexion = sql.connect(self.nombreDB)
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id FROM productos WHERE nombre = (?)", (nombre_producto,))
        resultado = cursor.fetchone()
        
        conexion.commit()
        conexion.close()
        
        return resultado[0]
        
    def getUltimoTicket(self):
        conexion = sql.connect(self.nombreDB)
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id FROM tickets ORDER BY id DESC LIMIT 1")
        resultado = cursor.fetchone()
        
        conexion.commit()
        conexion.close()
        
        return resultado[0]
    
    def getResumenProductosPorFamilia(self, nombre_familia, fecha_limite):
        conexion = sql.connect(self.nombreDB)
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT 
                p.nombre,
                (
                    SELECT pr.precio
                    FROM precios pr
                    JOIN tickets t ON pr.ticket_id = t.id
                    WHERE pr.producto_id = p.id
                    AND t.fecha <= ?
                    ORDER BY DATE(t.fecha) DESC
                    LIMIT 1
                ) AS precio_actual,
                MIN(pr.precio) AS minimo,
                MAX(pr.precio) AS maximo,
                AVG(pr.precio) AS media
            FROM productos p
            JOIN precios pr ON pr.producto_id = p.id
            JOIN tickets t ON pr.ticket_id = t.id
            WHERE p.familia = ?
            AND t.fecha <= ?
            GROUP BY p.id
            ORDER BY p.nombre ASC
        """, (fecha_limite, nombre_familia, fecha_limite))
        
        resultados = cursor.fetchall()
        conexion.close()

        productos = []
        for nombre, precio, minimo, maximo, media in resultados:
            productos.append({
                "producto": nombre,
                "precio": f"{precio:.2f}" if precio is not None else "N/A",
                "minimo": f"{minimo:.2f}" if minimo is not None else "N/A",
                "maximo": f"{maximo:.2f}" if maximo is not None else "N/A",
                "media": f"{media:.2f}" if media is not None else "N/A"
            })

        return productos
    
    def vaciarBaseDeDatos(self):
        conexion = sql.connect(self.nombreDB)
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM precios")
        cursor.execute("DELETE FROM tickets")
        cursor.execute("DELETE FROM productos")

        conexion.commit()
        conexion.close()

if __name__ == "__main__":
    base = DBController("data/pricelist.db")
    base.vaciarBaseDeDatos()