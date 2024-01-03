import tkinter as tk
from tkinter import *
import cv2
from PIL import ImageTk, Image

class App():
    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry("1080x720")
        self.root.title("Mouse Tracker")
        self.root.iconphoto(False, tk.PhotoImage(file="imgs\goofy.png"))

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.canvasWidth = 800
        self.canvasHeight = 540

        self.canvas = tk.Canvas(self.frame, width=self.canvasWidth, height=self.canvasHeight, bg="#333333", cursor="none")
        self.canvas.pack()

        self.cords = tk.Label(self.frame, text="", font=("Gotham-Bold", 20))
        self.cords.pack(pady=10)
        self.mousePos = (0,0)

        self.cap = cv2.VideoCapture(0)
        self.photo = None
        self.root.after(1, self.videoUpdate)

        self.canvas.bind("<Motion>", self.move)

        self.root.protocol("WM_DELETE_WINDOW", self.release)

        self.root.mainloop()

    def move(self, e):
        x = int(e.x - self.canvasWidth/2)
        y = int(-(e.y - self.canvasHeight/2))
        self.cords.config(text="x: " + str(x) + " y: " + str(y))
    
        self.mousePos = (e.x, e.y)

    def videoUpdate(self):
        ret, frame = self.cap.read()
        self.crop = 50
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.canvasWidth+(self.crop*2), self.canvasHeight))
            frame = frame[:, self.crop:-self.crop]

            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, anchor=NW, image=self.photo)

            # x and y axis
            self.canvas.create_line(0, self.canvasHeight/2, self.canvasWidth, self.canvasHeight/2, fill="white", width=2) # x axis
            self.canvas.create_line(self.canvasWidth/2, 0, self.canvasWidth/2,self.canvasHeight, fill="white", width=2) # y axis

            # draw crosshair
            self.crosshairImg = PhotoImage(file="imgs/crosshair.png")
            self.crosshair = self.canvas.create_image(self.mousePos[0], self.mousePos[1], image=self.crosshairImg)

        self.root.after(1, self.videoUpdate)

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    App()
