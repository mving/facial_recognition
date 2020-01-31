"File doc"
import tkinter as tk
from PIL import Image, ImageTk
import detector
import loaders

CONFIG = {
    "cascade": "",
    "camera": 0,
    "cameraResolution": [1280, 720],
    "codec": 'MJPG',
    "fullScreen": True,
    "detectResolution": (427, 240),
    "scaleFactor": 1.2,
    "minNeighbors": 7,
    "minSize": (30, 30),
    "maxSize": (300, 300)
}

class Launcher(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.master.title("Reconocimiento de objetos")
        self.master.geometry("300x400")

        self.cascades = []
        for d in loaders.load_cascades():
            for c in loaders.load_cascades()[d]:
                self.cascades.append(c)
        self.fullScreenVar = tk.IntVar()
        self.fullScreenVar.set(1)
        self.cascadeVar = tk.StringVar(self)
        self.cascadeVar.set([loaders.load_cascades()['lbpcascades'][i] for i, s in enumerate(loaders.load_cascades()['lbpcascades']) if 'frontalface' in s and not 'improved' in s][0])
        self.cameraVar = tk.StringVar(self)
        self.cameraVar.set("0")

        self.museoImg = loaders.find_museo_image()

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        ##### GRAL #####
        render = ImageTk.PhotoImage(Image.open(self.museoImg).resize((200, 200), Image.ANTIALIAS))
        self.img_label = tk.Label(self, image=render)
        self.img_label.image = render
        self.img_label.place(x=0, y=0)

        self.full_screen_check = tk.Checkbutton(self, text="Pantalla completa", variable=self.fullScreenVar)
        self.camera_label = tk.Label(self, text="Camara")
        self.camera_optionmenu = tk.OptionMenu(self, self.cameraVar, "0", *range(loaders.count_cameras()))
        self.cascade_label = tk.Label(self, text="Cascade")
        self.cascade_optionmenu = tk.OptionMenu(self, self.cascadeVar, *self.cascades)
        self.start_button = tk.Button(self, text="Iniciar", font=("Arial bold", 18), command=self.run_detection)

        ##### FORMAT #####
        self.img_label.pack()
        self.full_screen_check.pack()
        self.camera_label.pack()
        self.camera_optionmenu.pack()
        self.cascade_label.pack()
        self.cascade_optionmenu.pack()
        self.start_button.pack(fill='x')

    def run_detection(self):
        CONFIG["cascade"] = self.cascadeVar.get()
        CONFIG["fullScreen"] = self.fullScreenVar.get() == 1
        CONFIG["camera"] = 1
        #CONFIG["camera"] = int(self.cameraVar.get())
        det = detector.Detector(CONFIG)
        det.detect_video()

    def render_settings(self):
        settings = Settings(self)
        settings.mainloop()

# OBSOLETE #
class Settings(tk.Frame):
    def __init(self, master):
        super().__init__(master)
        self.master = master

        self.master.title("Configuración")
        self.master.geometry("800x300")

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        ##### CLASS #####
        self.sampling_label = tk.Label(self, text="Opciones de muestreo", font=("Arial black", 18))
        self.processing_label = tk.Label(self, text="Opciones de procesado", font=("Arial black", 18))
        #self.dataset_optionmenu = tk.OptionMenu(self, self.cascadeVar, "uno", "dos", "tres", "cuatro")
        #self.dataset_optionmenu = tk.OptionMenu(*(self, CONFIG["cascade"]) + tuple(loaders.load_cascades()["lbpcascades"]))

        ##### FORMAT #####
        self.dataset_optionmenu.pack()
        self.sampling_label.pack()
        self.processing_label.pack()
