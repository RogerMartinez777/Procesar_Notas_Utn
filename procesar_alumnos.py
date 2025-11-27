# procesar_alumnos.py

# ---------------------------
# IMPORTS (Sección Inicial)
# ---------------------------
import pandas as pd
import re
import json
from unidecode import unidecode
import os                 # <--- Nuevo: Para interactuar con el sistema de archivos
from datetime import datetime # <--- Nuevo: Para generar el timestamp

# ---------------------------
# 1) Pegar aquí el 'roster' tal como viene de UVS con todos los participantes (en este caso para progra 2 fueron 190 filas)
# NOTA: Los caracteres de separación entre nombre y apellido deben ser TABULACIONES (\t) 
# o el parseo fallará. (eso se lo pida a la IA).
# ---------------------------
roster_text = """Maria Julieta\tAbadin Arce
Leonardo\tAcosta Koenig
Kiara\tAdamo
Esteban\tAggero Oggero
FEDERICO MATHIAS\tAGÜERO AGÜERO
Jesus\tAguirre
Jeronimo\tAhumada Torres
Franco Denise\tAlberione
Andres Mariano\tAlmarcha
Franco Maximiliano\tAmarilla
Alvaro\tAmatto
Tomás\tAmaya
Marianela\tArias Gibert
Diego Jesus\tArias Rojo
Federico Nicolas\tAris
Matias Alejandro\tAstorga De Giusti
Facundo\tBalls Boschi
Marco Ticiano\tBarabino
Mauricio Gaston\tBarrera
Gregorio Martín\tBasso
Milagros\tBelbruno
inaki\tBengoechea
Gabriel Ignacio\tBertolin
Franco\tBiancotti
Pablo\tBiasco
Lucas\tBima
Micaela Candelaria\tBini Toledo
Luciano Agustin\tBognanno
Galo\tBonfanti
Juan Manuel\tBosque Bonanate
Oscar Ernesto\tBotta
Diego Angel\tBravo
Franco\tBrizzio Recchia
Marcio Roman\tBulla
Valentina del Valle\tBusceni
Valentin\tCaceres
Alexis\tCaiguara Ramirez
Ignacio Javier\tCantero
Mateo\tCarballo Juarez
Cintia Loana\tCariddi
Maximiliano Daniel\tCarignano Valenzuela
Pablo Emanuel\tCarpio
Manuel Marcelo\tCarranza Oyhanart
Gustavo Daniel\tCarrasco
Tomas Ezequiel\tCarrion
Blanca Rosa\tCarrizo
Thiago Ariel\tCáseres
Nicolás Francisco Alejandro\tCastelli
Cristian Armando\tCastillo
Rafael Ceferino\tCastro
Ludmila Mailen\tCejas
Constanza\tCenteno
Máximo\tCerquatti
Bautista\tChamorro Crettino
Alexis\tChaname
Lorenzo\tCobos Robert
Danisa Belen\tColque
Mateo Adriano\tConte
Fernando\tCorrea
Priscila Magali\tCortez Rearte
Erika Romina\tCuello
Felipe\tCuervo
Gino\tDassano
carmen\tdavila
Luca\tDe Girolamo
Martin\tde lucca
Agustin\tDe Robles
Franco\tDel Giudice
Agustín Ariel\tDi Leo
Cesar Nolasco\tDiaz
Bruno\tDiomedi
Julieta\tDisca
Natasha Eliana\tDrahanczuk
Gonzalo Gabriel\tFernández
Lucas Joaquín\tFernández
Alejo Jeremías\tFernandez Manca
Baltasar\tFerreyra Peuser
Diego Gabriel\tFlores
Aylen Milena\tGarcía Maestri
Nahuel Ceferino\tGatica
Gabriel\tGiaveno
Emiliano\tGimenez
Ana Lucia\tGimenez Herrero
Maximo Emir\tGodoy
Facundo Agustin\tGomez
Ruben Alejo\tGomez
mateo nicolas\tgomez arce
Ornella Selene\tGonzalez
ROMAN ADRIEL\tGONZALEZ
Gisela Inés\tGordillo Grisolia
Jerónimo\tGuemeberena
Matias Daniel\tGulli
Brenda Abigail\tGutierrez
Federico\tGuzman
Braian\tHeredia
Erwin\tHoffman
Franco Nicolas\tIriarte
Tomas\tKimmel
Emma\tKnubel
Francisco Octavio\tLaferriere
Bruno\tLalomia Romagnolo
Martin\tLantieri
Tomas Agustin\tLiendo
Julian\tLlop
Martín\tLozzano
Gonzalo Nicolás\tLudueña Heredia
claudio alejandro\tluna
John\tMackinson
Gonzalo Joaquin\tMainardi
Lautaro Ezequiel\tMainardi
Valentina\tMaldonado
Nolis Lilian\tMaldonado Sarmiento
Tomas\tMammana
Mateo\tMansilla
Santiago\tMarconetto
Thomas\tMariani
Manuel\tMarquez
Camila\tMartín
Roger Damián\tMartinez
Fabrizio Agustin\tMasiero
Alexis Ezequiel\tMedina
Valentino\tMellia Bonetto
Joaquín\tMellibosky
Gissel\tMendez
Lucas Gabriel\tMendoza
Nicolas\tMenendez
Vicente\tMengarelli
Gonzalo\tMercado
Axel Augusto\tMonier
Octavio\tMontoya Lusso
Matías\tMoreno
Emmanuel\tMoreno Halberstadt
Leonardo\tMoscovich
Santiago Agustin\tMoya
Federico\tNavarrete
Josías\tNuñez Linares
Franco\tOlave
Matheo\tOrtiz
Lucas Emanuel\tPadula
Franco\tPalavecino Altamirano
Santiago\tPalavecino Berraondo
José Alberto\tPanichelli
Kiara\tParisi Nakayama
Joaquin\tPastran Verde
Lorenzo\tPaulucci
Pablo\tPerdomo
PABLO\tPERELDA
Kevin Gabriel\tPereyra
Mirko Said\tPereyra Alcazar
Lautaro Gabriel\tPerez
Matias Ezequiel\tPerez
Nicolas\tPerez Orellano
Facundo\tPiscitello
Maximo\tPoletti Torretta
Martín Darío\tPolliotto
Benjamin\tPolzoni
Federico\tPonce de León
Pablo Gabriel\tPrimitz
Nicolas\tProperzi Scheffer
Lucas\tQuevedo Jaime
Tomás\tQuinteros
Ignacio Tomas\tRamallo Herrera
Gonzalo Emanuel\tRamirez
Ramiro Ezequiel\tReyna
Ignacio Valentin\tRios
Baltasar\tRodriguez Teruel
Lucas Miguel\tRojo
Nicolás\tRosencovich
Ignacio Tomas\tRosso
Martin\tRostagno
Agustin Nicolas\tSanchez Garcia
Manuel\tSanchez German
Exequiel Juan Luis\tSantoro
Benjamín\tSchnveitzer
Facundo Matias\tSoria Molina
Ludmila\tSosa
Tomás\tSuarez Galvez
Martina\tTahir
Juan Manuel\tTorrejón
Marcos Ezequiel\tTorres Faba
Matias\tUrbina
Mauricio\tVaca Ferrero
Heber\tVela
Filippo\tVenturi
Giuliana\tVita
Lucio\tWiesek
Joaquin\tzambrano
Lisina\tZanotti
Andres Martin\tZea Cardenas
Stefano\tZoffoli Toro
"""

