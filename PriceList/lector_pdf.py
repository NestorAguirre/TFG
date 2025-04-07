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
        diccionario_productos = {}

        for producto in self.arrayTicket[self.inicioProductos + 1 :]:
            producto = producto.strip()

            if not producto:
                continue

            partes = producto.split(" ", 1)
            if len(partes) != 2:
                continue

            cantidad, nombre = partes

            if nombre.strip().upper() == "PARKING":
                break

            try:
                cantidad = int(cantidad)
            except ValueError:
                continue

            diccionario_productos[nombre.strip()] = cantidad

        return diccionario_productos
    
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
        diccionarioProductos = self.extraerProductos()
        arrayPrecios = self.extraerPrecios()
        arrayNombres = []
        
        contador = 0
        for nombreProducto in diccionarioProductos.keys():
            self.diccionarioProductos[nombreProducto] = (diccionarioProductos[nombreProducto], arrayPrecios[contador])
            contador = contador + 1
            
        return self.diccionarioProductos
        

    
if __name__ == "__main__":
    lector = LectorTicket("ticket.pdf")
    texto = lector.cargarDiccionario()
    for mierda in texto.keys():
        print(mierda, texto[mierda])
    
    