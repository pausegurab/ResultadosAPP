import tkinter as tk
from tkinter import ttk, filedialog

from FileChoose import FileChoose
import pandas as pd


class ActualizarResultados:
    """
    A class to handle the updating of match results in a football league.

    This class creates a new window that allows the user to update the results
    of football matches in a specified CSV file.
    """

    def __init__(self, master):
        """
        Initialize the Actualizar Resultados window.

        Args:
            master (tk.Tk or tk.Toplevel): The parent window for this interface.
        """
        self.master = tk.Toplevel(master)  # Create a new top-level window
        self.master.title("Actualizar Resultados")  # Set the window title
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)  # Define the close protocol

        self.file_name = ""  # Initialize the file name as an empty string
        self.df = None  # Initialize the DataFrame as None

        self.setup_widgets()  # Set up the interface widgets


    def on_close(self):
        """
        Handle the close event of the window.

        This method brings back the main application window and closes the current window.
        """
        self.master.master.deiconify()  # Restore the main application window
        self.master.destroy()  # Close the current window

    def setup_widgets(self):
        """
        Set up the interface widgets for updating results.

        This method creates and arranges elements like labels, comboboxes, and buttons
        for updating match results.
        """
        # Prompt the user to open a CSV file
        filechoose = FileChoose()
        self.file_path = filechoose.get_filepath()
        if self.file_path is None or self.file_path == '':
            self.file_path = filechoose.choose_new_file()
        if self.file_path:
            if "clasificacion" in self.file_path:
                self.file_path = self.file_path.replace('clasificacion.csv', '.csv')
            self.file_name = self.file_path.split('/')[-1].replace('.csv', '')  # Extract the file name
            self.df = pd.read_csv(self.file_path, index_col=0)  # Load the CSV file into a pandas DataFrame

        # Create and arrange interface widgets
        label_local = tk.Label(self.master, text="Local:")
        label_local.grid(row=0, column=0, pady=10)

        self.combo_local = ttk.Combobox(self.master, values=list(self.df.index))
        self.combo_local.grid(row=0, column=1, padx=10, pady=10)

        label_visitante = tk.Label(self.master, text="Visitante:")
        label_visitante.grid(row=1, column=0, pady=10)

        self.combo_visitante = ttk.Combobox(self.master, values=list(self.df.columns))
        self.combo_visitante.grid(row=1, column=1, padx=10, pady=10)

        label_resultado = tk.Label(self.master, text="Resultado:")
        label_resultado.grid(row=2, column=0, pady=10)

        self.entrada_resultado = tk.Entry(self.master)
        self.entrada_resultado.insert(0, '2-1')  # Default value for the result entry
        self.entrada_resultado.grid(row=2, column=1, padx=10, pady=10)

        self.boton_actualizar = tk.Button(self.master, text="Actualizar", command=self.updateCSV)
        self.boton_actualizar.grid(row=3, column=0, columnspan=2, padx=30, pady=30)

        self.nombre_archivo_label = tk.Label(self.master, text=f"Archivo: {self.file_name}")
        self.nombre_archivo_label.grid(row=4, column=0, columnspan=2, sticky='w')

    def updateCSV(self):
        """
        Update the results in the CSV file.

        This method reads the selected match results and updates them in the DataFrame,
        and then writes the updated DataFrame back to the CSV file.
        """
        local = self.combo_local.get()  # Get the home team
        visitante = self.combo_visitante.get()  # Get the away team
        resultado = self.entrada_resultado.get()  # Get the match result

        # Update the DataFrame and save it to the CSV file if the necessary data is present
        if self.df is not None and local and visitante:
            if self.df[visitante].dtype != 'object':
                self.df[visitante] = self.df[visitante].astype('object')

            self.df.at[local, visitante] = str(resultado)
            self.df.to_csv(self.file_path)
            self.entrada_resultado.delete(0, tk.END)  # Clear the result entry field




