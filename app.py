

import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import streamlit as st
from reportlab.lib.utils import ImageReader
from io import BytesIO
import base64
def generate_pdf(turno_data, turno):
    # Configuración del documento PDF
    filename = f"turnos-{turno}.pdf"
    document_title = f"Concurso Persona con discapacidad"
    document_title_1 = f"Turno: {turno}"
    page_width, page_height = A4

    # Configuración de la tabla
    table_width, table_height = page_width, 15 * mm
    table_x = 0
    table_y = page_height - 50 * mm  # Margen superior para el logo y el título

    # Crear el documento PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
   # c = canvas.Canvas(filename, pagesize=A4)

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
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_width / 2, page_height - 35 * mm, document_title)

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_width / 2, page_height - 45 * mm, document_title_1)
    # Configurar la tabla de datos
    column_widths = [15 * mm, 30 * mm, 85 * mm, 45 * mm, 45 * mm]
    row_height = 20 * mm

    # Dibujar los encabezados de la tabla
    c.setFont("Helvetica", 12)
    c.drawString(table_x + 5 * mm, table_y - 20, "Nº")
    c.drawString(table_x + 20 * mm, table_y - 20, "Documento")
    c.drawString(table_x + 55 * mm, table_y - 20, "Nombre y Apellido")
    c.drawString(table_x + 140 * mm, table_y - 20, "Firma")
    c.drawString(table_x + 180 * mm, table_y - 20, "Observación")


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
               # Agregar el título
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(page_width / 2, page_height - 35 * mm, document_title)

            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(page_width / 2, page_height - 45 * mm, document_title_1)
            # Dibujar los encabezados de la tabla en cada página
            c.setFont("Helvetica", 12)
            c.drawString(table_x + 5 * mm, table_y - 20, "Nº")
            c.drawString(table_x + 20 * mm, table_y - 20, "Documento")
            c.drawString(table_x + 55 * mm, table_y - 20, "Nombre y Apellido")
            c.drawString(table_x + 130 * mm, table_y - 20, "Firma")
            c.drawString(table_x + 180 * mm, table_y - 20, "Observación")


        i += 1
        c.drawString(table_x + 5 * mm, table_y - i * row_height, str(record["Nª"]))
        c.drawString(table_x + 20 * mm, table_y - i * row_height, str(record["documento"]))
        c.drawString(table_x + 50 * mm, table_y - i * row_height, record["nombre_completo"])
        c.drawString(table_x + 150 * mm, table_y - i * row_height, "")
        c.drawString(table_x + 180 * mm, table_y - i * row_height, "")



        for j, column_width in enumerate(column_widths):
            x = table_x + sum(column_widths[:j])
            y = table_y - 40 - i * row_height
            c.rect(x, y, column_width, row_height, stroke=1, fill=0)  # Bordes de la celda

        y = table_y - 40 - i * row_height
        c.rect(table_x, y, table_width, row_height, stroke=1, fill=0)  # Bordes de la fila


    # Guardar y cerrar el documento PDF
    c.save()
    buffer.seek(0)
    # Convertir el archivo PDF a base64
    pdf_bytes = buffer.getvalue()
    encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    # Mostrar enlace de descarga
    href = f'<a href="data:application/pdf;base64,{encoded_pdf}" download="{filename}">Descargar PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

   
# Función para obtener el enlace de descarga del archivo
def get_binary_file_downloader_html(bin_file, file_label='File', file_name='file.pdf'):
    data = bin_file.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">{file_label}</a>'
    return href
# Configurar la interfaz web con Streamlit
st.title("Generador de Planillas de Turnos")

uploaded_file = st.file_uploader("Cargar archivo Excel", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Agrupar por categoría y turno y generar un PDF para cada grupo
    categorias = df["categoria"].unique()
    turnos = df["Turnos"].unique()
    
    if st.button("Descargar todas las planillas"):
        for categoria in categorias:
            for turno in turnos:
                filtro = (df["categoria"] == categoria) & (df["Turnos"] == turno)
                turno_data = df[filtro]
                
                if not turno_data.empty:
                    turno_data = turno_data.sort_values(['apellido'])
                    turno_data = turno_data.reset_index(drop=True)
                    turno_data["Nª"] = turno_data.index + 1
                    generate_pdf(turno_data, turno+ "-" + categoria )

               
        st.success("¡Archivos PDF generados y descargados correctamente!")
    st.header(':blue[Visualiza y descarga]')
    st.markdown("""
        [Planilla de Turno Examen](https://docs.google.com/spreadsheets/d/100Q2umy7HXSt74Tm6NN_aN0fE0kznVb3xCAva8J0v2M/edit?usp=sharing)
        """)
    categorias = df["categoria"].unique()
    turnos = df["Turnos"].unique()
    for categoria in categorias:
        for turno in turnos:
            turno_data = df[df["Turnos"] == turno]
            
            if not turno_data.empty:
                turno_data = turno_data.sort_values(['apellido'])
                turno_data = turno_data.reset_index(drop=True)
                turno_data["Nª"] = turno_data.index + 1
                cantidad_personas = len(turno_data)
                
                st.header(f':blue[Turno]: {turno} -{categoria}')
                st.caption(f':blue[Cantidad de personas por turno]: {cantidad_personas}')
                
                turno_data  # Muestra los datos del turno en la interfaz
                
                if st.button(f"Generar Turno {turno}"):
                    generate_pdf(turno_data, turno)
                    st.success(f"¡Archivo PDF para Turno {turno} generado correctamente!")