# ---------------------------
# 2) Pegar aquí los bloques de la columna de nombres de la entrega en cuestion, esta es la actividad 01.
# ---------------------------
activity1_raw = """
Selecciones Marcio Roman Bulla
Seleccione Juan Manuel Bosque Bonanate
Seleccione Nicolas Menendez
Seleccione Nicolas Properzi Scheffer
Seleccione Mateo Carballo Juarez
Seleccione Matías Moreno
Seleccione Martin de lucca
Seleccione Matheo Ortiz
Seleccione Jeronimo Ahumada Torres
Seleccione Benjamin Polzoni
Seleccione Marco Ticiano Barabino
Seleccione Pablo Biasco
Seleccione Valentina del Valle Busceni
Seleccione Fabrizio Agustin Masiero
Seleccione Ludmila Sosa
Seleccione Jerónimo Guemeberena
Seleccione Heber Vela
Seleccione Danisa Belen Colque
Seleccione Benjamín Schnveitzer
Seleccione Tomas Ezequiel Carrion
Seleccione Franco Del Giudice
Seleccione carmen davila
Seleccione Pablo Gabriel Primitz
Seleccione Gonzalo Joaquin Mainardi
Seleccione Tomas Agustin Liendo
Seleccione Matias Ezequiel Perez
Seleccione Tomás Quinteros
Seleccione Cesar Nolasco Diaz
Seleccione Emiliano Gimenez
Seleccione Leonardo Acosta Koenig
Seleccione Joaquin Pastran Verde
Seleccione ROMAN ADRIEL GONZALEZ
Seleccione Lorenzo Paulucci
Seleccione Nicolás Francisco Alejandro Castelli
Seleccione Manuel Marquez
Seleccione Ignacio Tomas Ramallo Herrera
Seleccione Federico Ponce de León
Seleccione Emmanuel Moreno Halberstadt
Seleccione Máximo Cerquatti
Seleccione Ramiro Ezequiel Reyna
Seleccione Rafael Ceferino Castro
Seleccione Lucas Quevedo Jaime
Seleccione Martina Tahir
Seleccione Lucio Wiesek
Seleccione Stefano Zoffoli Toro
Seleccione Cristian Armando Castillo
Seleccione Cintia Loana Cariddi
Seleccione Kiara Adamo
Seleccione Baltasar Rodriguez Teruel
Seleccione Galo Bonfanti
Seleccione Gissel Mendez
Seleccione Maximo Poletti Torretta
Seleccione Vicente Mengarelli
Seleccione Gonzalo Gabriel Fernández
Seleccione Valentina Maldonado
Seleccione Tomas Kimmel
Seleccione Marcos Ezequiel Torres Faba
Seleccione Federico Nicolas Aris
Seleccione Martin Lantieri
Seleccione Ornella Selene Gonzalez
Seleccione Matias Alejandro Astorga De Giusti
Seleccione Lucas Emanuel Padula
Seleccione Facundo Agustin Gomez
Seleccione Ruben Alejo Gomez
Seleccione Nolis Lilian Maldonado Sarmiento
Seleccione Valentino Mellia Bonetto
Seleccione Lucas Miguel Rojo
Seleccione Leonardo Moscovich
Seleccione Gisela Inés Gordillo Grisolia
Seleccione Franco Nicolas Iriarte
Seleccione Mirko Said Pereyra Alcazar
Seleccione Bruno Lalomia Romagnolo
Seleccione Pablo Perdomo
Seleccione Gino Dassano
Seleccione Mauricio Vaca Ferrero
Seleccione Tomás Amaya
Seleccione Agustin Nicolas Sanchez Garcia
Seleccione Ludmila Mailen Cejas
Seleccione Franco Maximiliano Amarilla
Seleccione Ignacio Javier Cantero
Seleccione José Alberto Panichelli
Seleccione Franco Denise Alberione
Seleccione Gregorio Martín Basso
Seleccione Ignacio Valentin Rios
Seleccione Octavio Montoya Lusso
Seleccione Nahuel Ceferino Gatica
Seleccione Thomas Mariani
Seleccione Lorenzo Cobos Robert
Seleccione Julieta Disca
Seleccione Kevin Gabriel Pereyra
Seleccione Santiago Agustin Moya
Seleccione Facundo Matias Soria Molina
Seleccione Martín Lozzano
Seleccione PABLO PERELDA
Seleccione Camila Martín
Seleccione Aylen Milena García Maestri
Seleccione Priscila Magali Cortez Rearte
Seleccione Mateo Adriano Conte
Seleccione Lucas Bima
Seleccione Juan Manuel Torrejón
Seleccione inaki Bengoechea
Seleccione Diego Jesus Arias Rojo
Seleccione Ignacio Tomas Rosso
"""

