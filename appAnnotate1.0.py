
# Autor: Joseba Iribarren L.
# Función: Facilitar la identificación de partes de animales

import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import os
import csv


class PhotoViewer:
    def __init__(self, master):

        # Settings
        self.tamano_oval = 3
        self.ancho = 1300
        self.largo = 700 

        self.master_ancho = 1400
        self.master_largo = 800

        self.master = master
        self.master.title("Visualizador de Fotos")
        self.master.geometry(str(self.master_ancho)+'x'+str(self.master_largo))

        self.current_image = None
        self.image_list = []
        self.current_index = -1
        self.original_image = None
        self.click_coordinates = []
        self.oval_ids = []
        

        # Frame para botones
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(side=tk.TOP, pady=10)
        
        # Botones
        self.open_button = tk.Button(self.button_frame, text="Open folder", command=self.open_folder)
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = tk.Button(self.button_frame, text="Previous", command=self.show_previous)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.show_next)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.button_frame, text="Save", command=self.save_coordinates)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # EN PROCESO ==================================================================================================================
        self.zoom_in_button = tk.Button(self.button_frame, text="Zoom in", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = tk.Button(self.button_frame, text="Zoom out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)
        # =============================================================================================================================


        # Etiqueta para mostrar coordenadas
        self.bottom_frame = tk.Frame(self.master, bg="black")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.coord_label = tk.Label(self.bottom_frame, text="Coordenadas: ", fg="white", bg="black", font=("Arial", 12, "bold"))
        self.coord_label.pack(side=tk.LEFT, padx=5)
        self.coord_click = tk.Label(self.bottom_frame, text="Click: ", fg="white", bg="black", font=("Arial", 12, "bold"))
        self.coord_click.pack(side=tk.LEFT, padx=5)

        # Imagen 
        self.imagen_label = tk.Label(self.bottom_frame, text="Image", fg="white", bg="black", font=("Arial", 12, "bold"))
        self.imagen_label.pack(side=tk.LEFT, padx=5)
        
        # colores
        self.position_colors = tk.Label(self.bottom_frame, text="5-Cola", fg="#90EE90", bg="black", font=("Arial", 8, "bold"))
        self.position_colors.pack(side=tk.RIGHT, padx=0)
        self.position_colors = tk.Label(self.bottom_frame, text="4-Fin Aleta", fg="red", bg="black", font=("Arial", 8, "bold"))
        self.position_colors.pack(side=tk.RIGHT, padx=0)
        self.position_colors = tk.Label(self.bottom_frame, text="3-Inicio Aleta", fg="#FFD700", bg="black", font=("Arial", 8, "bold"))
        self.position_colors.pack(side=tk.RIGHT, padx=0)
        self.position_colors = tk.Label(self.bottom_frame, text="2-Espiraculo", fg="#00FFFF", bg="black", font=("Arial", 8, "bold"))
        self.position_colors.pack(side=tk.RIGHT, padx=0)
        self.position_colors = tk.Label(self.bottom_frame, text="1-Cabeza", fg="#FF00FF", bg="black", font=("Arial", 8, "bold"))
        self.position_colors.pack(side=tk.RIGHT, padx=0)





        # Canvas para la imagen
        self.canvas = tk.Canvas(self.master, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # EN PROCESO ==================================================================================================================
        # # Barra de desplazamiento vertical
        # self.v_scrollbar = tk.Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        # self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # # Barra de desplazamiento horizontal
        # self.h_scrollbar = tk.Scrollbar(self.canvas, orient=tk.HORIZONTAL, command=self.canvas.xview)
        # self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # # Configura el canvas para que use las barras de desplazamiento
        # self.canvas.config(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set, scrollregion=(0, 0, int(self.master_ancho), int(self.master_largo)))
        # ===============================================================================================================================

        # funciones del mouse
        self.canvas.bind("<Motion>", self.show_pixel_coord)
        self.canvas.bind("<ButtonPress-1>", lambda event: self.save_pixel_coord(event))
        self.canvas.bind("<ButtonPress-3>", lambda event: self.delete_pixel_coord(event))







    # SECCION DE FUNCIONES =============================================================================================================
    # ==================================================================================================================================
    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_name_list = os.listdir(folder_path)
            self.image_list = [os.path.join(folder_path, f) for f in self.image_name_list
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
            if self.image_list:
                self.current_index = 0
                self.show_image()
            else:
                tk.messagebox.showinfo("Información", "No se encontraron imágenes en la carpeta seleccionada.")

    
    def show_image(self):
        if 0 <= self.current_index < len(self.image_list):
            image_path = self.image_list[self.current_index]

            self.imagen_label.config(text=str(self.image_name_list[self.current_index]))

            self.original_image = Image.open(image_path)
            self.current_image = self.resize_image(self.original_image, self.ancho, self.largo)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)
            self.master.title(f"Visualizador de Fotos - {os.path.basename(image_path)}")
            self.resized_width = self.resized_image.width()
            self.resized_height = self.resized_image.height()

    def resize_image(self, image, ancho, largo):
        image_save_proyect = image.resize(
        (ancho, largo),
        Image.Resampling.LANCZOS)
        self.resized_image = ImageTk.PhotoImage(image_save_proyect)
        return self.resized_image

    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_image()

    def show_next(self):
        if self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            self.load_image()

    def load_image(self):

        self.imagen_label.config(text=str(self.image_name_list[self.current_index]))

        if self.current_image:
            self.current_image = None
            self.original_image = None

        image_path = self.image_list[self.current_index]
        self.original_image = Image.open(image_path)
        self.current_image = self.resize_image(self.original_image, self.ancho, self.largo)
        self.canvas.config(width=self.current_image.width(), height=self.current_image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)
        self.master.title(f"Visualizador de Fotos - {os.path.basename(image_path)}")



    def show_pixel_coord(self, event):
        if self.original_image:
            img_width, img_height = self.original_image.size

            scale_x = img_width / self.resized_width
            scale_y = img_height / self.resized_height

            x = event.x * scale_x
            y = event.y * scale_y

            x = max(0, min(x, img_width))
            y = max(0, min(y, img_height))

            x = int(round(x))
            y = int(round(y))

            self.coord_label.config(text=f"Coordenadas: X: {x}, Y: {y}")
        else:
            self.coord_label.config(text="Coordenadas: N/A")
    
    def save_pixel_coord(self, event):
        if self.original_image:

            position = simpledialog.askinteger("Enter a position (1 - 5)", "Position")
            if position in range(1,6):

                img_width, img_height = self.original_image.size

                scale_x = img_width / self.resized_width
                scale_y = img_height / self.resized_height

                x = event.x * scale_x
                y = event.y * scale_y

                x = max(0, min(x, img_width))
                y = max(0, min(y, img_height))

                x = int(round(x))
                y = int(round(y))

                self.coord_click.config(text=f"Click: X: {x}, Y: {y}")

                self.click_coordinates.append([os.path.basename(self.image_list[self.current_index]), position, int(x), int(y)])

                if position == 1:
                    self.oval_id = self.canvas.create_oval(event.x-self.tamano_oval, event.y-self.tamano_oval, event.x+self.tamano_oval, event.y+self.tamano_oval, 
                                            fill="#FF00FF")  
                elif position == 2:
                    self.oval_id = self.canvas.create_oval(event.x-self.tamano_oval, event.y-self.tamano_oval, event.x+self.tamano_oval, event.y+self.tamano_oval,
                                            fill="#00FFFF")
                elif position == 3:
                    self.oval_id = self.canvas.create_oval(event.x-self.tamano_oval, event.y-self.tamano_oval, event.x+self.tamano_oval, event.y+self.tamano_oval,
                                            fill="#FFD700")
                elif position == 4:
                    self.oval_id = self.canvas.create_oval(event.x-self.tamano_oval, event.y-self.tamano_oval, event.x+self.tamano_oval, event.y+self.tamano_oval, 
                                            fill="red")
                elif position == 5:
                    self.oval_id = self.canvas.create_oval(event.x-self.tamano_oval, event.y-self.tamano_oval, event.x+self.tamano_oval, event.y+self.tamano_oval,
                                            fill="#90EE90")
                self.oval_ids.append(self.oval_id)

                print(f"Posicion {position} guardada en: {x}, {y}")
            else:
                self.coord_click.config(text="Click: N/A")
    
    def delete_pixel_coord(self, event):
        if self.click_coordinates:
            self.click_coordinates.pop()

            ultimo_ovalo = self.oval_ids.pop()
            self.canvas.delete(ultimo_ovalo)

            print("Last position deleted")
        else:
            print("There is no more positions to delete")



    def save_coordinates(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv")])
        if filename:
            self.save_coordinates_to_csv(filename)

    def save_coordinates_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            csv_writer.writerow(['Imagen', 'Position', 'X', 'Y'])
            
            for coord in self.click_coordinates:
                csv_writer.writerow(coord)
        
        print(f"Coordenadas guardadas en '{filename}'")

    
    def zoom_in(self):
        self.ancho = int(round(self.ancho*1.2))
        self.largo = int(round(self.largo*1.2))
        self.canvas.delete("all")
        self.show_image()
    
    def zoom_out(self):
        self.ancho = int(round(self.ancho/1.2))
        self.largo = int(round(self.largo/1.2))
        self.canvas.delete("all")
        self.show_image()




# Correr la app
if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoViewer(root)
    root.mainloop()