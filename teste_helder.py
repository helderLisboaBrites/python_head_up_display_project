import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time


canvasDimWidth = 300
canvasDimHeight = 200
class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        global canvasDimWidth 
        global canvasDimHeight 

        img3 = PIL.ImageTk.PhotoImage(PIL.Image.open("tout_droit1.png")) #resize((50,50), PIL.Image.ANTIALIAS)

        frame_Canvas = tkinter.Frame(window, bg="black")
        frame_Derection = tkinter.Frame(window, bg="black")#, width = 50, height = 50


        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(frame_Canvas, width = canvasDimWidth, height = canvasDimHeight)
        self.canvas.pack()
        frame_Canvas.pack(side=tkinter.LEFT, anchor=tkinter.NE)
        #setup directions frame
        #frame_Derection.place(x=640, y=50)
        I1 = tkinter.Label(frame_Derection, image = img3).pack()
        
        tkinter.Label(frame_Derection,bg="black", fg="white", text = "200 m", font=("Helvetica", 20)).pack()
        tkinter.Label(frame_Derection,bg="black", fg="white", text="13 km/h",  font=("Helvetica", 20)).pack()
        label = tkinter.Label(frame_Derection, bg="black", fg="white",text ="Direction")
        label.pack(anchor=tkinter.S)
        
        
        frame_Derection.pack(side=tkinter.RIGHT, anchor=tkinter.NW)
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
 
        self.window.after(self.delay, self.update)

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

# Create a window and pass it to the Application object

root =tkinter.Tk()
root.geometry('800x400')
root.resizable(width=0, height=0)
root['bg']='black'
App(root, "Tkinter and OpenCV")