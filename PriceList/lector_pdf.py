from pdfminer.high_level import extract_text

class LectorTicket:
    def __init__(self, ticket):
        self.ticket = ticket
        self.arrayTicket = []
        self.diccionarioProductos = {}
        self.extraerTexto()
        self.inicioProductos, self.inicioPrecios = self.inicioProductosPrecios()
        
    def extraerTexto(self):
        ticketTexto = extract_text(self.ticket)
        lineas = ticketTexto.split("\n")

        for linea in lineas:
            if linea.strip() != "":
                self.arrayTicket.append(linea.strip())

        return self.arrayTicket

    
    def inicioProductosPrecios(self):
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
    
    def extraerProductos(self):
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
                nombre = str(nombre)

                if nombre.strip().endswith("kg"):
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
    
    def extraerPrecios(self):
        arrayPrecios = []
        for precio in self.arrayTicket[self.inicioPrecios + 1 : ]:
            precio = str(precio).strip()
            precio = precio.replace(",",".")
            
            if not precio:
                continue
            
            if precio == "0.00":
                break
            
            precio = float(precio)
            
            arrayPrecios.append(precio)
        return arrayPrecios

    def cargarDiccionario(self):
        lista_productos = self.extraerProductos()
        arrayPrecios = self.extraerPrecios()
        
        contador = 0
        while contador < len(arrayPrecios):
            producto = lista_productos[contador]
            precio = arrayPrecios[contador]
            
            if producto[1] > 1:
                precio = round(arrayPrecios[contador] / producto[1], 2)
            
            self.diccionarioProductos[producto[0]] = precio
            contador += 1
        
        return self.diccionarioProductos
        

    
if __name__ == "__main__":
    lector = LectorTicket("ticket1.pdf")
    texto = lector.cargarDiccionario()
    for mierda in texto.keys():
        print(f"1 {mierda} cuesta {texto[mierda]}")
    