activity2_raw = """
Marcio Roman Bulla
Seleccione Juan Manuel Bosque Bonanate
Seleccione Mateo Carballo Juarez
Seleccione Jeronimo Ahumada Torres
Seleccione Benjamin Polzoni
Seleccione Marco Ticiano Barabino
Seleccione Pablo Biasco
Seleccione Fabrizio Agustin Masiero
Seleccione Ludmila Sosa
Seleccione Jerónimo Guemeberena
Seleccione Danisa Belen Colque
Seleccione Tomas Ezequiel Carrion
Seleccione Franco Del Giudice
Seleccione carmen davila
Seleccione Pablo Gabriel Primitz
Seleccione Tomas Agustin Liendo
Seleccione Matias Ezequiel Perez
Seleccione Cesar Nolasco Diaz
Seleccione Emiliano Gimenez
Seleccione Joaquin Pastran Verde
Seleccione ROMAN ADRIEL GONZALEZ
Seleccione Lorenzo Paulucci
Seleccione Andres Mariano Almarcha
Seleccione Nicolás Francisco Alejandro Castelli
Seleccione Manuel Marquez
Seleccione Ignacio Tomas Ramallo Herrera
Seleccione Santiago Marconetto
Seleccione Emmanuel Moreno Halberstadt
Seleccione Ramiro Ezequiel Reyna
Seleccione Rafael Ceferino Castro
Seleccione Lucas Quevedo Jaime
Seleccione Martina Tahir
Seleccione Stefano Zoffoli Toro
Seleccione Cristian Armando Castillo
Seleccione Baltasar Rodriguez Teruel
Seleccione Galo Bonfanti
Seleccione Vicente Mengarelli
Seleccione Gonzalo Gabriel Fernández
Seleccione Valentina Maldonado
Seleccione Tomas Kimmel
Seleccione Marcos Ezequiel Torres Faba
Seleccione Federico Nicolas Aris
Seleccione Martin Lantieri
Seleccione Lucas Emanuel Padula
Seleccione Nolis Lilian Maldonado Sarmiento
Seleccione Valentino Mellia Bonetto
Seleccione Leonardo Moscovich
Seleccione Gisela Inés Gordillo Grisolia
Seleccione Franco Nicolas Iriarte
Seleccione Bruno Lalomia Romagnolo
Seleccione Tomás Amaya
Seleccione Agustin Nicolas Sanchez Garcia
Seleccione Ludmila Mailen Cejas
Seleccione Franco Maximiliano Amarilla
Seleccione José Alberto Panichelli
Seleccione Ignacio Valentin Rios
Seleccione Lorenzo Cobos Robert
Seleccione Julieta Disca
Seleccione Santiago Agustin Moya
Seleccione Facundo Matias Soria Molina
Seleccione Martín Lozzano
Seleccione Camila Martín
Seleccione Aylen Milena García Maestri
Seleccione Priscila Magali Cortez Rearte
Seleccione Lucas Bima
Seleccione Juan Manuel Torrejón
Seleccione inaki Bengoechea
Seleccione Diego Jesus Arias Rojo
"""

