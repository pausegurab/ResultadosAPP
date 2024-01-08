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

        This method creates and arranges elements like labels, entry fields, and buttons
        for the league creation process.
        """
        label_instruccion = tk.Label(self.master,
                                     text="Introduce los nombres de los equipos separados por comas:")
        label_instruccion.pack(padx=10, pady=10)

        self.entrada_equipos = tk.Entry(self.master, width=50)  # Entry for team names
        self.entrada_equipos.pack(padx=10, pady=10)

        label_nombre = tk.Label(self.master, text="Indica el nombre del dataframe")
        label_nombre.pack(padx=10, pady=10)

        self.entrada_nombre = tk.Entry(self.master, width=50)  # Entry for the file name
        self.entrada_nombre.pack(padx=10, pady=10)

        boton_confirmar = tk.Button(self.master, text="Crear Liga", command=self.crear_liga)
        boton_confirmar.pack(padx=10, pady=10)

    def crear_liga(self):
        """
        Handle the creation of the league.

        This method reads the input team names and file name, creates the necessary
        data structures for the league, and saves them to CSV files.
        """
        equipos_str = self.entrada_equipos.get()
        equipos_lista = [e.strip() for e in equipos_str.split(',')]  # Process the input team names
        equipos_lista.sort()
        equipos_lista = [equipo.upper() for equipo in equipos_lista]  # Convert team names to uppercase

        voltes = (len(equipos_lista) - 1) * 2  # Calculate the number of game-weeks
        jornadas = range(1, voltes + 1)
        multi_index = pd.MultiIndex.from_product([equipos_lista, jornadas], names=['Equipo', 'Jornada'])

        self.df_liga = pd.DataFrame(index=equipos_lista, columns=equipos_lista)  # Create the league DataFrame
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
