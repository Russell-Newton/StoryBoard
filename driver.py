from tkinter import filedialog

from PIL import ImageGrab

from plotpoint import *


class Driver(object):
    def __init__(self, master: tk.Tk, **kwargs):
        self.master = master
        self.canvas = tk.Canvas(self.master, kwargs)
        self.canvas.pack()

        self.plot_points = get_plot_points()

        self.rendered_plot_points = self.render_plot_points()

    def save_image(self):
        """
        Save the image on the canvas using PIL.
        """
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + SCREEN_WIDTH
        y1 = y + SCREEN_HEIGHT
        image = filedialog.asksaveasfilename(title="Select File", filetypes=(("PNG files", "*.png"),
                                                                             ("All Files", "*.*")))
        if not image.endswith(".png"):
            image += ".png"

        if image is not ".png":
            ImageGrab.grab().crop((x, y, x1, y1)).save(image)
        else:
            print("Image saving failed.")

        self.master.destroy()

    def render_plot_points(self) -> list:
        rendered = []
        for plot_point in self.plot_points:
            rendered.append(plot_point.render(self.canvas))
        return rendered


if __name__ == '__main__':
    root = tk.Tk()
    root.overrideredirect(1)
    driver = Driver(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    if SAVE_IMAGE:
        driver.save_image()
    root.mainloop()
