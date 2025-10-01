from db import connect_db
from extract import extract_newdocs
from transform import export_excel, enviar_correo

def main():

  conn = connect_db()
  cursor = conn.cursor()
  data_docs = extract_newdocs(cursor)
  file = export_excel(data_docs)
  enviar_correo(file)

if __name__ == "__main__":
  main()