import tkinter as tk
from tkinter import *

class App():
    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry("1080x720")
        self.root.title("Mouse Tracker")

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.canvasWidth = 720
        self.canvasHeight = 540

        self.canvas = tk.Canvas(self.frame, width=self.canvasWidth, height=self.canvasHeight, bg="#333333", cursor="none")
        self.canvas.pack()

        self.canvas.create_line(0, self.canvasHeight/2, self.canvasWidth, self.canvasHeight/2, fill="white", width=2) # x axis
        self.canvas.create_line(self.canvasWidth/2, 0, self.canvasWidth/2,self.canvasHeight, fill="white", width=2) # y axis

        self.crosshairImg = PhotoImage(file="img/crosshair.png")
        self.crosshair = self.canvas.create_image(self.canvasWidth/2, self.canvasHeight/2, image=self.crosshairImg)

        self.cords = tk.Label(self.frame, text="", font=("Gotham-Bold", 20))
        self.cords.pack(pady=10)

        self.canvas.bind("<Motion>", self.move)

        self.root.mainloop()

    def move(self, e):
        x = int(e.x - self.canvasWidth/2)
        y = int(-(e.y - self.canvasHeight/2))
    
        self.crosshairImg = PhotoImage(file="img/crosshair.png")
        self.crosshair = self.canvas.create_image(e.x, e.y, image=self.crosshairImg)
        self.cords.config(text="x: " + str(x) + " y: " + str(y))


if __name__ == "__main__":
    App()

