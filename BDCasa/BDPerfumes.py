from tkinter import Tk, Button, Entry, Label, ttk, PhotoImage, StringVar, Frame, messagebox, IntVar, Toplevel, filedialog, END
from tkinter.font import Font
import sqlite3
from time import strftime
from datetime import datetime
from PIL import Image, ImageTk
import cv2
import imutils
import os
from xlsxwriter import workbook
import locale # Cambiar a español la localidad

BDP = Tk()

BDP.title("Perfumes")
BDP.attributes('-fullscreen', True)
BDP.resizable(0,0)
BDP.config(background = "blue3")
#BDP.wm_iconbitmap(".ico")

fuente = Font(family="Gill Sans Ultra Bold", size=12)
fuente_titulo = Font(family="Gill Sans Utra Bold", size=18, weight='bold')
fuente_titulogrande = Font(family="Gill Sans Ultra Bold", size=35, weight='bold')
fuente_cuerpo = Font(family="Gill Sans Ultra Bold", size=12, weight='normal')
locale.setlocale(locale.LC_ALL, 'es-MX')

filename = PhotoImage(file = 'Imagenes y Logos/Fondo_Azul.png') # Imagen de Fondo 
background_label = Label(BDP, image=filename).place(x=0, y=0, relwidth=1, relheight=1)

"CONSULTAS SQL"

# Conexión con la base de datos
conexion = sqlite3.connect('BDCasa.db')

