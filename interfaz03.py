from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk


from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import numpy as np
from playsound import playsound 

faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
fgbg=0
kernel=0

def video_de_entrada():
    global cap
    global fgbg
    global kernel
    if selected.get() == 1:
        path_video = filedialog.askopenfilename(filetypes = [
            ("all video format", ".mp4"),
            ("all video format", ".avi")])
        if len(path_video) > 0:
            btnEnd.configure(state="active")
            rad1.configure(state="disabled")
            rad2.configure(state="disabled")

            pathInputVideo = "..." + path_video[-20:]
            lblInfoVideoPath.configure(text=pathInputVideo)
            cap = cv2.VideoCapture(path_video)
            visualizar()
    if selected.get() == 2:
        btnEnd.configure(state="active")
        rad1.configure(state="disabled")
        rad2.configure(state="disabled")
        lblInfoVideoPath.configure(text="")
        cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
        ##cap = cv2.VideoCapture(0)
        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        detectMove()

def visualizar():
    global cap
    ret, frame = cap.read()
    if ret == True:
        frame = imutils.resize(frame, width=640)
        frame = deteccion_facilal(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, visualizar)
    else:
        lblVideo.image = ""
        lblInfoVideoPath.configure(text="")
        rad1.configure(state="active")
        rad2.configure(state="active")
        selected.set(0)
        btnEnd.configure(state="disabled")
        cap.release()
##Captar Movimiento
def detectMove():
    global cap
    global fgbg
    global kernel
    #cap = cv2.VideoCapture(0)
    #fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

    ret, frame = cap.read()
    if ret == True:
        ##ret, frame = cap.read()
        #if ret == False: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Dibujamos un rectángulo en frame, para señalar el estado
        # del área en análisis (movimiento detectado o no detectado)
        cv2.rectangle(frame,(0,0),(frame.shape[1],40),(0,0,0),-1)
        color = (0, 255, 0)
        texto_estado = "Estado: No se ha detectado movimiento"
        # Especificamos los puntos extremos del área a analizar
        area_pts = np.array([[0,40], [frame.shape[1],40], [frame.shape[1],frame.shape[0]], [0,frame.shape[0]]])
        
        # Con ayuda de una imagen auxiliar, determinamos el área
        # sobre la cual actuará el detector de movimiento
        imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
        imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
        image_area = cv2.bitwise_and(gray, gray, mask=imAux)
        # Obtendremos la imagen binaria donde la región en blanco representa
        # la existencia de movimiento
        fgmask = fgbg.apply(image_area)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.dilate(fgmask, None, iterations=2)
        # Encontramos los contornos presentes en fgmask, para luego basándonos
        # en su área poder determina si existe movimiento
        cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        for cnt in cnts:
            if cv2.contourArea(cnt) > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0), 2)
                texto_estado = "Estado: Alerta Movimiento Detectado!"
                playsound("E:/fiuna2_2021/lpv/Tema5/graciosos-alarma-es-tu-mujer-.mp3")
                color = (0, 0, 255) 
        # Visuzalizamos el alrededor del área que vamos a analizar
        # y el estado de la detección de movimiento        
        cv2.drawContours(frame, [area_pts], -1, color, 2)
        cv2.putText(frame, texto_estado , (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color,2)
        #cv2.imshow('fgmask', fgmask)
        #cv2.imshow("frame", frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, detectMove)
        #k = cv2.waitKey(2) & 0xFF
        #if k == 27:
            #break
    else:
        lblVideo.image = ""
        lblInfoVideoPath.configure(text="")
        rad1.configure(state="active")
        rad2.configure(state="active")
        selected.set(0)
        btnEnd.configure(state="disabled")
        cap.release()
    
def deteccion_facilal(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame

def finalizar_limpiar():
    lblVideo.image = ""
    lblInfoVideoPath.configure(text="")
    rad1.configure(state="active")
    rad2.configure(state="active")
    selected.set(0)
    cap.release()

###Clases Menu
def salirAplicacion():
    valor = messagebox.askquestion("Salir","Esta seguro que desea salir de la Aplicacion?")
    if valor == "yes":
        root.destroy()#sirve para cerrar las ventanas
        pass
def mensaje():
    acerca = '''Aplicacion: Trabajo de LPV \n
                Integrantes:\n
                -Christian Gomez\n
                Tutores:
                -Isaura Flores\n
                -Rodney Rojas\n
                '''
    messagebox.showinfo(title="INFORMACION", message= acerca)


cap = None
root = Tk(className='Tema 5')
#root.geometry("640x500")

lblInfo1 = Label(root, text="VIDEO DE ENTRADA", font="bold")
lblInfo1.grid(column=0, row=0, columnspan=2)

selected = IntVar()
rad1 = Radiobutton(root, text="Elegir video", width=20, value=1, variable=selected, command=video_de_entrada)
rad2 = Radiobutton(root, text="Video en directo", width=20, value=2, variable=selected, command=video_de_entrada)
rad1.grid(column=0, row=1)
rad2.grid(column=1, row=1)

lblInfoVideoPath = Label(root, text="", width=20)
lblInfoVideoPath.grid(column=0, row=2)
lblVideo = Label(root)
lblVideo.grid(column=0, row=3, columnspan=2)
btnEnd = Button(root, text="Finalizar visualización y limpiar", state="disabled", command=finalizar_limpiar)
btnEnd.grid(column=0, row=4, columnspan=2, pady=10)

####Crear los menus####
menubar= Menu(root)
menubasedat= Menu(menubar, tearoff=0)
menubasedat.add_command(label= "Salir", command= salirAplicacion)
menubar.add_cascade(label="Inicio", menu= menubasedat)
ayudamenu= Menu(menubar, tearoff= 0)
ayudamenu.add_command(label= "Acerca", command= mensaje)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

root.config(menu=menubar)
root.mainloop()



