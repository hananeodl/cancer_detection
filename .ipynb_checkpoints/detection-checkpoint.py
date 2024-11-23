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
        logo_image = Image.open("ribbon.png")
        logo_image = logo_image.resize((100, 100), Image.LANCZOS)
        logo_tk_image = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self, image=logo_tk_image)
        logo_label.image = logo_tk_image
        logo_label.pack(padx=10, pady=20)
        #label
        label = tk.Label(self, text="BREAST CANCER DETECTOR" , font=("Arial", 20, "bold"),pady=20)
        label.pack()
        

        self.upload_button = tk.Button(self, text="Upload Image",
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

        label = tk.Label(self, text="analysis result" , font=("Arial", 12, "bold"))
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
    
    # def loading_animation(self):
    #     animation = "|/-\\"
    #     message = "loading ..."

    #     for i in range(100):
    #         time.sleep(0.1)
    #         percent = "{:.2f}%".format(i/100*100)
    #         load_str = f"\r{message} {percent} {animation[i%len(animation)]}"
    #         #print(load_str, end="", flush=True)       
    #         label = tk.Label(self, flush=True , font=("Arial", 12, "bold"))
    #         label.pack(pady=(60, 10))
    #         os.system('cls' if os.name == 'nt' else 'clear')

    #     #print("\nDone!")
    #     label = tk.Label(self, text="\nDone!", flush=True , font=("Arial", 12, "bold"))
    #     label.pack(pady=(60, 10))





root = tk.Tk()
root.title("detection du cancer")
root.wm_iconbitmap('ribbon.ico')
app = Application(master=root)
app.mainloop()























# # detection de concer de sein

# from skimage import data, filters, measure, morphology, segmentation

# def analyze_image(image):
#     # Preprocess the image
#     image = morphology.remove_small_objects(image, min_size=32)
#     image = filters.gaussian(image, sigma=1)

#     # Segment the image
#     labels = measure.label(image)

#     # Analyze the regions
#     properties = measure.regionprops(labels)

#     # Classify the regions as cancer or not
#     for prop in properties:
#         if prop.eccentricity > 0.9:
#             return True

#     return False

# #lier l'interface avec l'analyse

# def upload_file(self):
#     file_path = filedialog.askopenfilename()
#     self.image = Image.open(file_path)
#     self.photo = ImageTk.PhotoImage(self.image)
#     self.image_label.config(image=self.photo)

#     # Analyze the image
#     if analyze_image(self.image):
#         self.result_label.config(text="The person on the image may have breast cancer.")
#     else:
#         self.result_label.config(text="The person on the image does not appear to have breast cancer.")