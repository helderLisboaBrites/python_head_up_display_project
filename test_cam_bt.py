import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from lxml import *
from xml.dom import minidom
from threading import Thread
from bluetooth import *
import RPi.GPIO as GPIO


canvasDimWidth = 350
canvasDimHeight = 250
class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.initGPIO()
        self.dicoDirection = { "attente" : PIL.ImageTk.PhotoImage(PIL.Image.open("attente.png")) ,  "droite" : PIL.ImageTk.PhotoImage(PIL.Image.open("droite.png")) , "gauche" : PIL.ImageTk.PhotoImage(PIL.Image.open("gauche.png").resize((150,150),PIL.Image.ANTIALIAS)) , "tout_droit" : PIL.ImageTk.PhotoImage(PIL.Image.open("tout_droit.png")) , "demi_tour" : PIL.ImageTk.PhotoImage(PIL.Image.open("demi_tour.png")) , "arrive" : PIL.ImageTk.PhotoImage(PIL.Image.open("arrive.png"))}
        self.cameraOn = True
        global canvasDimWidth 
        global canvasDimHeight 



        #img3 = PIL.ImageTk.PhotoImage(PIL.Image.open(listDirections[0])) #resize((50,50), PIL.Image.ANTIALIAS)

        frame_Canvas = tkinter.Frame(window, bg="black")
        frame_Direction = tkinter.Frame(window, bg="black")#, width = 50, height = 50
        frame_Heure = tkinter.Frame(window, bg = "black")
        frame_TempsRestant = tkinter.Frame(window, bg = "black")
        frame_KmRestant = tkinter.Frame(window, bg = "black")
        frame_HeureArrive = tkinter.Frame(window, bg = "black")

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(frame_Canvas,bg="black", width = canvasDimWidth, height = canvasDimHeight)
        self.canvas.pack()
        #frame_Canvas.pack(side=tkinter.LEFT, anchor=tkinter.NE)
        #setup directions frame
        frame_Direction.place(x=650, y=100)
        frame_Canvas.place(x=10, y=10)
        frame_Heure.place(x=400, y=50)
        frame_KmRestant.place(x=300,y=400)
        frame_TempsRestant.place(x=500,y=400)
        frame_HeureArrive.place(x=400,y=350)

        #I1 = tkinter.Label(frame_Derection, image = img3).pack()
        
        #tkinter.Label(frame_Direction,bg="black", fg="white", text = "200 m", font=("Helvetica", 20)).pack()
        #tkinter.Label(frame_Direction,bg="black", fg="white", text="13 km/h",  font=("Helvetica", 20)).pack()

        self.Distance = tkinter.Label(frame_Direction,text= "aze",bg="black", fg="white", font=("Helvetica", 20))
        self.Direction = tkinter.Label(frame_Direction,image= self.dicoDirection.get("attente"),bg="black", fg="white")
        self.TempsRestant = tkinter.Label(frame_TempsRestant,text= "",bg="black", fg="white", font=("Helvetica", 20))
        self.HeureArrive = tkinter.Label(frame_HeureArrive,text= "",bg="black", fg="white", font=("Helvetica", 20))
        self.KmRestant = tkinter.Label(frame_KmRestant,text= "",bg="black", fg="white", font=("Helvetica", 20))
        self.Heure = tkinter.Label(frame_Heure,text= "",bg="black", fg="white", font=("Helvetica", 20))
        
        
        self.Direction.pack()
        self.Distance.pack()
        self.TempsRestant.pack()
        self.HeureArrive.pack()
        self.KmRestant.pack()
        self.Heure.pack()     


        #label = tkinter.Label(frame_Direction, bg="black", fg="white",text ="Direction")
        #label.pack(anchor=tkinter.S)
        
        
        #frame_Direction.pack() #side=tkinter.RIGHT, anchor=tkinter.NW
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10
        self.update()
        threadAff = ThreadAffichage(self)
        threadAff.start()
        self.window.mainloop()


    def update(self):
        # Get a frame from the video source
        if self.cameraOn : 
            ret, frame = self.vid.get_frame()

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        else:
            self.canvas.delete("all")
            self.canvas.config(background="black")
        self.window.after(self.delay, self.update)

    def initGPIO(self):
        # configuration de la broche 7 en entree
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
        # definition de l'interruption
        GPIO.add_event_detect(26, GPIO.RISING, callback=self.switch_bt_callback, bouncetime=300)

    def switch_bt_callback(self,a):
        self.cameraOn = not self.cameraOn

    def set_Distance(self, pDistance):
        #print(type(self.Distance))
        self.Distance["text"]= self.conversion_km(pDistance) #.config(text='change the value')

    def set_Direction(self, pDirection):
        self.Direction.configure(image = self.dicoDirection.get(pDirection))

    def set_TempsRestant(self, pTempsRestant):
        self.TempsRestant["text"] = self.conversion_heure(pTempsRestant)

    def set_HeureArrive(self, pHeureArrive):
        self.HeureArrive["text"] = pHeureArrive

    def set_KmRestant(self, pKmRestant):
        self.KmRestant["text"] = self.conversion_km(pKmRestant)

    def set_Heure(self, pHeure):
        self.Heure["text"] = pHeure
        
    def switch(self,clef_arbre,objet_arbre):
        return getattr(self, 'set_' + clef_arbre)(objet_arbre)
    
    def conversion_heure(self,s):
        s = int(s)
        heure = s//3600
        m = s -(heure)*3600
        min = m//60
        if heure == 0 : 
            return str(min)+ "min"
        elif min == 0 and heure != 0:
            return str(heure) + "h"
        else : 
            return str(heure) +"h" + str(min) + "min"
        
    def conversion_km(self,m):
        m=int(m)
        km = m//1000
        m = m - (km)*1000
        if km == 0 :
            return str(m) + "m"
        elif m == 0 and km != 0:
            return str(km) +"km"
        else : 
            return str(km) +"km" + str(m) + "m"


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        #self.vid.set(3, 1280)
        #self.vid.set(4, 720)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            global canvasDimWidth 
            global canvasDimHeight 
            ret, frame = self.vid.read()
            frame = cv2.resize(frame, (canvasDimWidth, canvasDimHeight))
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()