activity3_raw = """
Seleccione Marcio Roman Bulla
Seleccione Mateo Carballo Juarez
Seleccione Marco Ticiano Barabino
Seleccione Fabrizio Agustin Masiero
Seleccione Ludmila Sosa
Seleccione Jerónimo Guemeberena
Seleccione Tomas Ezequiel Carrion
Seleccione carmen davila
Seleccione Pablo Gabriel Primitz
Seleccione Tomas Agustin Liendo
Seleccione Matias Ezequiel Perez
Seleccione ROMAN ADRIEL GONZALEZ
Seleccione Lorenzo Paulucci
Seleccione Nicolás Francisco Alejandro Castelli
Seleccione Rafael Ceferino Castro
Seleccione Lucas Quevedo Jaime
Seleccione Martina Tahir
Seleccione Cristian Armando Castillo
Seleccione Baltasar Rodriguez Teruel
Seleccione Galo Bonfanti
Seleccione Gonzalo Gabriel Fernández
Seleccione Valentina Maldonado
Seleccione Marcos Ezequiel Torres Faba
Seleccione Lucas Miguel Rojo
Seleccione Bruno Lalomia Romagnolo
Seleccione Ludmila Mailen Cejas
Seleccione José Alberto Panichelli
Seleccione Maria Julieta Abadin Arce
Seleccione Santiago Agustin Moya
Seleccione Facundo Matias Soria Molina
Seleccione Camila Martín
Seleccione Aylen Milena García Maestri
Seleccione Priscila Magali Cortez Rearte
Seleccione Lucas Bima
Seleccione Juan Manuel Torrejón
Seleccione Ignacio Tomas Rosso
"""

