import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImageGrab

class ClipboardImageApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Clipboard Image")

        self.canvas = tk.Canvas(self.window, width=300, height=200)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.button = tk.Button(self.window, text="Get Image from Clipboard", command=self.on_button_click)
        self.button.pack()

        self.top_left_button = tk.Button(self.window, text="Top Left", command=self.set_top_left_mode)
        self.top_left_button.pack()

        self.bottom_right_button = tk.Button(self.window, text="Bottom Right", command=self.set_bottom_right_mode)
        self.bottom_right_button.pack()


        self.image_np = None
        self.current_mode = 'top_left'
        self.tl_h = None
        self.tl_w = None
        self.br_h = None
        self.br_w = None



    def get_image_from_clipboard(self):
        try:
            img = ImageGrab.grabclipboard()
            return img
        except Exception as e:
            print(f"Error getting image from clipboard: {e}")
            return None

    def display_image(self, img):
        if img:
            img_rgb = img.convert('RGB')
            width, height = img_rgb.size
            self.canvas.config(width=width, height=height)

            tk_img = ImageTk.PhotoImage(img_rgb)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
            self.canvas.image = tk_img

            self.image_np = np.array(img_rgb)
        else:
            print("No image found in clipboard")

    def update_image(self):
        if self.image_np is not None:
            img = Image.fromarray(self.image_np)
            width, height = img.size
            self.canvas.config(width=width, height=height)

            tk_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
            self.canvas.image = tk_img
        else:
            print("No image_np to update")

    def on_button_click(self):
        img = self.get_image_from_clipboard()
        self.display_image(img)

    def on_canvas_click(self, event):
        self.click_h = event.y
        self.click_w = event.x

        if self.image_np is not None and 0 <= self.click_h < self.image_np.shape[0] and 0 <= self.click_w < self.image_np.shape[1]:
            print(f"Clicked on image at height: {self.click_h}, width: {self.click_w}")
            print(f"Pixel value: {self.image_np[self.click_h][self.click_w]}")

            if self.current_mode == "top_left":
                self.tl_h = self.click_h
                self.tl_w = self.click_w
                print(f"Top-left corner set to height: {self.tl_h}, width: {self.tl_w}")

            elif self.current_mode == "bottom_right":
                self.br_h = self.click_h
                self.br_w = self.click_w
                print(f"Bottom-right corner set to height: {self.br_h}, width: {self.br_w}")

        else:
            print("Clicked outside of the image")
            
    def set_top_left_mode(self):
        self.current_mode = "top_left"

    def set_bottom_right_mode(self):
        self.current_mode = "bottom_right"


    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ClipboardImageApp()
    app.run()
