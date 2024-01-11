import tkinter as tk
from tkinter import messagebox

import pandas as pd


class CrearLiga:
    """
    A class to handle the creation of a new football league.

    This class creates a new window that allows the user to input team names
    and set up a new league, generating the necessary data structures and files.
    """

    def __init__(self, master):
        """
        Initialize the Crear Liga window.

        Args:
            master (tk.Tk or tk.Toplevel): The parent window for this interface.
        """
        self.master = tk.Toplevel(master)  # Create a new top-level window
        self.master.title("Crear Liga")  # Set the window title
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)  # Define the close protocol

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.width = int(screen_width // 4)
        height = int(screen_height // 2)


        self.master.geometry(f'{self.width}x{height}')

        self.viewCrearLiga()  # Set up the interface for creating a league

    def on_close(self):
        """
        Handle the close event of the window.

        This method brings back the main application window and closes the current window.
        """
        self.master.master.deiconify()  # Restore the main application window
        self.master.destroy()  # Close the current window

    def viewCrearLiga(self):
        """
        Set up the interface elements for creating a league.

        This method creates and arranges elements like labels, entry fields, lists, and buttons
        for the league creation process.
        """

        self.label_lista = tk.Label(self.master, text="Equipos:")
        self.label_lista.place(x= 10, y = 10)

        self.lista = tk.Listbox(self.master)
        self.lista.place(x=10, y=30)

        self.label_add = tk.Label(self.master, text="Añade un equipo:")
        self.label_add.place(x= 200, y=60)

        self.entrada_equipos = tk.Entry(self.master, width=20)  # Entry for team names
        self.entrada_equipos.place(x=190, y=90)

        self.boton_add = tk.Button(self.master, text="Añadir", command=self.add_to_list)
        self.boton_add.place(x=200, y=120, width=100)

        label_instruccion = tk.Label(self.master,
                                     text="Selecciona un equipo en la lista y pulsa el boton para eliminar:")
        label_instruccion.place(x=10, y=200)


        self.boton_add = tk.Button(self.master, text="Eliminar", command=self.delete_from_list)
        self.boton_add.place(x=self.width//2 - 50, y=230, width=100)

        label_nombre = tk.Label(self.master, text="Indica el nombre del dataframe")
        label_nombre.place(x=10, y=280)

        self.entrada_nombre = tk.Entry(self.master, width=50)  # Entry for the file name
        self.entrada_nombre.place(x=10, y=310)

        boton_confirmar = tk.Button(self.master, text="Crear Liga", command=self.crear_liga)
        boton_confirmar.place(x=self.width//2 - 50, y=340, width=100)

    def add_to_list(self):
        """
        Set up the teams for creating a league.

        This method adds to the list team the team written in the corresponding entry.
        """

        equipo = self.entrada_equipos.get()
        if equipo != '':
            equipo = equipo.upper()

            self.lista.insert(tk.END, equipo)
        self.entrada_equipos.delete(0,tk.END)

    def delete_from_list(self):
        """
        Set up the teams for creating a league.

        This method deletes the selected item from the list.
        """
        seleccion = self.lista.curselection()
        if seleccion:
            index = seleccion[0]
            self.lista.delete(index)

    def crear_liga(self):
        """
        Handle the creation of the league.

        This method reads the input team names and file name, creates the necessary
        data structures for the league, and saves them to CSV files.
        """
        equipos_str = self.lista.get(0,tk.END)
        equipos = list(equipos_str)
        equipos.sort()   # Process the input team names
        print(equipos)

        voltes = (len(equipos) - 1) * 2  # Calculate the number of game-weeks
        jornadas = range(1, voltes + 1)
        multi_index = pd.MultiIndex.from_product([equipos, jornadas], names=['Equipo', 'Jornada'])

        self.df_liga = pd.DataFrame(index=equipos, columns=equipos)  # Create the league DataFrame
        self.historica = pd.DataFrame(index=multi_index, columns=['Posicion'])  # Create the standings DataFrame

        file_name = self.entrada_nombre.get().strip()
        if file_name:
            liga_file_name = f"{file_name}.csv" if not file_name.endswith('.csv') else file_name
            historica_file_name = f"{file_name}clasificacion.csv"

            self.df_liga.to_csv(liga_file_name)  # Save the league DataFrame to CSV
            self.historica.to_csv(historica_file_name)  # Save the standings DataFrame to CSV
        else:
            messagebox.showwarning("Advertencia", "Por favor, introduce un nombre para el archivo de la liga.")

        self.master.master.deiconify()
        self.master.destroy()  # Close the window after creating the league