# Inserta los datos en la tabla
def insertar_data(marca, nombre, color, famolfativa, clima, año, tipo, foto, estela, duracion):
    cursor = conexion.cursor()
    cursor.execute('''INSERT INTO Perfumes (MARCA, NOMBRE, COLOR, FAMOLFATIVA, CLIMA, AÑO, TIPO, FOTO, ESTELA, DURACION) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (marca, nombre, color, famolfativa, clima, año, tipo, foto, estela, duracion))
    conexion.commit()
    cursor.close()

# Consulta todas las marcas de la tabla
def consultar_marcas():
    cursor = conexion.cursor()
    cursor.execute("SELECT MARCA FROM Perfumes ")
    datos = cursor.fetchall()
    Marcas = []
    for marcas in datos: Marcas.append(marcas[0])
    for marcas in Marcas: 
        while(Marcas.count(marcas) > 1): Marcas.remove(marcas)
    Marcas.sort()
    return Marcas

# Consulta todos los nombres de una misma marca de la tabla
def consultar_nombres(marca):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Perfumes WHERE MARCA = ? ", (marca, ))
    datos = cursor.fetchall()
    Nombres = []
    for perfumes in datos:
        for valores in perfumes:
            if valores == marca: Nombres.append(perfumes[1])
    Nombres.sort()
    return Nombres

# Consulta todos los nombres de la tabla
def consulta_nombres():
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM Perfumes')
    datos = cursor.fetchall()
    Nombres = []
    for perfumes in datos: Nombres.append(perfumes[1])
    Nombres.sort()
    return Nombres

# Regresa el número total de perfumes en la base
def numero_perfumes():
    cursor = conexion.cursor()
    cursor.execute('SELECT NOMBRE FROM Perfumes')
    datos = cursor.fetchall()
    return len(datos)

# Regresa toda la tabla
def base_completa():
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM Perfumes')
    datos = cursor.fetchall()
    return datos

# Consulta los datos con base en la marca y el nombre en la tabla
def consulta_data(marca=None, nombre=None):
    if marca != None and nombre != None:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Perfumes WHERE MARCA = ? AND NOMBRE = ?", (marca, nombre))
        datos = cursor.fetchall()
        return datos
    elif marca == None:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Perfumes WHERE NOMBRE = ?", (nombre, ))
        datos = cursor.fetchall()
        return datos

# Elimina un elemento de la tabla
def eliminar_data(nombre):
        cursor = conexion.cursor()
        cursor.execute('''DELETE FROM Perfumes WHERE NOMBRE = ? ''', (nombre, ))
        conexion.commit()
        cursor.close()

# Actualiza los valores en la tabla incluyendo la imagen
def actualizar_data_completa(marca, nombre, color, famolfativa, clima, año, tipo, foto, estela, duracion, name):
    cursor = conexion.cursor()
    cursor.execute('''UPDATE Perfumes SET MARCA = ? , NOMBRE = ? , COLOR = ? , FAMOLFATIVA = ? , CLIMA = ? , AÑO = ? , TIPO = ? , FOTO = ? , ESTELA = ? , DURACION = ? WHERE NOMBRE = ? ''', (marca, nombre, color, famolfativa, clima, año, tipo, foto, estela, duracion, name))
    dato = cursor.row_factory
    conexion.commit()
    cursor.close()

# Actualiza los valores de la tabla sin incluir la imagen
def actualizar_data_sin_foto(marca, nombre, color, famolfativa, clima, año, tipo, estela, duracion, name):
    cursor = conexion.cursor()
    cursor.execute('''UPDATE Perfumes SET MARCA = ? , NOMBRE = ? , COLOR = ? , FAMOLFATIVA = ? , CLIMA = ? , AÑO = ? , TIPO = ? , ESTELA = ? , DURACION = ? WHERE NOMBRE = ? ''', (marca, nombre, color, famolfativa, clima, año, tipo, estela, duracion, name))
    dato = cursor.row_factory
    conexion.commit()
    cursor.close()

# Consulta el elemento de la tabla por sus caracteristicas
def consulta_por_caracteristicas(caracteristica, opcion):
    if caracteristica == "FAMILIA OLFATIVA":
        cursor = conexion.cursor()
        cursor.execute("SELECT NOMBRE FROM Perfumes WHERE FAMOLFATIVA = ? ", (opcion,))
        datos = cursor.fetchall()
        valores = []
        for perfumes in datos: valores.append(perfumes[0])
        return valores
    elif caracteristica == "AÑO":
        cursor = conexion.cursor()
        cursor.execute("SELECT NOMBRE FROM Perfumes WHERE AÑO = ? ", (opcion,))
        datos = cursor.fetchall()
        valores = []
        for perfumes in datos: valores.append(perfumes[0])
        return valores
    elif caracteristica == "COLOR":
        cursor = conexion.cursor()
        cursor.execute("SELECT NOMBRE FROM Perfumes WHERE COLOR = ? ", (opcion,))
        datos = cursor.fetchall()
        valores = []
        for perfumes in datos: valores.append(perfumes[0])
        return valores
    elif caracteristica == "GÉNERO":
        cursor = conexion.cursor()
        cursor.execute("SELECT NOMBRE FROM Perfumes WHERE TIPO = ? ", (opcion,))
        datos = cursor.fetchall()
        valores = []
        for perfumes in datos: valores.append(perfumes[0])
        return valores
    elif caracteristica == "CLIMA":
        cursor = conexion.cursor()
        cursor.execute("SELECT NOMBRE FROM Perfumes WHERE CLIMA = ? ", (opcion,))
        datos = cursor.fetchall()
        valores = []
        for perfumes in datos: valores.append(perfumes[0])
        return valores
    elif caracteristica == "DURACIÓN":
        cursor = conexion.cursor()
        cursor.execute("SELECT NOMBRE FROM Perfumes WHERE DURACION = ? ", (opcion,))
        datos = cursor.fetchall()
        valores = []
        for perfumes in datos: valores.append(perfumes[0])
        return valores
    elif caracteristica == "ESTELA":
        cursor = conexion.cursor()
        cursor.execute("SELECT NOMBRE FROM Perfumes WHERE ESTELA = ? ", (opcion,))
        datos = cursor.fetchall()
        valores = []
        for perfumes in datos: valores.append(perfumes[0])
        return valores
    else: return ["No funciona"]

# Realiza un respaldo de la base cada vez que se agrega un nuevo elemento a la base
def realizar_respaldo():
    back_up = sqlite3.connect('BDPerfumesBK.db')
    conexion.backup(back_up)
    back_up.close()
        
"MANEJO DE LAS IMÁGENES"

image = None # Variable global para la imagen
# Convertir la imagen a binario
def converir_blob(ruta_foto):
    with open(ruta_foto, 'rb') as f:
        blob = f.read()
    return blob

# Función para hacer visible las imágenes
def procesar_imagen(foto):
    if len(foto) > 0:
            global image
        
    # Leer la imagen de entrada
    image = cv2.imread(foto)
    imageShow = imutils.resize(image, width=255, height=355)
    imageShow = cv2.cvtColor(imageShow, cv2.COLOR_BGR2RGBA) #COLOR_BGR2RGB

    # Para visualizar la imagen de entrada en la GUI
    im = Image.fromarray(imageShow)
    img = ImageTk.PhotoImage(image=im)
    return img

"FUNCIONES DE LA APLICACIÓN"

# Función botón para cerrar la aplicación
def salir(): 
    BDP.destroy()
    BDP.quit()

# Función botón para minimizar la pantalla
def minimizar():
    BDP.iconify()

# Función para la hora
def HORA():
        hora = strftime('%I:%M:%S  %p').upper() # %I: Para reloj de 12 horas y %p: Para AM y PM 
        hora_label.config(text=hora, font=Font(family="Gill Sans Ultra Bold", size=16))
        hora_label.after(1000, HORA)

# Función para la fecha
def FECHA():
        return datetime.now().strftime('%A, %d de %B').capitalize()

"FUNCIONES DE LOS BOTONES DENTRO DE LA INTERFAZ"

# Da las listas con los valores que se utilizan en los combobox en la ventana de agregar y actualizar
def opciones_combobox(valor=0):
    """Valor 1 = Género -- Valor 2 = Clima -- Valor 3 = Duración -- Valor 4 = Estela -- Valor 5 = Características -- Valor 6 = Familia Olfativa -- Valor 7 = Año -- Valor 8 = Color"""
    if valor == 1:
        valores = ["UNISEX", "MASCULINO", "FEMENINO"]
    elif valor == 2:
        valores = ["OTOÑO / INVIERNO", "PRIMAVERA / VERANO", "VERSATIL"]
    elif valor == 3:
        valores = ["CORTA", "MEDIANA", "LARGA"]
    elif valor == 4:
        valores = ["MODERADA", "PESADA", "LIGERA"]
    elif valor == 5:
        valores = ["FAMILIA OLFATIVA", "AÑO", "COLOR", "GÉNERO", "CLIMA", "DURACIÓN", "ESTELA"]
    elif valor == 6:
        cursor = conexion.cursor()
        cursor.execute("SELECT FAMOLFATIVA FROM Perfumes ")
        datos = cursor.fetchall()
        valores = []
        for marcas in datos: valores.append(marcas[0])
        for marcas in valores: 
            while(valores.count(marcas) > 1): valores.remove(marcas)
        valores.sort()
    elif valor == 7:
        cursor = conexion.cursor()
        cursor.execute("SELECT AÑO FROM Perfumes ")
        datos = cursor.fetchall()
        valores = []
        for marcas in datos: valores.append(marcas[0])
        for marcas in valores: 
            while(valores.count(marcas) > 1): valores.remove(marcas)
        valores.sort()
    elif valor == 8:
        cursor = conexion.cursor()
        cursor.execute("SELECT COLOR FROM Perfumes ")
        datos = cursor.fetchall()
        valores = []
        for marcas in datos: valores.append(marcas[0])
        for marcas in valores: 
            while(valores.count(marcas) > 1): valores.remove(marcas)
        valores.sort()
    else: valores = None
    return valores

# Función para exportar la base de datos a un archivo .xlsx
def excel():
    ruta = filedialog.asksaveasfilename(title = "Guardar como...", filetypes = (("Archivo Excel",
    "*.xlsx"),("Archivo PDF","*.pdf"),("Todos los Archivos","*.*")))
    name = ruta + '.xlsx'
    if name == '.xlsx':
        messagebox.showinfo('PROCESO CANCELADO', 'SE CANCELÓ EL GUARDADO.')
    else:
        archivo = workbook(name)
        hoja = archivo.add_worksheet()
        bold = archivo.add_format({'bold': True})
        datos = sorted(base_completa())
        fila = 1
        columna = 0
        for f in range(len(datos)):
            for c in range(len(datos[f])):
                if c == 9:
                    break
                elif c >= 7:
                    hoja.write(fila, c, datos[f][c+1])
                else:
                    hoja.write('A1', 'MARCA', bold)
                    hoja.write('B1', 'NOMBRE', bold)
                    hoja.write('C1', 'COLOR', bold)
                    hoja.write('D1', 'FAMILIA OLFATIVA', bold)
                    hoja.write('E1', 'CLIMA', bold)
                    hoja.write('F1', 'AÑO', bold)
                    hoja.write('G1', 'TIPO', bold)
                    hoja.write('H1', 'ESTELA', bold)
                    hoja.write('I1', 'DURACIÓN', bold)
                    hoja.write(fila, c, datos[f][c])
            fila += 1
        archivo.close()
        messagebox.showinfo('PROCESO EXITOSO', 'SE GUARDÓ CORRECTAMENTE EL ARCHIVO EN: ' + name)

# Función botón abrir pantalla de agregar más elementos 
def agregar():
    add = Toplevel(BDP)
    add.title('AGREGAR PERFUME')
    ancho_ventana = 800
    alto_ventana = 600
    #add.wm_iconbitmap(".ico")

    # Centra la ventana en la pantalla
    x_ventana = add.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = add.winfo_screenheight() // 2 - alto_ventana // 2

    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    add.geometry(posicion)
    add.resizable(0,0) # No se puede modificar el tamaño de la pantalla

    background_label = Label(add, image=filename).place(x=0, y=0, relwidth=1, relheight=1) # Imagen de fondo

    # Etiquetas y entrys de la ventana 'agregar'
    marca_label = Label(add, text="MARCA", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=40)
    nombre_label = Label(add, text="NOMBRE", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=90)
    marca_Combo = ttk.Combobox(add, font=fuente, height=170, width=24)
    marca_Combo.configure(values=consultar_marcas())
    marca_Combo.place(x=120, y=40)
    Nombre_Entry = StringVar()
    nombre_entry = Entry(add, width = "25", justify = "center", font = fuente ,textvariable = Nombre_Entry)
    nombre_entry.place(x=120, y=90)

    fam_label = Label(add, text="FAMILIA\nOLFATIVA", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=60, y=150)
    Fam_Entry = StringVar()
    fam_entry = Entry(add, width = "12", justify = "center", font = fuente ,textvariable = Fam_Entry)
    fam_entry.place(x=30, y=220)

    año_label = Label(add, text="AÑO", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=335, y=160)
    Año_Entry = IntVar()
    año_entry = Entry(add, width = "12", justify = "center", font = fuente ,textvariable = Año_Entry)
    año_entry.place(x=280, y=220)

    color_label = Label(add, text="COLOR", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=75, y=270)
    Color_Entry = StringVar()
    color_entry = Entry(add, width = "12", justify = "center", font = fuente ,textvariable = Color_Entry)
    color_entry.place(x=30, y=320)

    tipo_label = Label(add, text="GÉNERO", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=320, y=270)
    tipo_combo = ttk.Combobox(add, font=fuente, width=12)
    tipo_combo.configure(values=opciones_combobox(1), state="readonly", justify="center")
    tipo_combo.place(x=280, y=320)

    clima_label = Label(add, text="CLIMA", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=75, y=370)
    clima_combo = ttk.Combobox(add, font=fuente, width=12, state="readonly", justify="center")
    clima_combo.configure(values=opciones_combobox(2))
    clima_combo.place(x=30, y=420)

    duracion_label = Label(add, text="DURACIÓN", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=308, y=370)
    duracion_combo = ttk.Combobox(add, font=fuente, width=12, state="readonly", justify="center")
    duracion_combo.configure(values=opciones_combobox(3))
    duracion_combo.place(x=280, y=420)

    estela_label = Label(add, text="ESTELA", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=195, y=480)
    estela_combo = ttk.Combobox(add, font=fuente, width=12, state="readonly", justify="center")
    estela_combo.configure(values=opciones_combobox(4))
    estela_combo.place(x=155, y=530)
    
    ruta = []

    def selec_imagen():
        foto = filedialog.askopenfilename( 
            filetypes=[("image",".png"),
                       ("image",".jpg")]
            )
        ruta.append(foto)
        img = procesar_imagen(foto) # Pasamos la dirección de la imagen como argumento de la función
        imagen_label.configure(image=img, width=255, height=355)
        imagen_label.image = img

    imagen_boton = Button(add, text="Elegir Imagen", font=fuente, padx=5, pady=5, command=selec_imagen).place(x=565, y=120)
    imagen_label = Label(add, width=35, height=25)
    imagen_label.place(x=520, y=200)

    def subir():
        if all(x.isalpha() or x.isspace() for x in color_entry.get()):
            if all(x.isalpha() or x.isspace() for x in fam_entry.get()):
                if all(x.isalpha() or x.isspace() or (x == '/') or (x == '-') for x in clima_combo.get()):
                    if all(x.isalpha() or x.isspace() for x in tipo_combo.get()):
                        if all(x.isalpha() or x.isspace() for x in estela_combo.get()):
                            if all(x.isalpha() or x.isspace() for x in duracion_combo.get()):
                                if (año_entry.get()).isdigit():
                                    insertar_data(marca_Combo.get().upper(), nombre_entry.get().upper(), color_entry.get().upper(), fam_entry.get().upper(), clima_combo.get().upper(), año_entry.get().upper(), tipo_combo.get().upper(), converir_blob(ruta[0]), estela_combo.get().upper(), duracion_combo.get().upper())   
                                    ruta.clear()
                                    Marca_Barra.configure(values=consultar_marcas())
                                    realizar_respaldo()
                                    add.destroy()
                                    messagebox.showinfo('OPERACIÓN EXITOSA', 'SE AGREGÓ CORRECTAMENTE EL PERFUME.')
                                else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "AÑO" (SOLO NÚMEROS ENTEROS).')
                            else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "DURACIÓN".') 
                        else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "ESTELA".')
                    else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "GÉNERO".') 
                else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "CLIMA".')
            else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "FAMILIA OLFATIVA".')
        else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "COLOR".')

    agregar_boton = Button(add, text="AGREGAR", font=fuente, padx=5, pady=5, command=subir, fg="white", bg="green")
    agregar_boton.place(x=585, y=30)

# Función de ventana para actualizar datos
def actualizar():
    update = Toplevel(BDP)
    update.title('ACTUALIZAR PERFUME')
    ancho_ventana = 1100
    alto_ventana = 500
    #update.wm_iconbitmap(".ico")

    # Centra la ventana en la pantalla
    x_ventana = update.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = update.winfo_screenheight() // 2 - alto_ventana // 2

    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    update.geometry(posicion)
    update.resizable(0,0)
    background_label = Label(update, image=filename).place(x=0, y=0, relwidth=1, relheight=1)

    marca = Label(update, text="MARCA:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=30)
    Marca_Entry = StringVar()
    marca_bd = Entry(update, width = "25", justify = "center", font = fuente, textvariable = Marca_Entry)
    marca_bd.place(x=130, y=30)

    nombre = Label(update, text="NOMBRE:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=80)
    Nombre_Entry = StringVar()
    nombre_bd = Entry(update, width = "40", justify = "center", font = fuente, textvariable = Nombre_Entry)
    nombre_bd.place(x=130, y=80)

    fam = Label(update, text="FAMILIA OLFATIVA:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=130)
    Fam_Entry = StringVar()
    fam_bd = Entry(update, width = "25", justify = "center", font = fuente, textvariable = Fam_Entry)
    fam_bd.place(x=240, y=130)

    año = Label(update, text="AÑO:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=180)
    Año_Entry = IntVar()
    año_bd = Entry(update, width = "25", justify = "center", font = fuente, textvariable = Año_Entry)
    año_bd.place(x=90, y=180)

    color = Label(update, text="COLOR:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=230)
    Color_Entry= StringVar()
    color_bd = Entry(update, width = "25", justify = "center", font = fuente, textvariable = Color_Entry)
    color_bd.place(x=120, y=230)

    tipo = Label(update, text="GÉNERO:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=280)
    tipo_bd = ttk.Combobox(update, font=fuente, width=25)
    tipo_bd.configure(values=opciones_combobox(1), state="readonly", justify="center")
    tipo_bd.place(x=120, y=280)

    clima = Label(update, text="CLIMA:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=330)
    clima_bd = ttk.Combobox(update, font=fuente, width=25)
    clima_bd.configure(values=opciones_combobox(2), state="readonly", justify="center")
    clima_bd.place(x=120, y=330)

    duracion = Label(update, text="DURACIÓN:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=380)
    duracion_bd = ttk.Combobox(update, font=fuente, width=25)
    duracion_bd.configure(values=opciones_combobox(3), state="readonly", justify="center")
    duracion_bd.place(x=150, y=380)

    estela = Label(update, text="ESTELA:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=430)
    estela_bd = ttk.Combobox(update, font=fuente, width=25)
    estela_bd.configure(values=opciones_combobox(4), state="readonly", justify="center")
    estela_bd.place(x=120, y=430)

    global imagen_etiqueta
    imagen_etiqueta = Label(update, width=35, height=25)
    imagen_etiqueta.place(x=780, y=100)

    # Obtenemos los datos de la base de datos según lo ingresado en los Combobox
    datos = consulta_data(Marca_Barra.get(), Nombre_Barra.get())
    try:
        marca_bd.insert(0, datos[0][0])
        nombre_bd.insert(0, datos[0][1])
        color_bd.insert(0, datos[0][2])
        fam_bd.insert(0, datos[0][3])
        clima_bd.set(datos[0][4])
        Año_Entry.set(datos[0][5])
        tipo_bd.set(datos[0][6])
        select_imagen = datos[0][7]
        estela_bd.set(datos[0][8])
        duracion_bd.set(datos[0][9])

        temp = '{}_BD.png'.format(datos[0][1])

        with open(temp, 'wb') as f:
            f.write(datos[0][7])

        IMG2 = procesar_imagen(temp)

        imagen_etiqueta.configure(image=IMG2, width=255, height=355)
        imagen_etiqueta.image = IMG2

        if os.path.exists(temp): os.remove(temp)
    except IndexError:
        messagebox.showerror(title="ERROR", message="Seleccione el perfume que desea actualizar.")
        update.destroy()

    ruta = []

    def cambio_imagen():
        if len(ruta) == 0: return False
        else: return True

    def selec_imagen():
        foto = filedialog.askopenfilename( 
            filetypes=[("image",".png"),
                       ("image",".jpg")]
            )
        
        ruta.append(foto)

        if len(foto) > 0:
            img = procesar_imagen(foto)

            imagen_etiqueta.configure(image=img, width=255, height=355)
            imagen_etiqueta.image = img

    imagen_boton = Button(update, text="Elegir Imagen", font=fuente, padx=5, pady=5, bg="orange", fg="white", command=selec_imagen)
    imagen_boton.bind("<<Button-1>>", cambio_imagen)
    imagen_boton.place(x=750, y=30)

    def Actualizar():
        if all(x.isalpha() or x.isspace() for x in color_bd.get()):
            if all(x.isalpha() or x.isspace() for x in fam_bd.get()):
                if all(x.isalpha() or x.isspace() or (x == '/') or (x == '-') for x in clima_bd.get()):
                    if all(x.isalpha() or x.isspace() for x in tipo_bd.get()):
                        if all(x.isalpha() or x.isspace() for x in estela_bd.get()):
                            if all(x.isalpha() or x.isspace() for x in duracion_bd.get()):
                                if (año_bd.get()).isdigit():
                                    imagen = cambio_imagen()
                                    if imagen:
                                        actualizar_data_completa(marca_bd.get().upper(), nombre_bd.get().upper(), color_bd.get().upper(), fam_bd.get().upper(), clima_bd.get().upper(), año_bd.get().upper(), tipo_bd.get().upper(), converir_blob(ruta[0]), estela_bd.get().upper(), duracion_bd.get().upper(), Nombre_Barra.get())
                                        Marca_Barra.configure(values=consultar_marcas())
                                        ruta.clear()
                                        update.destroy()
                                        imagen = False
                                        messagebox.showinfo('OPERACIÓN EXITOSA', 'SE AGREGÓ CORRECTAMENTE EL PERFUME.')
                                    else: 
                                        actualizar_data_sin_foto(marca_bd.get().upper(), nombre_bd.get().upper(), color_bd.get().upper(), fam_bd.get().upper(), clima_bd.get().upper(), año_bd.get().upper(), tipo_bd.get().upper(), estela_bd.get().upper(), duracion_bd.get().upper(), Nombre_Barra.get())
                                        Marca_Barra.configure(values=consultar_marcas())
                                        imagen = False
                                        update.destroy()
                                        messagebox.showinfo('OPERACIÓN EXITOSA', 'SE AGREGÓ CORRECTAMENTE EL PERFUME.')
                                else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "AÑO" (SOLO NÚMEROS ENTEROS).')
                            else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "DURACIÓN".') 
                        else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "ESTELA".')
                    else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "GÉNERO".') 
                else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "CLIMA".')
            else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "FAMILIA OLFATIVA".')
        else: messagebox.showerror('ERROR', 'VALOR INVÁLIDO EN EL CAMPO "COLOR".')

    actualizar_boton = Button(update, text="ACTUALIZAR", font=fuente, padx=5, pady=5, bg="green", fg="white", command=Actualizar).place(x=930, y=30)

# Función de ventana para eliminar unelemento de la base
def eliminar():
    delete = Toplevel(BDP)
    delete.title('BORRAR PERFUME')
    ancho_ventana = 400
    alto_ventana = 250
    #delete.wm_iconbitmap(".ico")

    # Centra la ventana en la pantalla
    x_ventana = delete.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = delete.winfo_screenheight() // 2 - alto_ventana // 2

    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    delete.geometry(posicion)
    delete.resizable(0,0)
    background_label = Label(delete, image=filename).place(x=0, y=0, relwidth=1, relheight=1)

    def Eliminar():
        if len(nombres.get()) > 0:
            eliminar_data(nombres.get())
            Marca_Barra.configure(values=consultar_marcas())
            delete.destroy()
            messagebox.showinfo('PROCESO EXITOSO', 'El Perfume se ELIMINÓ CORRECTAMENTE.')
        else: messagebox.showerror('ERROR', 'DEBE SELECCIONAR UN PERFUME.')
        
    Nombres = consulta_nombres()

    instruccion = Label(delete, text="Seleccione el Perfume a ELIMINAR:", font=fuente, bg='black', fg='white', padx=5, pady=5)
    instruccion.pack(pady=30)
    nombres = ttk.Combobox(delete, font=Font(family="Gill Sans Ultra Bold", size=8), height=10, width=40, values=Nombres, state="readonly")
    nombres.pack(ipady=8)
    borrar = Button(delete, text="ELIMINAR", font=Font(family="Gill Sans Ultra Bold", size=16), background='red', foreground='white', padx=5, pady=5, command=Eliminar)
    borrar.pack(pady=40)

# Función de ventana de consulta de la base de datos
def buscar():
    info = Toplevel(BDP)
    info.title('INFORMACIÓN PERFUME')
    info.geometry("800x500+30+310") # ancho x largo + x(posición de izquierda a derecha) + y(posicion de arriba a abajo)
    info.resizable(0,0)
    #info.wm_iconbitmap(".ico")
    background_label = Label(info, image=filename).place(x=0, y=0, relwidth=1, relheight=1)

    marca = Label(info, text="MARCA:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=30)
    marca_bd = Label(info, text="", font=fuente, bg='white', fg='black', padx=5, pady=5)
    marca_bd.place(x=130, y=30)
    nombre = Label(info, text="NOMBRE:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=80)
    nombre_bd = Label(info, text="", font=fuente, bg='white', fg='black', padx=5, pady=5)
    nombre_bd.place(x=130, y=80)
    fam = Label(info, text="FAMILIA OLFATIVA:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=130)
    fam_bd = Label(info, text="", font=fuente, bg='white', fg='black', padx=5, pady=5)
    fam_bd.place(x=240, y=130)
    año = Label(info, text="AÑO:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=180)
    año_bd = Label(info, text="", font=fuente, bg='white', fg='black', padx=5, pady=5)
    año_bd.place(x=90, y=180)
    color = Label(info, text="COLOR:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=230)
    color_bd = Label(info, text="", font=fuente, bg='white', fg='black', padx=5, pady=5)
    color_bd.place(x=120, y=230)
    tipo = Label(info, text="GÉNERO:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=280)
    tipo_bd = Label(info, text="", font=fuente, bg='white', fg='black', padx=5, pady=5)
    tipo_bd.place(x=120, y=280)
    clima = Label(info, text="CLIMA:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=330)
    clima_bd = Label(info, text="", font=fuente, bg='white', fg='black', padx=5, pady=5)
    clima_bd.place(x=120, y=330)
    duracion = Label(info, text="DURACIÓN:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=380)
    duracion_bd = Label(info, text="", font=fuente, bg='white', fg='black', padx=5, pady=5)
    duracion_bd.place(x=150, y=380)
    estela = Label(info, text="ESTELA:", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=10, y=430)
    estela_bd = Label(info, text="", font=fuente, bg='white', fg='black', padx=5, pady=5)
    estela_bd.place(x=120, y=430)

    if len(Marca_Barra.get()) > 0 and len(Nombre_Barra.get()) > 0:
        # Obtenemos los datos de la base de datos según lo ingresado en los Combobox
        datos = consulta_data(Marca_Barra.get(), Nombre_Barra.get())
    else: datos = consulta_data(nombre=Resultados_Barra.get())

    try:
        marca_bd.configure(text=datos[0][0])
        nombre_bd.configure(text=datos[0][1])
        color_bd.configure(text=datos[0][2])
        fam_bd.configure(text=datos[0][3])
        clima_bd.configure(text=datos[0][4])
        año_bd.configure(text=datos[0][5])
        tipo_bd.configure(text=datos[0][6])
        estela_bd.configure(text=datos[0][8])
        duracion_bd.configure(text=datos[0][9])

        temp = '{}_BD.png'.format(datos[0][1])

        with open(temp, 'wb') as f:
            f.write(datos[0][7])

        # Función de segunda ventana con la imagen
        def pantallafoto():
            foto = Toplevel(BDP)
            foto.title('IMAGEN PERFUME')
            foto.geometry("600x700+900+100")
            foto.resizable(0,0)
            background_label = Label(foto)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

            IMG = procesar_imagen(temp)

            background_label.configure(image=IMG, width=255, height=355)
            background_label.image = IMG

            def cerrar():
                foto.destroy()
                info.destroy()

            info.protocol("WM_DELETE_WINDOW", cerrar)
            foto.protocol("WM_DELETE_WINDOW", cerrar)

        pantallafoto()

        if os.path.exists(temp): os.remove(temp)
    except IndexError:
        info.destroy()
        messagebox.showerror(title="ERROR", message="No se encontró el Perfume en la Base.")

# Despliega la ayuda del uso de la aplicación
def ayuda():
    help = Toplevel(BDP)
    help.title('AYUDA DE USO')
    x_ventana = help.winfo_screenwidth() // 2 - 1100 // 2
    y_ventana = help.winfo_screenheight() // 2 - 300 // 2
    help.geometry("1100x300+{}+{}".format(x_ventana, y_ventana)) # ancho x largo + x(posición de izquierda a derecha) + y(posicion de arriba a abajo)
    help.resizable(0,0)
    #info.wm_iconbitmap(".ico")
    background_label = Label(help, image=filename).place(x=0, y=0, relwidth=1, relheight=1)

    def A_Excel():
        help.destroy()
        a_excel = Toplevel(BDP)
        a_excel.title("AYUDA BOTÓN EXCEL")
        x_ventana = a_excel.winfo_screenwidth() // 2 - 600 // 2
        y_ventana = a_excel.winfo_screenheight() // 2 - 600 // 2
        a_excel.geometry("600x600+{}+{}".format(x_ventana, y_ventana)) # ancho x largo + x(posición de izquierda a derecha) + y(posicion de arriba a abajo)
        a_excel.resizable(0,0)
        #info.wm_iconbitmap(".ico")

        def Btn_Volver():
            a_excel.destroy()
            ayuda()

        background_label = Label(a_excel, image=filename).place(x=0, y=0, relwidth=1, relheight=1)
        imagen = Label(a_excel, image=excel_png).pack(pady=50)
        informacion = Label(a_excel, text="Al apretar el botón de Excel, se abrirá una\n ventana de guardado en donde se indicará\n el nombre y el lugar de donde se guardará\nel archivo de excel en donde se exportará\n la base de datos completa.\n\nSi el proceso fue éxitoso se mostrará una\n pequeña ventana de confirmación.\n\nDe lo contrario se notificará la cancelación del \nproceso.", bg='black', fg='white', font=fuente_cuerpo).pack(pady=20)
        volver_btn = Button(a_excel, text="VOLVER", font=fuente_titulo, command=Btn_Volver, padx=5, pady=8).pack(pady=15)
    
    def A_Agregar():
        help.destroy()
        a_agregar = Toplevel(BDP)
        a_agregar.title("AYUDA BOTÓN AGREGAR")
        x_ventana = a_agregar.winfo_screenwidth() // 2 - 900 // 2
        y_ventana = a_agregar.winfo_screenheight() // 2 - 700 // 2
        a_agregar.geometry("900x700+{}+{}".format(x_ventana, y_ventana)) # ancho x largo + x(posición de izquierda a derecha) + y(posicion de arriba a abajo)
        a_agregar.resizable(0,0)
        #info.wm_iconbitmap(".ico")

        def Btn_Volver():
            a_agregar.destroy()
            ayuda()

        background_label = Label(a_agregar, image=filename).place(x=0, y=0, relwidth=1, relheight=1)
        imagen = Label(a_agregar, image=agregar_png).pack(pady=50)
        informacion = Label(a_agregar, text="Al presionar el botón de Agregar, se abrirá una ventana de registro \ndonde se encuentran 10 opciones. \n\nMARCA: En esta sección se puede o bien agregar el nombre de una marca ya \nregistrada o ingresar una nueva marca. \n\nHay 4 secciones (GÉNERO, CLIMA, DURACIÓN y ESTELA) en las que las opciones \nson limitadas, en las demás secciones se tiene libertad de elegir una opción fuera \nde los parámetros, excepto en la sección AÑO, en la cual se deben \ningresar únicamente números enteros. \n\nEn la sección ELEGIR IMAGEN, al presionar el botón se abrirá una ventana \nde búsqueda de archivos para que se pueda seleccionar una imagen que se pueda \nsubir a la base, deben ser formatos .jpg o .png. \n\nAl llenar todos los campos se presiona el botón AGREGAR y si el proceso \nfue exitoso saldrá una pequeña ventana de confimación. \nNOTA: Todos los datos se subirán en mayúsculas sin importar cómo fueron ingresados.",  bg='black', fg='white', font=fuente_cuerpo).pack(pady=10)
        volver_btn = Button(a_agregar, text="VOLVER", font=fuente_titulo, command=Btn_Volver, padx=5, pady=8).pack(pady=15)

    def A_Actualizar():
        help.destroy()
        a_actualizar = Toplevel(BDP)
        a_actualizar.title("AYUDA BOTÓN ACTUALIZAR")
        x_ventana = a_actualizar.winfo_screenwidth() // 2 - 900 // 2
        y_ventana = a_actualizar.winfo_screenheight() // 2 - 600 // 2
        a_actualizar.geometry("900x600+{}+{}".format(x_ventana, y_ventana)) # ancho x largo + x(posición de izquierda a derecha) + y(posicion de arriba a abajo)
        a_actualizar.resizable(0,0)
        #info.wm_iconbitmap(".ico")

        def Btn_Volver():
            a_actualizar.destroy()
            ayuda()

        background_label = Label(a_actualizar, image=filename).place(x=0, y=0, relwidth=1, relheight=1)
        imagen = Label(a_actualizar, image=actualizar_png).pack(pady=50)
        informacion = Label(a_actualizar, text="Antes de presionar el botón se debe seleccionar la marca \ny el perfume que se quiere actualizar. \n\nDespués de seleccionar estos datos y presionar el botón, podrá modificar \ntodos los datos que quiera, incluyendo la imagen. \n\nAl finalizar debe presionar el botón de ACTUALIZAR. \n\nSi el proceso fue éxitoso se mostrará una pequeña ventana de confirmación. \n\nNOTA: Todos los datos se subirán en mayúsculas sin importar como fueron ingresados.",  bg='black', fg='white', font=fuente_cuerpo).pack(pady=20)
        volver_btn = Button(a_actualizar, text="VOLVER", font=fuente_titulo, command=Btn_Volver, padx=5, pady=8).pack(pady=15)

    def A_Eliminar():
        help.destroy()
        a_eliminar = Toplevel(BDP)
        a_eliminar.title("AYUDA BOTÓN ELIMINAR")
        x_ventana = a_eliminar.winfo_screenwidth() // 2 - 600 // 2
        y_ventana = a_eliminar.winfo_screenheight() // 2 - 600 // 2
        a_eliminar.geometry("600x600+{}+{}".format(x_ventana, y_ventana)) # ancho x largo + x(posición de izquierda a derecha) + y(posicion de arriba a abajo)
        a_eliminar.resizable(0,0)
        #info.wm_iconbitmap(".ico")

        def Btn_Volver():
            a_eliminar.destroy()
            ayuda()

        background_label = Label(a_eliminar, image=filename).place(x=0, y=0, relwidth=1, relheight=1)
        imagen = Label(a_eliminar, image=eliminar_png).pack(pady=50)
        informacion = Label(a_eliminar, text="Después de presionar el botón se mostrará un combobox\n con todos los perfumes que hay en la base, \nseleccione el que desea eliminar y \noprima el botón de ELIMINAR. \n\nSi el proceso fue éxitoso se mostrará una \npequeña ventana de confirmación. \n\nNOTA: Todos los datos se subirán en mayúsculas \nsin importar como fueron ingresados.",  bg='black', fg='white', font=fuente_cuerpo).pack(pady=20)
        volver_btn = Button(a_eliminar, text="VOLVER", font=fuente_titulo, command=Btn_Volver, padx=5, pady=8).pack(pady=15)

    def A_Buscar():
        help.destroy()
        a_buscar = Toplevel(BDP)
        a_buscar.title("AYUDA BOTÓN BUSCAR")
        x_ventana = a_buscar.winfo_screenwidth() // 2 - 600 // 2
        y_ventana = a_buscar.winfo_screenheight() // 2 - 700 // 2
        a_buscar.geometry("600x700+{}+{}".format(x_ventana, y_ventana)) # ancho x largo + x(posición de izquierda a derecha) + y(posicion de arriba a abajo)
        a_buscar.resizable(0,0)
        #info.wm_iconbitmap(".ico")

        def Btn_Volver():
            a_buscar.destroy()
            ayuda()

        background_label = Label(a_buscar, image=filename).place(x=0, y=0, relwidth=1, relheight=1)
        imagen = Label(a_buscar, image=buscar_png).pack(pady=50)
        informacion = Label(a_buscar, text="Para utilizar este botón se debe seleccionar o bien \nla MARCA y el NOMBRE del perfume o \nhacer uso de la sección FILTRAR ya que \nestas dos secciones funcionan con este mismo botón. \n\nUna vez se haya usado alguna de las dos secciones \n(es importante que solo sea una de las \ndos y no ambas al mismo tiempo) \nse puede usar el botón de BUSCAR y este \nabrirá dos ventanas. \n\nUna con la información del perfume y \nla otra con la imagen del mismo. \n\nDe no haber seleccionado ninguna de las dos secciones, \nse mostrará una pequeña ventana de error en la que \nse notificará que no se encontró el perfume.",  bg='black', fg='white', font=fuente_cuerpo).pack(pady=20)
        volver_btn = Button(a_buscar, text="VOLVER", font=fuente_titulo, command=Btn_Volver, padx=5, pady=8).pack(pady=15)

    def A_Filtro():
        help.destroy()
        a_filtro = Toplevel(BDP)
        a_filtro.title("AYUDA SECCIÓN FILTRAR")
        x_ventana = a_filtro.winfo_screenwidth() // 2 - 600 // 2
        y_ventana = a_filtro.winfo_screenheight() // 2 - 700 // 2
        a_filtro.geometry("600x700+{}+{}".format(x_ventana, y_ventana)) # ancho x largo + x(posición de izquierda a derecha) + y(posicion de arriba a abajo)
        a_filtro.resizable(0,0)
        #info.wm_iconbitmap(".ico")

        def Btn_Volver():
            a_filtro.destroy()
            ayuda()

        background_label = Label(a_filtro, image=filename).place(x=0, y=0, relwidth=1, relheight=1)
        imagen = Label(a_filtro, text="FILTRAR", bg='black', fg='white', font=fuente_titulo).pack(pady=50)
        informacion = Label(a_filtro, text="Para utilizar la sección de FILTRAR primero debe \nasegurarse de que no tenga ningún contenido los \ncombobox de MARCA y NOMBRE \n(esto se puede asegurar con el botón de LIMPIAR).\n\nPosteriormente puede hacer la selección primero \nen el combobox de CARACTERISTICAS, en el cual se \nencuentran todos los filtros que hay para \nlos perfumes, seleccionara después en el combobox\nde OPCIONES el tipo de filtro que busca y \npor último tendrá todos los perfumes que coincidan con \nlas especificaciones dadas anteriormente, seleccione \nel que desea ver y oprima el botón de BUSCAR.",  bg='black', fg='white', font=fuente_cuerpo).pack(pady=20)
        volver_btn = Button(a_filtro, text="VOLVER", font=fuente_titulo, command=Btn_Volver, padx=5, pady=8).pack(pady=15)

    def A_Limpiar():
        help.destroy()
        a_limpiar = Toplevel(BDP)
        a_limpiar.title("AYUDA BOTÓN LIMPIAR")
        x_ventana = a_limpiar.winfo_screenwidth() // 2 - 600 // 2
        y_ventana = a_limpiar.winfo_screenheight() // 2 - 500 // 2
        a_limpiar.geometry("600x500+{}+{}".format(x_ventana, y_ventana)) # ancho x largo + x(posición de izquierda a derecha) + y(posicion de arriba a abajo)
        a_limpiar.resizable(0,0)
        #info.wm_iconbitmap(".ico")

        def Btn_Volver():
            a_limpiar.destroy()
            ayuda()

        background_label = Label(a_limpiar, image=filename).place(x=0, y=0, relwidth=1, relheight=1)
        imagen = Label(a_limpiar, image=limpiar_png).pack(pady=50)
        informacion = Label(a_limpiar, text="La función que tiene este botón es de borrar los \ncampos seleccionados en los combobox MARCAS y \nNOMBRES, al igual que en la \nsección de FILTRAR.",  bg='black', fg='white', font=fuente_cuerpo).pack(pady=20)
        volver_btn = Button(a_limpiar, text="VOLVER", font=fuente_titulo, command=Btn_Volver, padx=5, pady=8).pack(pady=15)
    
    titulo1 = Label(help, text="SELECCIONE EN QUÉ SECCIÓN NECESITA AYUDA", font=fuente_titulo, fg='white', bg='black').pack(pady=50)
    ayuda_excel = Button(help, text="EXCEL", font=fuente_titulo, command=A_Excel).place(x=20, y=140)
    ayuda_agregar = Button(help, text="AGREGAR", font=fuente_titulo, command=A_Agregar).place(x=140, y=140)
    ayuda_actualizar = Button(help, text="ACTUALIZAR", font=fuente_titulo, command=A_Actualizar).place(x=310, y=140)
    ayuda_eliminar = Button(help, text="ELIMINAR", font=fuente_titulo, command=A_Eliminar).place(x=510, y=140)
    ayuda_buscar = Button(help, text="BUSCAR", font=fuente_titulo, command=A_Buscar).place(x=670, y=140)
    ayuda_filtro = Button(help, text="FILTRAR", font=fuente_titulo, command=A_Filtro).place(x=810, y=140)
    ayuda_limpiar = Button(help, text="LIMPIAR", font=fuente_titulo, command=A_Limpiar).place(x=960, y=140)

# Limpia los campos de la ventana principal
def limpiar():
    Marca_Barra.set("")
    Nombre_Barra.set("")
    Caracteristicas_Barra.set("")
    Opciones_Barra.set("")
    Resultados_Barra.set("")

"ELEMENTOS DE LA INTERFAZ"

Barra = Frame(BDP, width=1700, height=40, background="black")
Barra.pack_propagate(False)
Barra.pack()

hora_label = Label(Barra, fg="white", background="black", font=fuente)
hora_label.pack(side="left")

fecha = Label(Barra, text=FECHA(), fg="white", background="black" ,font=Font(family="Gill Sans Ultra Bold", size=16)).place(x=640, y=5)
HORA()

tache = PhotoImage(file='Imagenes y Logos/Tache.png')
Tache = Button(Barra, image=tache, width=40, height=40, command=salir).pack(side="right")

min = PhotoImage(file='Imagenes y Logos/Minimizar.png')
Min = Button(Barra, image=min, width=40, height=40, command=minimizar).pack(side='right')

Marca = Label(BDP, text="MARCA", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=30, y=75)

Nombre = Label(BDP, text="NOMBRE", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=30, y=155)

Filtro = Label(BDP, text="FILTRAR", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=1140, y=50)
Caracteristicas = Label(BDP, text="CARACTERÍSTICAS", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=870, y=95)
Opciones = Label(BDP, text="OPCIONES", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=1260, y=95)
Resultados = Label(BDP, text="RESULTADOS", font=fuente, bg='black', fg="white", padx=5, pady=5).place(x=870, y=180)

Perfumes = Label(BDP, text=f"Perfumes: {numero_perfumes()}", font=fuente_titulogrande, bg='black', fg='white', padx=5, pady=5).pack(side="bottom") 

"ASIGNACIÓN DE VALORES PARA LOS COMBOBOX"

# Muestra la lista de nombres según la marca ingresada
def Consultar_Nombres(event):
    Nombre_Barra.configure(values=consultar_nombres(Marca_Barra.get())) # Las opciones de nombres con la marca seleccionada

# Muestra la lista de algunas de las opciones que tienen en el combobox de "Opciones_Barra"
def Consulta_Opciones(event):
    if Caracteristicas_Barra.get() == "GÉNERO": Opciones_Barra.configure(values=opciones_combobox(1))
    elif Caracteristicas_Barra.get() == "CLIMA": Opciones_Barra.configure(values=opciones_combobox(2))
    elif Caracteristicas_Barra.get() == "DURACIÓN": Opciones_Barra.configure(values=opciones_combobox(3))
    elif Caracteristicas_Barra.get() == "ESTELA": Opciones_Barra.configure(values=opciones_combobox(4))
    elif Caracteristicas_Barra.get() == "FAMILIA OLFATIVA": Opciones_Barra.configure(values=opciones_combobox(6))
    elif Caracteristicas_Barra.get() == "AÑO": Opciones_Barra.configure(values=opciones_combobox(7))
    elif Caracteristicas_Barra.get() == "COLOR": Opciones_Barra.configure(values=opciones_combobox(8))

# Muestra la lista de elementos de la tabla que coinciden con lo seleccionado en "Características_Barra"
def Consulta_Filtro(event):
    Resultados_Barra.configure(values=consulta_por_caracteristicas(Caracteristicas_Barra.get(), Opciones_Barra.get()))

Marca_Barra = ttk.Combobox(font=fuente, height=170, width=40, state="readonly")
Marca_Barra.configure(values=consultar_marcas()) # Las opciones de marcas disponibles de marcas en tiempo real
Marca_Barra.bind("<<ComboboxSelected>>", Consultar_Nombres) # Evento que detecta la selección en el Combobox
Marca_Barra.place(x=180, y=80)

Nombre_Barra = ttk.Combobox(font=fuente, height=180, width=40, state="readonly")
Nombre_Barra.place(x=180, y=160)

Caracteristicas_Barra = ttk.Combobox(font=fuente, height=180, width=16, state="readonly")
Caracteristicas_Barra.configure(values=opciones_combobox(5))
Caracteristicas_Barra.bind("<<ComboboxSelected>>", Consulta_Opciones)
Caracteristicas_Barra.place(x=870, y=140)

Opciones_Barra = ttk.Combobox(font=fuente, height=180, width=16, state="readonly")
Opciones_Barra.bind("<<ComboboxSelected>>", Consulta_Filtro)
Opciones_Barra.place(x=1260, y=140)

Resultados_Barra = ttk.Combobox(font=fuente, height=180, width=44, state="readonly")
Resultados_Barra.place(x=870, y=230)

excel_png = PhotoImage(file='Imagenes y Logos/Excel.png')
Excel = Button(BDP, image=excel_png, command=excel).place(x=40, y=210)
agregar_png = PhotoImage(file='Imagenes y Logos/Agregar.png')
Agregar = Button(BDP, image=agregar_png, command=agregar).place(x=180, y=210)
actualizar_png = PhotoImage(file='Imagenes y Logos/Actualizar.png')
Actualizar = Button(BDP, image=actualizar_png, command=actualizar).place(x=340, y=210)
eliminar_png = PhotoImage(file='Imagenes y Logos/Eliminar.png')
Eliminar = Button(BDP, image=eliminar_png, command=eliminar).place(x=520, y=210)
buscar_png = PhotoImage(file='Imagenes y Logos/Buscar.png')
Buscar = Button(BDP, image=buscar_png, command=buscar).place(x=677, y=210)
ayuda_png = PhotoImage(file="Imagenes y Logos/Ayuda.png")
Ayuda = Button(BDP, image=ayuda_png, command=ayuda).place(x=10, y=750)
limpiar_png = PhotoImage(file="Imagenes y Logos/Limpiar.png")
Limpiar = Button(BDP, image=limpiar_png, command=limpiar).place(x=1425, y=750)

BDP.mainloop()