# 📊 PriceList

**PriceList** es una aplicación para Android desarrollada con **Python** y **Kivy**, diseñada para analizar tickets de supermercado en formato **PDF**. Actualmente está centrada en el supermercado **Mercadona**, pero se ha desarrollado de forma que pueda adaptarse fácilmente a otros supermercados en el futuro.

## 🧠 ¿Qué hace?

- 📥 Importa tickets de Mercadona en formato `.pdf`
- 🔍 Extrae automáticamente los productos comprados y sus precios
- 🗃️ Organiza los productos en categorías: alimentos envasados, frescos, bebidas, congelados, cuidado personal y limpieza
- 📈 Muestra el precio más alto, más bajo, la media y el del último ticket para cada producto
- 📆 Permite consultar precios por fecha para analizar la evolución del gasto y detectar aumentos de precio (inflación)

## 🛠️ Tecnologías utilizadas

- **Python** 🐍
- **Kivy** – para la interfaz de usuario
- **pdfplumber** – para la lectura de tickets PDF
- **SQLite** – base de datos local para almacenar los productos y sus precios

## 📲 Funcionamiento

1. El usuario importa un ticket en formato `.pdf`
2. La app analiza el contenido y extrae los productos y sus precios
3. Los datos se guardan en una base de datos local por categorías
4. El usuario puede:
   - Navegar por las familias y subcategorías
   - Consultar la evolución de precios por producto y fecha
   - Visualizar las estadísticas de precios (último, medio, mínimo, máximo)

## 🔮 Mejoras futuras

- Compatibilidad con otros supermercados (Carrefour, Lidl, etc.)
- Versión para iOS
- Arreglar errores
