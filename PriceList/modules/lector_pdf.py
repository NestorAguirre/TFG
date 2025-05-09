from pdfminer.high_level import extract_text
import re

class ErrorTicket(Exception):
    pass

class LectorTicket:
    def __init__(self, ticket):
        self.ticket = ticket
        self.arrayTicket = []
        self.diccionarioProductos = {}
        self.extraerTexto()
        self.detectarTicket()
        self.inicioProductos, self.inicioPrecios = self.inicioProductosPrecios()
        
    def extraerTexto(self):
        ticketTexto = extract_text(self.ticket)
        lineas = ticketTexto.split("\n")

        for linea in lineas:
            if linea.strip() != "":
                self.arrayTicket.append(linea.strip())

        return self.arrayTicket
    
    def detectarTicket(self):
        if not self.arrayTicket or str(self.arrayTicket[0]).strip().upper()[0:9] != "MERCADONA":
            raise ErrorTicket("No se ha podido leer el ticket. Parece que no es un ticket del Mercadona.")
    
    def inicioProductosPrecios(self):
        try:
            contador = 0
            inicioProductos = 0
            inicioPrecios = 0
            for texto in self.arrayTicket:
                if texto == "Descripción".strip():
                    inicioProductos = contador
                if texto == "Importe".strip():
                    inicioPrecios = contador
                contador = contador + 1
            return inicioProductos, inicioPrecios
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
            arrayPrecios = []
            for precio in self.arrayTicket[self.inicioPrecios + 1 : ]:
                precio = str(precio).strip()
                precio = precio.replace(",",".")
                
                try:
                    precio_float = float(precio)
                except ValueError:
                    break
                
                if precio == "0.00":
                    break
                
                precio = float(precio)
                
                arrayPrecios.append(precio)
            return arrayPrecios
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
                
                if producto[1] > 1:
                    precio = round(arrayPrecios[contador] / producto[1], 2)
                
                self.diccionarioProductos[producto[0]] = precio
                contador += 1
            
            return self.diccionarioProductos
        except:
            raise ErrorTicket("Error en la lectura del ticket")
        
    def getFechaTicket(self):
        for linea in self.arrayTicket:
            match = re.match(r'^(\d{2}/\d{2}/\d{4}) \d{2}:\d{2}$', linea)
            if match:
                return match.group(1)
        raise ErrorTicket("No se encontró una fecha válida en el ticket.")
    
if __name__ == "__main__":
    #try:
    #    lector = LectorTicket("tickets/ticket1.pdf") #ME HE QUEDADO EN EL 13
    #    texto = lector.cargarDiccionario()
    #    print(texto)
    #except ErrorTicket as e:
    #    print(f"Error: {e}")
    lector = LectorTicket(r"D:\ASIGNATURAS\TFG\TFG\tickets\ticket30.pdf")
    print(lector.getFechaTicket())