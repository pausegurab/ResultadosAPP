import tkinter as tk
from tkinter import filedialog

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



class VisualizarClasificacionGrafico:
    """
    A class to visualize the classification of teams in a graphical format over the course of a season.

    This class creates a new window to display a point graph showing the position of teams across different game weeks.
    """

    def __init__(self, master):
        """
        Initialize the Visualizar Clasificación Gráfico window.

        Args:
            master (tk.Tk or tk.Toplevel): The parent window for this interface.
        """
        self.master = tk.Toplevel(master)  # Create a new top-level window
        self.master.title("Gráfico Jornada a Jornada")  # Set the window title
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)  # Define the close protocol

        self.viewGrafico()  # Set up the interface for viewing the graph

    def on_close(self):
        """
        Handle the close event of the window.

        This method brings back the main application window and closes the current window.
        """
        self.master.master.deiconify()  # Restore the main application window
        self.master.destroy()  # Close the current window

    def viewGrafico(self):
        """
        Set up the graph visualization interface.

        This method creates and configures the graph display, including loading the data
        from a CSV file and plotting it using Matplotlib.
        """
        # Set the window size to full screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        width = screen_width
        height = screen_height
        self.master.geometry(f'{width}x{height}')
        x_left = (screen_width - width) // 2
        y_top = (screen_height - height) // 2
        self.master.geometry(f'+{x_left}+{y_top}')

        # Open file dialog to choose the CSV file
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            self.file_name = self.file_path.split('/')[-1].replace('.csv', '')  # Extract the file name
            self.df_grafico = pd.read_csv(self.file_path, index_col=0)  # Load the CSV file into a pandas DataFrame

            # Create a Matplotlib figure and axis for the graph
            fig = Figure(figsize=(width / 100, height / 100), dpi=100)
            ax = fig.add_subplot(111)
            self.df_grafico['Posicion'] = self.df_grafico['Posicion'].apply(lambda x: int(x) if pd.notnull(x) else x)

            # Count the number of teams
            equipos_cont = sum(1 for _ in self.df_grafico.groupby('Equipo'))

            # Set up a color palette for the teams
            color_palette = plt.colormaps['tab20'].colors

            # Plot each team's position by game week
            for i, (equipo, group) in enumerate(self.df_grafico.groupby('Equipo')):
                ax.plot(group['Jornada'], group['Posicion'], marker='o', label=equipo, color=color_palette[i % len(color_palette)])

            # Configure axis and layout of the graph
            ax.invert_yaxis()  # Invert the y-axis to have the top position at the top
            ax.set_yticks(np.arange(1, equipos_cont + 1, 1))
            ax.set_xticks(np.arange(1, ((equipos_cont - 1) * 2) + 1, 1))
            ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
            ax.set_xlabel('Jornada')
            ax.set_ylabel('Posición')
            ax.set_title('Evolución de la Clasificación por Jornada')
            ax.grid(True)
            ax.set_facecolor('black')

            # Embed the figure in the Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=self.master)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