class ThreadCamera(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        global flag_callback
        self.flag = flag_callback
    
    def my_callback():
        # function qui sera appelé lorsque le programme sur interrompu
        flag = True
    
    
    def process_my_callback(a):
        if a == True : 
            __del__()
        else: 
            App(root, "Tkinter and OpenCV")
        a = not a 
   
    def run(self):
        

        # 2- boucle infini = tache principale
        while True:
        # 3- si une interruption c'est produite alors on lance le traitement c
        # adéquat
            if  flag == True:
                process_my_callback(etatCamera)
                flag = False
            
            pass

     

class ThreadAffichage(Thread):
   
    def __init__(self,App):
       Thread.__init__(self)
       self.app = App
       server_addr = "B:27:EB:01:B1:FF"
       port = 1
       backlog = 1
       server_sock = BluetoothSocket(RFCOMM)
       server_sock.setblocking(True)
       server_sock.bind((server_addr, port))
       server_sock.listen(backlog)
       print("lancement application")
       #self.client_socket, address = server_sock.accept() 
    
    def ChangementAffichage(self,clef_arbre,objet_arbre):
        #print('set_' + clef_arbre +": "+objet_arbre)
        #print('thread',type(self.app))
        self.app.switch(clef_arbre,objet_arbre)

    def analyse_xml(self, root):
        if not root.hasChildNodes():
            Parent = root.parentNode
            self.ChangementAffichage(Parent.nodeName, root.nodeValue)
        else : 
            ListeEnfant = root.childNodes
            for x in ListeEnfant :
                self.analyse_xml(x)

    def run(self): 
        while 1:
            try:
                #data = self.client_socket.recv(1024).decode('utf-8')
                data="<?xml version=\"1.0\" encoding=\"UTF-8\"?><code><Distance>1200</Distance><Direction>gauche</Direction><TempsRestant>120</TempsRestant><HeureArrive>12h40</HeureArrive><KmRestant>800</KmRestant><Heure>12h38</Heure></code>"

                #print(data)
                root = minidom.parseString(data)
                #print(root)
                self.analyse_xml(root)
            
            except btcommon.BluetoothError :
                self.client_socket, address = server_sock.accept()
        




# Create a window and pass it to the Application object

root =tkinter.Tk()
root.geometry('854x480')
root.resizable(width=0, height=0)
root['bg']='black'
App(root, "Head UP")
