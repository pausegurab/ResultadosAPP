import tkinter as tk
from tkinter import filedialog

from FileChoose import FileChoose
import pandas as pd


class VisualizarLiga:
    """
    A class to handle the visualization of the scoresheet document.

    This class creates a new window to display league data loaded from a CSV file.
    """

    def __init__(self, master):
        """
        Initialize the Visualizar Liga window.

        Args:
            master (tk.Tk or tk.Toplevel): The parent window for this interface.
        """
        self.master = tk.Toplevel(master)  # Create a new top-level window
        self.master.title("Visualizar Liga")  # Set the window title
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)  # Define the close protocol

        self.file_path = None
        self.file_name = None
        self.viewResultados() # Set up the interface to view league results
        self.cargar_csv()

    def on_close(self):
        """
        Handle the close event of the window.

        This method brings back the main application window and closes the current window.
        """
        self.master.master.deiconify()  # Restore the main application window
        self.master.destroy()  # Close the current window

    def viewResultados(self):
        """
        Set up the interface elements to view league results.

        This method creates and arranges elements like buttons and text display area
        for the league results.
        """


        # Calculate and set the window size and position
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        width = screen_width // 2
        height = screen_height // 2
        self.master.geometry(f'{round(width*1.2)}x{height}')
        x_left = (screen_width - width) // 2
        y_top = (screen_height - height) // 2
        self.master.geometry(f'+{x_left}+{y_top}')

        # Create and pack the text widget to display league data
        self.nombre_archivo_label = tk.Label(self.master, text="Archivo:")
        self.nombre_archivo_label.grid(row=0, column=0, sticky=tk.W)

        # Text widget para mostrar los datos de la liga
        self.texto_df = tk.Text(self.master, height=height, width=width, wrap='none')
        self.texto_df.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def cargar_csv(self):
        """
        Handle the loading of CSV files.

        This method opens a file dialog to select a CSV file, loads it,
        and displays its content in the text widget.
        """
        filechoose = FileChoose()
        self.file_path = filechoose.get_filepath()
        if self.file_path is None or self.file_path == '':
            self.file_path = filechoose.choose_new_file()
        if self.file_path:
            if "clasificacion" in self.file_path:
                self.file_path = self.file_path.replace('clasificacion.csv', '.csv')
            self.file_name = self.file_path.split('/')[-1].replace('.csv', '')  # Extract the file name

            df = pd.read_csv(self.file_path, index_col=0)  # Load the CSV file into a pandas DataFrame

            # Update the text widget with the DataFrame's content
            self.texto_df.config(state=tk.NORMAL)
            self.texto_df.delete('1.0', tk.END)
            self.texto_df.insert(tk.END, df.to_string())
            self.texto_df.config(state=tk.DISABLED)

            # Display the name of the loaded file
            self.nombre_archivo_label.config(text=f"Archivo: {self.file_name}")



