import cv2
import numpy as np
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox
from PIL import Image, ImageTk


# todo
#   support variable size
#   implement various image processing
#             variable gui
#   function cv2_image => ImageTk.PhotoImage


class ImageManager:
    def __init__(self, canvas, height, width):
        print("image_processing instantiate!")
        self.path = ""
        self.origin_image = np.empty(0)

        self.displayed_canvas = canvas
        self.origin_height = height
        self.origin_width = width

        self.height = height
        self.width = width

    def convert_cv2imagetk(self, cvimage):
        tmp = cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGB)
        tmp = cv2.resize(tmp, (self.width, self.height))
        tmp = Image.fromarray(tmp)
        return ImageTk.PhotoImage(tmp)

    def open_file(self, path=""):
        self.height = self.origin_height
        self.width = self.origin_width
        self.path = path
        if self.path == "":
            return
        else:
            self.origin_image = cv2.imread(path)
            if len(self.origin_image.shape) == 3:
                height, width, channel = self.origin_image.shape[:3]
            else:
                height, width = self.origin_image.shape[:2]
                channel = 1
            if height / self.height > width / self.width:
                self.width = int(width * (self.height / height))
                print("aa")
            else:
                self.height = int(height * (self.width / width))
            self.tk_origin_image = self.convert_cv2imagetk(self.origin_image)
            self.displayed_canvas.create_image(self.width // 2, self.height // 2, image=self.tk_origin_image)


class ImageProcessing:
    def __init__(self):
        print('init ImageProcessing')

    def threshold_processing(self, cv_image):
        # param 190,255
        processed_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        ret, processed_image = cv2.threshold(processed_image, 190, 255, cv2.THRESH_BINARY)
        return processed_image

    def edge_extraction(self, cv_image):
        # param 100,200
        processed_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        processed_image = cv2.Canny(processed_image, 100.200)
        return processed_image


class MainFrame(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
        self.canvas_size = [500, 800]
        self.image_canvas = tkinter.Canvas(master, bg='gray', height=self.canvas_size[0], width=self.canvas_size[1])
        print(self.image_canvas.winfo_width())
        self.image_canvas.grid(row=1, column=1)
        self.image_manager = ImageManager(self.image_canvas, height=self.canvas_size[0], width=self.canvas_size[1])

    def create_widgets(self):
        menu_buttons = ttk.Menubutton(self, text='File')
        menu = tkinter.Menu(menu_buttons)
        menu_buttons['menu'] = menu
        menu.add_command(label="open", command=self.open_file)
        menu.add_command(label="quit", command=self.quit)
        menu_buttons.grid(row=0, column=0)

    def open_file(self):
        file_type = [('png file', '*.png'), ('jpg file', '*.jpg')]
        dir = 'C:/'  # initialize directory
        file_path = tkinter.filedialog.askopenfilename(filetypes=file_type, initialdir=dir)
        self.image_manager.open_file(path=file_path)

    def quit(self):
        self.master.quit()


if __name__ == '__main__':
    # initialize main tkinter
    root = tkinter.Tk()
    root.state('zoomed')
    app = MainFrame(master=root)
    app.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app.mainloop()