from openpyxl import Workbook
from openpyxl.styles import Font
from datetime import datetime
import os
from dotenv import load_dotenv
import yagmail

load_dotenv()

MAIL_AUTOR = os.getenv("MAIL_AUTOR")
APP_GMAIL_PASS = os.getenv("APP_GMAIL_PASS")
MAIL_DESTINO = os.getenv("MAIL_DESTINO")
MAIL_DESTINATARIOS = os.getenv("MAIL_DESTINATARIOS").split(",")

today = datetime.now()

def export_excel(data_docs):
    
  # Hoja 1 - Docs e infs. ult. semana

  wb = Workbook()
  ws = wb.active
  ws.title = "Docs e infs. ult. semana"

  headers = [ "ALUMNO ID", "NOMBRE", "OS", "NOMBRE DOC/INF", "FEC CARGA", "TIPO", 
                      "UBIC. CAT.", "UBIC. AÑO", "USUARIO DE CARGA" ]
  
  ws.append(headers)

  for cell in ws[1]:
      cell.font = Font(bold=True)

  for row in data_docs:
    alumno_id = row[1]
    alumno = row[2]
    os = row[3]
    nombre_doc = row[4]
    fec_carga = row[5]
    tipo = row[10]
    docalumnoseccion_nombre = row[6]
    anio = row[7]
    usuario = row[8]

    ws.append([alumno_id, alumno, os, nombre_doc, fec_carga, tipo, docalumnoseccion_nombre, anio, usuario])

  nombre_archivo = f"reporte_documentacion_{today.strftime('%Y-%m-%d')}.xlsx"
  wb.save(nombre_archivo)
  print(f"Archivo Excel generado: {nombre_archivo}")
  return nombre_archivo

def enviar_correo(nombre_archivo):
  try:
    yag = yagmail.SMTP(MAIL_AUTOR, APP_GMAIL_PASS)
    yag.send(
      to=MAIL_DESTINATARIOS,
      subject="Reporte general de Documentacion",
      contents="Buenos días, se adjunta el reporte del área de Documentación. ¡Saludos!",
      attachments=nombre_archivo
    )
    print("Correo enviado correctamente.")
  except Exception as e:
    print("Error al enviar el correo:", e)