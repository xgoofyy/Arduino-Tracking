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
        self.mousePos = (0, 0)

        self.cap = cv2.VideoCapture(0)
        self.photo = None
        self.display_mode = "all"  # "all" or "webcam_only"
        self.root.after(1, self.videoUpdate)

        self.canvas.bind("<Motion>", self.move)

        self.toggle_button = tk.Button(self.frame, text="Auto", font=("Gotham-Bold", 10), command=self.toggle_display)
        self.toggle_button.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.release)

        self.root.mainloop()

    def move(self, e):
        if self.display_mode == "all":
            x_scaled = (e.x - self.canvasWidth / 2) * 180 / (self.canvasWidth / 2)
            y_scaled = -(e.y - self.canvasHeight / 2) * 180 / (self.canvasHeight / 2)

            self.cords.config(text="x: " + str(int(x_scaled)) + " y: " + str(int(y_scaled)))
            self.mousePos = (e.x, e.y)

    def videoUpdate(self):
        ret, frame = self.cap.read()
        
        self.crop = 75 # to account for my weird webcam resolution, adjust as needed

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.canvasWidth + (self.crop * 2), self.canvasHeight))
            frame = frame[:, self.crop:-self.crop]

            self.canvas.delete("all") # Clear canvas

            # if webcam is on "manual"
            if self.display_mode == "all":
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, anchor=NW, image=self.photo)

                # x and y axis
                self.canvas.create_line(0, self.canvasHeight / 2, self.canvasWidth, self.canvasHeight / 2, fill="white", width=2)  # x axis
                self.canvas.create_line(self.canvasWidth / 2, 0, self.canvasWidth / 2, self.canvasHeight, fill="white", width=2)  # y axis

                # draw crosshair
                self.crosshairImg = PhotoImage(file="imgs/crosshair.png")
                self.crosshair = self.canvas.create_image(self.mousePos[0], self.mousePos[1], image=self.crosshairImg)

            # else if webcam is on "auto"
            elif self.display_mode == "webcam_only":
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, anchor=NW, image=self.photo)

        self.root.after(1, self.videoUpdate)

    def toggle_display(self):
        if self.display_mode == "all":
            self.display_mode = "webcam_only"
            self.cords.config(text="")
            self.canvas.delete("all")  # Clear canvas
        else:
            self.display_mode = "all"
        self.toggle_button.config(text="Auto" if self.display_mode == "all" else "Manual")

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    App()