activity4_raw = """
Mateo Carballo Juarez
Seleccione Marco Ticiano Barabino
Seleccione Fabrizio Agustin Masiero
Seleccione Tomas Ezequiel Carrion
Seleccione carmen davila
Seleccione Matias Ezequiel Perez
Seleccione Emiliano Gimenez
Seleccione ROMAN ADRIEL GONZALEZ
Seleccione Nicolás Francisco Alejandro Castelli
Seleccione Brenda Abigail Gutierrez
Seleccione Emmanuel Moreno Halberstadt
Seleccione Martina Tahir
Seleccione Cristian Armando Castillo
Seleccione Baltasar Rodriguez Teruel
Seleccione Galo Bonfanti
Seleccione Valentina Maldonado
Seleccione Marcos Ezequiel Torres Faba
Seleccione Federico Nicolas Aris
Seleccione Ornella Selene Gonzalez
Seleccione Bruno Lalomia Romagnolo
Seleccione Ludmila Mailen Cejas
Seleccione Franco Maximiliano Amarilla
Seleccione José Alberto Panichelli
Seleccione Maria Julieta Abadin Arce
Seleccione Santiago Agustin Moya
Seleccione Facundo Matias Soria Molina
Seleccione Camila Martín
Seleccione Aylen Milena García Maestri
Seleccione Priscila Magali Cortez Rearte
Seleccione Lucas Bima
Seleccione Ignacio Tomas Rosso
"""

activity5_raw = """
Seleccione Mateo Carballo Juarez
Seleccione carmen davila
Seleccione Martina Tahir
Seleccione Franco Maximiliano Amarilla
"""

# ---------------------------
# 3) Funciones de normalización y extracción
# ---------------------------
def normalize_text(s):
    if s is None:
        return ""
    s = s.strip()
    # eliminar múltiples espacios
    s = re.sub(r'\s+', ' ', s)
    # remover tildes y normalizar
    s = unidecode(s)
    return s.lower()

def parse_roster(text):
    rows = []
    for line in text.strip().splitlines():
        # Usamos split('\t') para SEPARAR EXACTAMENTE en la tabulación.
        parts = line.split("\t")
        
        # Debe haber al menos dos partes: Nombre Completo y Apellido Completo (algunos tienen como 3 nombres y 2 apellidos..)
        if len(parts) >= 2:
            # La parte 0 es "el" o "los" Nombres
            nombre = parts[0].strip()
            # La parte 1 es "el" o "los" Apellidos
            apellidos = parts[1].strip()
            
            rows.append({"nombre": nombre, "apellidos": apellidos, "actividades_hechas": 0})
        else:
            # Si no encuentra el tabulador (lo cual es raro si la fuente es limpia)
            # Imprimimos una advertencia para que sepas qué línea corregir.
            print(f"ADVERTENCIA: Falla de formato en roster, línea ignorada: {line}")
            
    return rows

def extract_activity_names(raw):
    names = []
    # Limpiamos corchetes innecesarios que estaban en la fuente de datos
    raw = raw.replace('[', '').replace(']', '') 
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        
        # **Ajuste para Robustez:** Eliminar cualquier carácter que NO sea letra o espacio
        # al principio de la línea (ej. 's ' o '1. ' o ' - ')
        line = re.sub(r'^[^a-z\s]+', '', line, flags=re.IGNORECASE)
        
        # quitar palabras como "Seleccione" o "Selecciones" (esas vienen de pecho de la columna nombres de UVS)
        line = re.sub(r'^(Seleccione|Selecciones)\s*[:\-–]*\s*', '', line, flags=re.IGNORECASE)
        line = line.replace("MCMateo", "Mateo ")
        if line:
            names.append(line.strip())
    return [re.sub(r'\s+', ' ', n).strip() for n in names]

def key_from_fullname(full_nombre, full_apellidos):
    # Primer nombre = primer token del campo "nombre"
    first = normalize_text(full_nombre).split()[0] if normalize_text(full_nombre) else ""
    last = normalize_text(full_apellidos).split()[-1] if normalize_text(full_apellidos) else ""
    return (first, last)

