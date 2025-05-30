import pdfplumber
import re
from datetime import datetime

class ErrorTicket(Exception):
    pass

class LectorTicket:
    def __init__(self, ticket):
        self.ticket = ticket
        self.arrayTicket = []
        self.diccionarioProductos = {}
        self.extraerTexto()
        self.detectarTicket()
        self.inicioProductos = self.inicioProductosPrecios()

    def extraerTexto(self):
        try:
            self.arrayTicket = []
            with pdfplumber.open(self.ticket) as pdf:
                for page in pdf.pages:
                    texto = page.extract_text()
                    if texto:
                        lineas = texto.split("\n")
                        for linea in lineas:
                            sublineas = re.split(r'\s{2,}', linea.strip())
                            for sub in sublineas:
                                sub = sub.strip()
                                if sub:
                                    self.arrayTicket.append(sub)
            return self.arrayTicket
        except Exception:
            raise ErrorTicket("Error leyendo el PDF")

    def detectarTicket(self):
        if not self.arrayTicket or not str(self.arrayTicket[0]).strip().upper().startswith("MERCADONA"):
            raise ErrorTicket("No se ha podido leer el ticket. Parece que no es un ticket del Mercadona.")

    def inicioProductosPrecios(self):
        try:
            for i, linea in enumerate(self.arrayTicket):
                if re.search(r'(?i)\bImporte\b', linea):
                    return i
            raise ErrorTicket("No se encontró 'Importe'")
        except Exception:
            raise ErrorTicket("Error en la lectura del ticket")

    def extraerProductos(self):
        try:
            lista_productos = []
            for linea in self.arrayTicket[self.inicioProductos + 1:]:
                linea = linea.strip()
                if not linea or "TOTAL" in linea or "TARJETA" in linea:
                    continue

                match = re.match(r"^(\d+)\s+(.*?)(?:\s+\d+,\d{2}){1,2}$", linea)
                if match:
                    cantidad = int(match.group(1))
                    nombre = match.group(2).strip().title()
                    lista_productos.append((nombre, cantidad))
                else:
                    tokens = linea.split()
                    if len(tokens) >= 2 and tokens[0].isdigit():
                        cantidad = int(tokens[0])
                        nombre = " ".join(tokens[1:]).title()
                        lista_productos.append((nombre, cantidad))
            return lista_productos
        except Exception:
            raise ErrorTicket("Error en la lectura de productos")

    def extraerPrecios(self):
        try:
            precios = []
            for linea in self.arrayTicket[self.inicioProductos + 1:]:
                if not linea or "TOTAL" in linea:
                    continue

                if "€/kg" in linea:
                    match = re.search(r"(\d+,\d{2})\s*€/kg", linea)
                    if match:
                        precio = float(match.group(1).replace(",", "."))
                        precios.append(round(precio, 2))
                        continue

                partes = re.findall(r"\d+,\d{2}", linea)
                if partes:
                    precio = float(partes[0].replace(",", "."))
                    precios.append(round(precio, 2))
            return precios
        except Exception:
            raise ErrorTicket("Error en la lectura de precios")

    def cargarDiccionario(self):
        try:
            productos = self.extraerProductos()
            precios = self.extraerPrecios()

            for i in range(min(len(productos), len(precios))):
                self.diccionarioProductos[productos[i][0]] = precios[i]

            for basura in ["Parking", "Parking:"]:
                self.diccionarioProductos.pop(basura, None)

            return self.diccionarioProductos
        except:
            raise ErrorTicket("Error cargando diccionario")

    def getFechaTicket(self):
        for linea in self.arrayTicket:
            match = re.search(r'(\d{2}/\d{2}/\d{4})\s+\d{2}:\d{2}', linea)
            if match:
                return datetime.strptime(match.group(1), "%d/%m/%Y").strftime("%Y-%m-%d")
        raise ErrorTicket("No se encontró una fecha válida en el ticket.")
    
if __name__ == "__main__":
    #try:
    #    lector = LectorTicket("tickets/ticket1.pdf") #ME HE QUEDADO EN EL 13
    #    texto = lector.cargarDiccionario()
    #    print(texto)
    #except ErrorTicket as e:
    #    print(f"Error: {e}")
    lector = LectorTicket(r"D:\ASIGNATURAS\TFG\TFG\tickets\ticket1.pdf")
    print(lector.cargarDiccionario())