import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from skimage import io 
import numpy as np
import keras.utils as image

from IPython.display import display

from keras.models import load_model



disease_class = ['M', 'B']

#interface graphique :


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("800x600")
        self.pack()
        self.create_widgets()
        

    def create_widgets(self):

        #logo label
        logo_image = Image.open("C:\\Users\\fatima ezzahra\\OneDrive\\Bureau\\projethanane\\projet\\ribbon.ico")
        logo_image = logo_image.resize((100, 100), Image.LANCZOS)
        logo_tk_image = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self, image=logo_tk_image)
        logo_label.image = logo_tk_image
        logo_label.pack(padx=10, pady=20)
        #label
        label = tk.Label(self, text="BREAST CANCER DETECTOR" , font=("Arial", 20, "bold"),pady=20)
        label.pack()
        

        self.upload_button = tk.Button(self, text="importer l'image",
        command=self.upload_file,
        font=("Helvetica", 20),
        relief="flat",
        bd=0,
        bg="#f78da7",
        fg="#ffffff",
        activebackground="#ffccff",
        activeforeground="#ffffff",
        cursor="hand2",
        )
        self.upload_button.pack(pady=(30,10))
        self.image_label = tk.Label(self)
        self.image_label.pack(side="top", fill="both", expand="yes")

        self.button= tk.Button(self, text="Analyser",
        command=self.Affichage(text_widget),
        font=("Helvetica", 20),
        relief="flat",
        bd=0,
        bg="#f78da7",
        fg="#ffffff",
        activebackground="#ffccff",
        activeforeground="#ffffff",
        cursor="hand2",
        )
        self.button.pack(pady=(40, 10))

        label = tk.Label(self, text="resultat d'analyse" , font=("Arial", 12, "bold"))
        label.pack(pady=(100, 10))

        text_widget = tk.Text(self, height=1, width=30,state='disabled')
        text_widget.pack()

        

    def upload_file(self):
        global image_path
        image_path = filedialog.askopenfilename()
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=self.photo)        
        
        
    def Analyse_image(image_path):
        loaded_Model = load_model('/content/drive/MyDrive/Breast Cancer Dataset/training_model.h5') 
        show_image = io.imread(image_path)

        img = image.load_img(image_path, grayscale=False, target_size=(224, 224))
        x= image.img_to_array(img)
        x= np.expand_dims(x, axis=0)
        x/= 255
        custom = loaded_Model.predict(x)
        print(custom[0])
        a=custom[0]
        ind=np.argmax(a)
        return disease_class[ind]
            
    def Affichage(self, text_widget):
        prediction = self.Analyse_image
        texte_resultat = f"Résultat d'analyse: {prediction}"
        text_widget.config(state='normal')  # Activer le widget de texte
        text_widget.delete('1.0', tk.END)  # Effacer le texte existant
        text_widget.insert(tk.END, texte_resultat)
        text_widget.config(state='disabled')  # Désactiver le widget de texte
    

root = tk.Tk()
root.title("detection du cancer")
root.wm_iconbitmap('C:\\Users\\fatima ezzahra\\OneDrive\\Bureau\\projethanane\\projet\\ribbon.png')
app = Application(master=root)
app.mainloop()