def key_from_activity_name(fullname):
    # Tomamos primer token como primer nombre y último token como apellido final
    s = normalize_text(fullname)
    parts = s.split()
    if not parts:
        return ("","")
    return (parts[0], parts[-1])

# ---------------------------
# 4) Procesamiento (Core de la lógica)
# ---------------------------
roster = parse_roster(roster_text)

acts = []
for raw in (activity1_raw, activity2_raw, activity3_raw, activity4_raw, activity5_raw):
    acts.append(extract_activity_names(raw))

# 1. Index roster for fast match by (first, last)
index = {}
for i, r in enumerate(roster):
    k = key_from_fullname(r["nombre"], r["apellidos"])
    index.setdefault(k, []).append(i)

# 2. Para cada actividad, intentar match
for act in acts:
    for name in act:
        k_act = key_from_activity_name(name)
        
        # Intento 1: Búsqueda rápida por clave indexada
        if k_act in index:
            for i in index[k_act]:
                roster[i]["actividades_hechas"] += 1
        else:
            # Intento 2 (Fallback): Búsqueda secuencial (para alumnos mal parseados)
            found = False
            for i, r in enumerate(roster):
                 k_roster = key_from_fullname(r["nombre"], r["apellidos"])
                 # Coincidencia directa de claves normalizadas
                 if k_act[0] == k_roster[0] and k_act[1] == k_roster[1]:
                     roster[i]["actividades_hechas"] += 1
                     found = True
                     break
            
            if not found:
                # No encontrado: mostrar en un log
                print("NO ENCONTRADO (actividad):", name)

# ---------------------------
# 5) Guardar archivos (Lógica de carpeta dinámica y Formato Avanzado Excel)
# ---------------------------

# 1. (Lógica de carpeta y timestamp, no cambia)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"REPORTE_{timestamp}"

try:
    os.makedirs(output_dir)
except Exception as e:
    print(f"Error fatal al crear el directorio {output_dir}: {e}")
    exit()

excel_path = os.path.join(output_dir, "alumnos_actividades.xlsx")
json_path = os.path.join(output_dir, "alumnos_actividades.json")

# 2. Generar el DataFrame
df = pd.DataFrame(roster)

# 3. Renombrar las columnas para que coincidan con el formato de cabecera
# Aplicamos "CamelCase" y el texto "Actividades Realizadas"
df.rename(columns={
    'nombre': 'Nombre',
    'apellidos': 'Apellidos',
    'actividades_hechas': 'Actividades Realizadas' 
}, inplace=True)

# 4. Guardar Excel con formato
# -----------------------------
writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
df.to_excel(writer, sheet_name='Reporte Alumnos', index=False)

# Acceder a los objetos de xlsxwriter
workbook = writer.book
worksheet = writer.sheets['Reporte Alumnos']

# 5. Definir el formato COMPLETO del encabezado
header_format = workbook.add_format({
    'bold': True,                   # Negrita
    'fg_color': '#FFFF00',          # Color de fondo (Amarillo)
    'border': 1,                    # Borde
    'align': 'center',              # Alineación Horizontal: Centrado
    'valign': 'vcenter',            # Alineación Vertical: Centrado
    'text_wrap': True               # Ajustar texto (Wrap Text)
})

# 6. Aplicar el formato a las celdas de la cabecera y ajustar ancho
for col_num, value in enumerate(df.columns.values):
    
    # Aplicar formato al encabezado (fila 0)
    worksheet.write(0, col_num, value, header_format)
    
    # Ajustar el ancho de las columnas
    if value == 'Nombre' or value == 'Apellidos':
        width = 25
    elif value == 'Actividades Realizadas':
        # Esta columna necesita más ancho para que se active el 'text_wrap'
        width = 15 
    else:
        width = 10
        
    worksheet.set_column(col_num, col_num, width) 

# También ajustamos la altura de la fila de encabezado para ver el texto envuelto
worksheet.set_row(0, 30) 

# 7. Cerrar el escritor de Excel para guardar el archivo
writer.close()
# -----------------------------

# 8. Guardar JSON (no cambia)
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(roster, f, ensure_ascii=False, indent=2)

print("Archivos generados en el directorio:")
print(f"- {output_dir}/alumnos_actividades.xlsx - formato mejorado")
print(f"- {output_dir}/alumnos_actividades.json")