

import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
import streamlit as st
from reportlab.lib.utils import ImageReader

def generate_pdf(turno_data, turno):
    # Configuración del documento PDF
    filename = f"turnos_{turno}.pdf"
    document_title = f"Concurso Persona con discapacidad - Turno {turno}"
    page_width, page_height = letter

    # Configuración de la tabla
    table_width, table_height = page_width, 15 * mm
    table_x = 0
    table_y = page_height - 50 * mm  # Margen superior para el logo y el título

    # Crear el documento PDF
    c = canvas.Canvas(filename, pagesize=letter)

    # Agregar el logo
    logo_path = "logo.png"  # Ruta al archivo de imagen del logo
    logo_image = ImageReader(logo_path)

    # Obtener las dimensiones originales del logo
    logo_width = logo_image.getSize()[0]
    logo_height = logo_image.getSize()[1]

    # Calcular la escala para mantener el aspecto original del logo
    logo_scale = min((page_height - 40) / logo_height, 1.0)

    # Calcular la posición del logo en el margen izquierdo
    logo_x = 10
    logo_y = page_height - (logo_height * logo_scale) - 10

    # Dibujar el logo
    c.drawImage(logo_image, logo_x, logo_y, logo_width * logo_scale, logo_height * logo_scale)

    # Agregar el título
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_width / 2, page_height - 40 * mm, document_title)

    # Configurar la tabla de datos
    column_widths = [20 * mm, 60 * mm, 60 * mm, 60 * mm]
    row_height = 20 * mm
    turno_data = turno_data.reset_index(drop=True)
    turno_data["Nª"] = turno_data.index + 1

# Dibujar los encabezados de la tabla
    c.setFont("Helvetica", 12)
    c.drawString(table_x + 5 * mm, table_y - 20, "Nº")
    c.drawString(table_x + 30 * mm, table_y - 20, "Documento")
    c.drawString(table_x + 60 * mm, table_y - 20, "Nombre y Apellido")
    c.drawString(table_x + 120 * mm, table_y - 20, "Firma")
    c.drawString(table_x + 180 * mm, table_y - 20, "Observación")

    # Dibujar las filas de la tabla con los datos
    c.setFont("Helvetica", 12)
    i = 0
    for _, record in turno_data.iterrows():
        # Si la fila actual excede el espacio disponible en la página, agregar una nueva página
        if (i + 1) * row_height > table_y - 40 * mm:
            c.showPage()  # Agregar nueva página
            i = 0

            # Dibujar el logo en cada página
            c.drawImage(logo_image, logo_x, logo_y, logo_width * logo_scale, logo_height * logo_scale)

            # Agregar el título en cada página
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(page_width / 2, page_height - 40 * mm, document_title)

            # Dibujar los encabezados de la tabla en cada página
            c.setFont("Helvetica", 12)
            c.drawString(table_x + 5 * mm, table_y - 20, "Nº")
            c.drawString(table_x + 30 * mm, table_y - 20, "Documento")
            c.drawString(table_x + 60 * mm, table_y - 20, "Nombre y Apellido")
            c.drawString(table_x + 120 * mm, table_y - 20, "Firma")
            c.drawString(table_x + 180 * mm, table_y - 20, "Observación")

        i += 1

        c.drawString(table_x + 5 * mm, table_y - (i + 1) * row_height, str(record["Nª"]))
        c.drawString(table_x + 30 * mm, table_y - (i + 1) * row_height, str(record["documento"]))
        c.drawString(table_x + 60 * mm, table_y - (i + 1) * row_height, record["nombre_completo"])
        c.drawString(table_x + 120 * mm, table_y - (i + 1) * row_height, "")
        c.drawString(table_x + 180 * mm, table_y - (i + 1) * row_height, "")

# Guardar y cerrar el documento PDF
    c.save()

# Configurar la interfaz web con Streamlit
st.title("Generador de Planillas de Turnos")

uploaded_file = st.file_uploader("Cargar archivo Excel", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Agrupar por turnos y generar un PDF para cada grupo
    turnos = df["Turnos"].unique()
    for turno in turnos:
        turno_data = df[df["Turnos"] == turno]
        if not turno_data.empty:
            if st.button(f"Generar Turno {turno}"):
                generate_pdf(turno_data, turno)
                st.success(f"¡Archivo PDF para Turno {turno} generado correctamente!")

    if st.button("Descargar Todo"):
        for turno in turnos:
            turno_data = df[df["Turnos"] == turno]
            if not turno_data.empty:
                generate_pdf(turno_data, turno)
        st.success("¡Archivos PDF generados y descargados correctamente!")
