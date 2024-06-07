import tkinter as tk
from tkinter import Canvas, Menu, Toplevel
import threading
from PIL import Image, ImageDraw, ImageTk
from tkhtmlview import HTMLLabel

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-threaded 2D Drawing App")

        # Set up the canvas
        self.canvas = Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        # Create clear button
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_canvas)
        self.clear_button.pack()

        # Buttons to start threads
        self.button1 = tk.Button(self.root, text="Start Thread 1 (Draw Line)", command=lambda: self.start_thread(self.draw_object1))
        self.button2 = tk.Button(self.root, text="Start Thread 2 (Draw Square)", command=lambda: self.start_thread(self.draw_object2))
        self.button3 = tk.Button(self.root, text="Start Thread 3 (Draw Circle)", command=lambda: self.start_thread(self.draw_object3))

        # Pack the buttons
        self.button1.pack()
        self.button2.pack()
        self.button3.pack()

        # Create a menu bar
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add Help menu
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="View Help", command=self.open_help)

    def clear_canvas(self):
        self.canvas.delete("all")

    def draw_object1(self):
        self.canvas.create_line(100, 250, 100, 100, fill="red", width=3)

    def draw_object2(self):
        self.canvas.create_rectangle(390, 390, 250, 250, fill="green")

    def draw_object3(self):
        size = 100  # diameter of the circle
        image = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        for y in range(size):
            for x in range(size):
                blue = int(255 * (1 - (x + y) / (2 * size)))
                green = int(255 * ((x + y) / (2 * size)))
                draw.point((x, y), fill=(0, green, blue, 255))

        # Create a circular mask
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, size, size), fill=255)

        # Apply the mask to the gradient image
        gradient_circle = Image.composite(image, Image.new('RGBA', (size, size), (255, 255, 255, 0)), mask)

        # Convert the PIL image to a Tkinter PhotoImage
        self.gradient_circle = ImageTk.PhotoImage(gradient_circle)

        # Draw the image on the canvas
        self.canvas.create_image(200, 200, image=self.gradient_circle)

    def start_thread(self, draw_function):
        thread = threading.Thread(target=draw_function)
        thread.start()

    def open_help(self):
        # Create a new window for the help file
        help_window = Toplevel(self.root)
        help_window.title("Help")

        # Load the HTML content
        with open("help.html", "r") as file:
            html_content = file.read()

        # Create an HTMLLabel widget to display the HTML content
        help_label = HTMLLabel(help_window, html=html_content)
        help_label.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
