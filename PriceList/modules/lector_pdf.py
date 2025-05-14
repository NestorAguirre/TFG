import fitz
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
        ticket = fitz.open(self.ticket)
        self.arrayTicket = []
        for pagina in ticket:
            textoTicket = pagina.get_text()
            lineas = textoTicket.split("\n")
            for linea in lineas:
                linea = linea.strip()
                if linea:
                    self.arrayTicket.append(linea)
        ticket.close()
        return self.arrayTicket
    
    def detectarTicket(self):
        if not self.arrayTicket or str(self.arrayTicket[0]).strip().upper()[0:9] != "MERCADONA":
            raise ErrorTicket("No se ha podido leer el ticket. Parece que no es un ticket del Mercadona.")
    
    def inicioProductosPrecios(self):
        try:
            contador = 0
            inicioProductosPrecios = 0
            for texto in self.arrayTicket:
                if texto == "Importe".strip():
                    inicioProductosPrecios = contador
                contador = contador + 1
            return inicioProductosPrecios
        except:
            raise ErrorTicket("Error en la lectura del ticket")
    
    def extraerProductos(self):
        try:
            lista_productos = []

            for producto in self.arrayTicket[self.inicioProductos + 1 :]:
                producto = producto.strip()

                if not producto:
                    continue
                
                if not producto.endswith(" kg"):
                    partes = producto.split(" ", 1)
                    if len(partes) != 2:
                        continue

                    cantidad, nombre = partes
                    nombre = str(nombre).title()

                    if nombre.strip().lower().endswith("kg"):
                        nombre = nombre[0:-2]
                        nombre = nombre.strip()

                    try:
                        cantidad = int(cantidad)
                    except ValueError:
                        continue
                    
                    lista_productos.append((nombre.strip(), cantidad))
                else:
                    kg = producto[0:-2].strip()
                    kg = kg.replace(",",".")
                    lista_productos[len(lista_productos)-1] = (nombre, float(kg))

            return lista_productos
        except:
            raise ErrorTicket("Error en la lectura del ticket")
    
    def extraerPrecios(self):
        try:
            arrayprecios = []
            i = self.inicioProductos + 1
            lista = self.arrayTicket

            while i < len(lista):
                item = lista[i]

                # Productos a peso (€/kg)
                if "€/kg" in str(item):
                    partes = str(item).split(" ")
                    for parte in partes:
                        if "€" in parte:
                            break
                        else:
                            precio = parte.replace(",", ".").strip()
                            arrayprecios.append(round(float(precio), 2))
                        break
                    i += 3
                    continue

                # Productos normales
                if isinstance(item, str):
                    es_numero = item.replace(",", "").replace(".", "").isdigit()
                    if not es_numero and "€/kg" not in item:
                        siguiente = lista[i + 1] if i + 1 < len(lista) else ""
                        despues = lista[i + 2] if i + 2 < len(lista) else ""

                        # Dos precios seguidos → coger el primero
                        if isinstance(siguiente, str) and siguiente.replace(",", "").replace(".", "").isdigit() and \
                        isinstance(despues, str) and despues.replace(",", "").replace(".", "").isdigit():
                            arrayprecios.append(round(float(siguiente.replace(",", ".")), 2))
                            i += 3
                            continue

                        # Un solo precio
                        elif isinstance(siguiente, str) and siguiente.replace(",", "").replace(".", "").isdigit():
                            arrayprecios.append(round(float(siguiente.replace(",", ".")), 2))
                            i += 2
                            continue

                i += 1

            return arrayprecios

        except:
            raise ErrorTicket("Error en la lectura del ticket")

    def cargarDiccionario(self):
        try:
            lista_productos = self.extraerProductos()
            arrayPrecios = self.extraerPrecios()
            
            contador = 0
            while contador < len(arrayPrecios):
                try:
                    producto = lista_productos[contador]
                except:
                    break
                precio = arrayPrecios[contador]
                
                self.diccionarioProductos[producto[0]] = precio
                contador += 1
                
            try:
                del self.diccionarioProductos["Parking"]
                del self.diccionarioProductos["Parking:"]
            except:
                pass
            return self.diccionarioProductos
        except:
            raise ErrorTicket("Error en la lectura del ticket")
        
    def getFechaTicket(self):
        for linea in self.arrayTicket:
            match = re.match(r'^(\d{2}/\d{2}/\d{4}) \d{2}:\d{2}$', linea)
            if match:
                fecha_str = match.group(1)
                # Convertir a formato datetime y luego a ISO (YYYY-MM-DD)
                fecha_iso = datetime.strptime(fecha_str, "%d/%m/%Y").strftime("%Y-%m-%d")
                return fecha_iso
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