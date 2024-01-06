import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import numpy as np
import pandas as pd
import itertools
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

        self.master.destroy()  # Close the window after creating the league
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
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
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


class VisualizarClasificacion:
    """
    A class for visualizing and managing the league classification.

    This class creates a window for viewing and updating the league standings based on match results.
    It provides functionalities to create and update the classification and handle tie-breaking scenarios.
    """

    def __init__(self, master):
        """
        Initialize the Visualizar Clasificacion window.

        Args:
            master (tk.Tk or tk.Toplevel): The parent window for this interface.
        """
        self.master = tk.Toplevel(master)  # Create a new top-level window
        self.master.title("Visualizar Clasificacion")  # Set the window title
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)  # Define the close protocol

        # Initialize data structures for classification
        self.df = None
        self.clasificacion = None
        self.file_path = ""
        self.file_name = ""
        self.rows = 0
        self.df_empates = None
        self.df_empates_par = None
        self.df_empates_grupo = None

        # Create and update the classification view
        self.createClasificacion()
        self.updateClasificacion()

    def on_close(self):
        """
        Handle the close event of the window.

        This method brings back the main application window and closes the current window.
        """
        self.master.master.deiconify()  # Restore the main application window
        self.master.destroy()  # Close the current window

    def createClasificacion(self):
        """
        Create the initial league classification structure.

        This method sets up the initial DataFrame for the league classification by loading match results from a CSV file.
        It initializes a DataFrame to store teams' standings based on various statistics like points, goals for, goals against, etc.
        """
        # Open a file dialog to select a CSV file containing match results
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            # Extract the file name from the path and load the CSV file into a DataFrame
            self.file_name = self.file_path.split('/')[-1].replace('.csv', '')
            self.df = pd.read_csv(self.file_path, index_col=0)

        # Determine the number of teams (rows) from the loaded DataFrame
        self.rows = self.df.shape[0]

        # Initialize the classification DataFrame with appropriate columns
        # Columns include team name, played matches (PJ), wins (PG), draws (PE), losses (PP),
        # goals for (GF), goals against (GC), goal difference (DIF), and points (PTS)
        self.clasificacion = pd.DataFrame(index=range(1, self.rows + 1), columns=range(9))
        self.clasificacion.columns = ['EQUIPO', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DIF', 'PTS']

        # Fill the 'EQUIPO' column with team names and initialize other columns to 0
        # Calculate the initial goal difference for each team
        self.clasificacion['EQUIPO'] = self.df.index
        self.clasificacion.fillna(0, inplace=True)
        self.clasificacion['DIF'] = self.clasificacion['GF'] - self.clasificacion['GC']

    def updateClasificacion(self):
        """
        Update the league classification with match results.

        This method processes the results of football matches from the loaded DataFrame
        and updates the league standings accordingly. It handles the calculation of points,
        goals for, goals against, and updates the standings based on match outcomes.
        """
        # Set the window size and position
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        width = screen_width // 2
        height = screen_height // 2
        self.master.geometry(f'{width}x{height}')
        x_left = (screen_width - width) // 2
        y_top = (screen_height - height) // 2
        self.master.geometry(f'+{x_left}+{y_top}')

        # Create and position the text widget for displaying the classification
        self.texto_clasificacion = tk.Text(self.master, height=height, width=width, wrap='none')
        self.texto_clasificacion.place(x=10, y=10, width=width - 20, height=height - 60)

        # Create and position the 'Guardar clasificacion' button
        self.boton_historica = tk.Button(self.master, text="Guardar clasificacion", command=self.guardar_historica)
        self.boton_historica.place(x=10, y=height - 50, width=width - 20, height=30)

        # Process match results to update team standings
        self.equipos = self.clasificacion['EQUIPO'].tolist()
        self.combinaciones = list(itertools.combinations(self.equipos, 2))

        # Initialize DataFrame for storing detailed match results
        self.ga = pd.DataFrame(self.combinaciones, columns=['Local', 'Visitante'])
        self.ga['GOLL'] = 0  # Goals scored by the local team
        self.ga['GOLV'] = 0  # Goals scored by the visiting team
        self.ga['GA'] = 0    # Goal average
        self.ga['ENF'] = 0   # Number of encounters

        # Iterate through the results DataFrame and update match statistics
        for local in self.df.index:
            for visitante in self.df.columns:
                resultado = self.df.at[local, visitante]
                if pd.notna(resultado):
                    goles_local, goles_visitante = map(int, resultado.split("-"))

                    # Update match results in the ga DataFrame
                    filtro = (self.ga['Local'] == local) & (self.ga['Visitante'] == visitante)
                    indices = self.ga[filtro].index

                    if not indices.empty:
                        # If the record exists, update the goals and encounter count
                        ind = indices[0]
                        self.ga.loc[ind, 'GOLL'] += goles_local  # Update goals for the local team
                        self.ga.loc[ind, 'GOLV'] += goles_visitante  # Update goals for the visiting team
                        self.ga.loc[ind, 'ENF'] += 1  # Increment the number of encounters
                    else:
                        # If the record does not exist, handle the reverse case (visitante vs local)
                        # This can occur if the team names in the DataFrame are not consistent
                        ga_visitant = local
                        ga_local = visitante
                        gols_local = goles_visitante
                        gols_visitant = goles_local

                        ind_rev = self.ga[(self.ga['Local'] == ga_local) & (self.ga['Visitante'] == ga_visitant)].index
                        if not ind_rev.empty:
                            # Update the reverse record with the reversed goals and increment encounter count
                            self.ga.loc[ind_rev[0], 'GOLL'] += gols_local
                            self.ga.loc[ind_rev[0], 'GOLV'] += gols_visitant
                            self.ga.loc[ind_rev[0], 'ENF'] += 1

                            # Update goals for and against for both local and visiting teams
                    self.clasificacion.loc[self.clasificacion['EQUIPO'] == local, 'GF'] += goles_local
                    self.clasificacion.loc[self.clasificacion['EQUIPO'] == local, 'GC'] += goles_visitante
                    self.clasificacion.loc[self.clasificacion['EQUIPO'] == visitante, 'GF'] += goles_visitante
                    self.clasificacion.loc[self.clasificacion['EQUIPO'] == visitante, 'GC'] += goles_local

                    # Increment the number of played matches (PJ) for both teams
                    self.clasificacion.loc[self.clasificacion['EQUIPO'] == local, 'PJ'] += 1
                    self.clasificacion.loc[self.clasificacion['EQUIPO'] == visitante, 'PJ'] += 1

                    # Determine and update points (PTS), wins (PG), draws (PE), and losses (PP) based on the match outcome
                    if goles_local > goles_visitante:
                        # Local team wins
                        self.clasificacion.loc[self.clasificacion['EQUIPO'] == local, 'PTS'] += 3
                        self.clasificacion.loc[self.clasificacion['EQUIPO'] == local, 'PG'] += 1
                        self.clasificacion.loc[self.clasificacion['EQUIPO'] == visitante, 'PP'] += 1
                    elif goles_local < goles_visitante:
                        # Visiting team wins
                        self.clasificacion.loc[self.clasificacion['EQUIPO'] == visitante, 'PTS'] += 3
                        self.clasificacion.loc[self.clasificacion['EQUIPO'] == local, 'PP'] += 1
                        self.clasificacion.loc[self.clasificacion['EQUIPO'] == visitante, 'PG'] += 1
                    else:
                        # Match is a draw
                        self.clasificacion.loc[self.clasificacion['EQUIPO'] == local, 'PTS'] += 1
                        self.clasificacion.loc[self.clasificacion['EQUIPO'] == visitante, 'PTS'] += 1
                        self.clasificacion.loc[self.clasificacion['EQUIPO'] == local, 'PE'] += 1
                        self.clasificacion.loc[self.clasificacion['EQUIPO'] == visitante, 'PE'] += 1

        # Calculate the goal average (GA) for each match-up in the 'ga' DataFrame
        self.ga['GA'] = self.ga['GOLL'] - self.ga['GOLV']

        # Sort the 'clasificacion' DataFrame based on points (PTS), descending order
        # This sorts the teams from highest to lowest points
        self.clasificacion = self.clasificacion.sort_values(by='PTS', ascending=False)

        # Reset the index of the DataFrame and update the goal difference (DIF) column
        self.clasificacion.reset_index(drop=True, inplace=True)
        self.clasificacion['DIF'] = self.clasificacion['GF'] - self.clasificacion['GC']
        self.clasificacion.index = range(1, self.rows + 1)

        # Create additional DataFrames for managing ties in points between teams
        self.crear_dataframe_empates()

        # If there are ties, apply tie-breaking rules
        if self.df_empates is not None:
            self.desempate_par()  # Handle tie-breaking for pairs of teams
            self.desempate_grupos()  # Handle tie-breaking for groups of teams

        # If a file path is set, display the updated classification in the text widget
        if self.file_path:
            self.file_name = self.file_path.split('/')[-1].replace('.csv', '')
            self.texto_clasificacion.config(state=tk.NORMAL)
            self.texto_clasificacion.delete('1.0', tk.END)
            self.texto_clasificacion.insert(tk.END, self.clasificacion.to_string())
            self.texto_clasificacion.config(state=tk.DISABLED)

    def crear_dataframe_empates(self):
        """
        Create DataFrames to manage teams with tied points.

        This method creates separate DataFrames for teams that are tied on points.
        It categorizes ties into pairs and groups of three or more teams.
        """
        # Initialize lists to hold rows of teams with tied points
        filas_empatadas = []       # For all ties
        filas_empatadas_2 = []     # For ties between two teams
        filas_empatadas_3_mas = [] # For ties among three or more teams

        # Get unique point values from the classification
        puntos = self.clasificacion['PTS'].unique()

        # Loop through each unique point value
        for p in puntos:
            # Get teams that are tied on these points
            equipos_empatados = self.clasificacion[self.clasificacion['PTS'] == p]

            # If there are ties (more than one team with the same points)
            if len(equipos_empatados) > 1:
                # Add each row to the tied teams list
                for index, fila in equipos_empatados.iterrows():
                    filas_empatadas.append(fila)

                # Handle ties between exactly two teams
                if len(equipos_empatados) == 2:
                    for index, fila in equipos_empatados.iterrows():
                        filas_empatadas_2.append(fila)

                # Handle ties among three or more teams
                elif len(equipos_empatados) >= 3:
                    for index, fila in equipos_empatados.iterrows():
                        filas_empatadas_3_mas.append(fila)

        # Create DataFrames from the lists
        self.df_empates = pd.DataFrame(filas_empatadas)          # DataFrame for all tied teams
        self.df_empates_par = pd.DataFrame(filas_empatadas_2)    # DataFrame for ties between two teams on the same points
        self.df_empates_grupo = pd.DataFrame(filas_empatadas_3_mas) # DataFrame for ties among three or more teams

    def desempate_par(self):
        """
        Apply tie-breaking rules for pairs of teams that are tied on points.

        This method resolves ties by examining the head-to-head results between each pair of tied teams.
        If there were exactly two encounters, it uses the goal average as a tiebreaker. Otherwise, it
        sorts the teams based on other criteria like total points, goal difference, and goals for.
        """
        # Check if there are pairs of teams with tied points
        if not self.df_empates_par.empty:
            # Iterate over each pair of tied teams
            for i in range(0, self.df_empates_par.shape[0], 2):
                # Extract pairs of teams and their respective match data
                self.par = self.df_empates_par.iloc[i:i+2]
                equipo1, equipo2 = self.df_empates_par['EQUIPO'].iloc[i], self.df_empates_par['EQUIPO'].iloc[i+1]
                self.par.index = range(1, 3)

                # Find matches between the two teams
                filtro = (self.ga['Local'] == equipo1) & (self.ga['Visitante'] == equipo2)
                indices = self.ga[filtro].index

                if not indices.empty:
                    ind = indices[0]
                    # If there were exactly two encounters, use the goal average to break the tie
                    if self.ga.loc[ind, 'ENF'] == 2:
                        average = self.ga.loc[ind, 'GA']
                        self.updateGA(equipo1, equipo2, average)


                    else:

                        # Extract the names of the tied teams

                        self.equiposTemp = self.par['EQUIPO'].tolist()

                        # Sort these teams based on total points, goal difference, goals for, and then team name

                        # This is the tie-breaking criteria if they haven't met exactly twice

                        self.par = self.par.sort_values(by=['PTS', 'DIF', 'GF', 'EQUIPO'],
                                                        ascending=[False, False, False, True])

                        # Find the positions of these teams in the overall classification

                        posicons_empatades = []

                        for equipo in self.equiposTemp:
                            posicion = self.clasificacion.index[self.clasificacion['EQUIPO'] == equipo].tolist()[0]

                            posicons_empatades.append(posicion)

                        # Reorder the teams in the main classification based on the sorted order

                        equipos_reordenados = self.par['EQUIPO'].tolist()

                        for i, posicion in enumerate(posicons_empatades):

                            equipo = equipos_reordenados[i]

                            equipo_stats = self.par[self.par['EQUIPO'] == equipo].iloc[0]

                            # Update each statistic for the team in the main classification

                            for columna in ['EQUIPO', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DIF', 'PTS']:
                                self.clasificacion.at[posicion, columna] = equipo_stats[columna]
                else:
                # Check for encounters in the reverse order (team2 vs team1)
                    ind_rev = self.ga[
                    (self.ga['Local'] == equipo2) & (self.ga['Visitante'] == equipo1)].index
                    if not ind_rev.empty:
                        # If there were exactly two reverse encounters, use the goal average to break the tie
                        if self.ga.loc[ind_rev[0], 'ENF'] == 2:
                            average = self.ga.loc[ind_rev[0], 'GA']
                            self.updateGA(equipo2, equipo1, average)
                        else:
                            # If not exactly two encounters, sort teams based on other criteria
                            self.equiposTemp = self.par['EQUIPO'].tolist()
                            self.par = self.par.sort_values(by=['PTS', 'DIF', 'GF', 'EQUIPO'],
                                                            ascending=[False, False, False, True])

                            # Determine the positions of these teams in the overall classification
                            posicons_empatades = []
                            for equipo in self.equiposTemp:
                                posicion = \
                                self.clasificacion.index[self.clasificacion['EQUIPO'] == equipo].tolist()[0]
                                posicons_empatades.append(posicion)

                            # Reorder the teams in the main classification based on the sorted order
                            equipos_reordenados = self.par['EQUIPO'].tolist()
                            for i, posicion in enumerate(posicons_empatades):
                                equipo = equipos_reordenados[i]
                                equipo_stats = self.par[self.par['EQUIPO'] == equipo].iloc[0]

                                # Update each statistic for the team in the main classification
                                for columna in ['EQUIPO', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DIF', 'PTS']:
                                    self.clasificacion.at[posicion, columna] = equipo_stats[columna]


    def desempate_grupos(self):
        """
        Apply tie-breaking rules for groups of three or more teams that are tied on points.

        This method handles ties involving larger groups of teams by examining their
        performance against each other and applying tie-breaking criteria.
        """
        # Check if there are groups of three or more teams with tied points
        if not self.df_empates_grupo.empty:
            # Get unique point values from these groups
            puntos_unicos = self.df_empates_grupo['PTS'].unique()

            # Iterate over each unique point value
            for p in puntos_unicos:
                # Extract the teams that are tied on these points
                drawedTeams = self.df_empates_grupo[self.df_empates_grupo['PTS'] == p]

                # Call a method to process the tie-breaking for these teams
                self.clasificacionTemp(drawedTeams)



    def clasificacionTemp(self, drawedTeams):
        """
        Process tie-breaking for groups of teams with equal points.

        This method creates a temporary DataFrame to compare the results of matches
        between the tied teams and applies tie-breaking rules based on their head-to-head records.

        Args:
            drawedTeams (DataFrame): A DataFrame containing teams that are tied.
        """
        # Extract the names of the teams involved in the tie
        self.equiposTemp = drawedTeams['EQUIPO'].tolist()

        # Set up a temporary DataFrame for the tied teams
        self.rows = len(self.equiposTemp)
        self.temp = pd.DataFrame(index=range(1, self.rows + 1), columns=range(9))
        self.temp.columns = ['EQUIPO', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DIF', 'PTS']
        self.temp['EQUIPO'] = self.equiposTemp
        self.temp.fillna(0, inplace=True)
        # Initialize goal difference based on the main classification
        self.temp['DIF'] = self.clasificacion['GF'] - self.clasificacion['GC']

        # Boolean flag to track if all encounters are two-legged (home and away)
        enf = True

        # Iterate through each match involving the tied teams
        for local in self.df.index:
            for visitante in self.df.columns:
                if local in self.equiposTemp and visitante in self.equiposTemp:
                    resultado = self.df.at[local, visitante]

                    if pd.notna(resultado):
                        # Process the match result
                        goles_local, goles_visitante = map(int, resultado.split("-"))

                        # Check if there's a direct encounter between the teams
                        filtro = (self.ga['Local'] == local) & (self.ga['Visitante'] == visitante)
                        indices = self.ga[filtro].index

                        if not indices.empty:
                            ind = indices[0]
                            # If all encounters are two-legged, keep 'enf' as True
                            if self.ga.loc[ind, 'ENF'] == 2 and enf:
                                enf = True
                            elif self.ga.loc[ind, 'ENF'] != 0 and enf:
                                # If any encounter is not two-legged, set 'enf' to False
                                enf = False

                        else:
                            # Check for reverse encounters
                            ind_rev = self.ga[(self.ga['Local'] == visitante) & (self.ga['Visitante'] == local)].index
                            if not ind_rev.empty:
                                if self.ga.loc[ind_rev[0], 'ENF'] == 2 and enf:
                                    enf = True
                                elif self.ga.loc[ind_rev[0], 'ENF'] != 0 and enf:
                                    enf = False
                        # Update goals for, goals against, and played matches for both teams
                        self.temp.loc[self.temp['EQUIPO'] == local, 'GF'] += goles_local
                        self.temp.loc[self.temp['EQUIPO'] == local, 'GC'] += goles_visitante
                        self.temp.loc[self.temp['EQUIPO'] == visitante, 'GF'] += goles_visitante
                        self.temp.loc[self.temp['EQUIPO'] == visitante, 'GC'] += goles_local
                        self.temp.loc[self.temp['EQUIPO'] == local, 'PJ'] += 1
                        self.temp.loc[self.temp['EQUIPO'] == visitante, 'PJ'] += 1

                        # Determine and update points (PTS), wins (PG), draws (PE), and losses (PP) based on the match outcome
                        if goles_local > goles_visitante:
                            # Local team wins
                            self.temp.loc[self.temp['EQUIPO'] == local, 'PTS'] += 3
                            self.temp.loc[self.temp['EQUIPO'] == local, 'PG'] += 1
                            self.temp.loc[self.temp['EQUIPO'] == visitante, 'PP'] += 1
                        elif goles_local < goles_visitante:
                            # Visiting team wins
                            self.temp.loc[self.temp['EQUIPO'] == visitante, 'PTS'] += 3
                            self.temp.loc[self.temp['EQUIPO'] == local, 'PP'] += 1
                            self.temp.loc[self.temp['EQUIPO'] == visitante, 'PG'] += 1
                        else:
                            # Match is a draw
                            self.temp.loc[self.temp['EQUIPO'] == local, 'PTS'] += 1
                            self.temp.loc[self.temp['EQUIPO'] == visitante, 'PTS'] += 1
                            self.temp.loc[self.temp['EQUIPO'] == local, 'PE'] += 1
                            self.temp.loc[self.temp['EQUIPO'] == visitante, 'PE'] += 1

                # Calculate goal difference for the tied teams based on their temporary records
        self.temp['DIF'] = self.temp['GF'] - self.temp['GC']

        # Initialize columns for overall/general statistics
        self.temp['DIF_GENERAL'] = 0
        self.temp['GF_GENERAL'] = 0
        self.temp['GC_GENERAL'] = 0
        self.temp['PTS_GENERAL'] = 0
        self.temp['PJ_GENERAL'] = 0
        self.temp['PG_GENERAL'] = 0
        self.temp['PE_GENERAL'] = 0
        self.temp['PP_GENERAL'] = 0

        # Loop through each team in the temporary DataFrame for tied teams
        for i in range(len(self.temp)):
            # Retrieve the team's name
            equipo = self.temp.at[i + 1, 'EQUIPO']

            # Fetch the team's general statistics from the main classification DataFrame
            dif_goles_general = self.clasificacion.loc[self.clasificacion['EQUIPO'] == equipo, 'DIF'].values[0]
            gf_general = self.clasificacion.loc[self.clasificacion['EQUIPO'] == equipo, 'GF'].values[0]
            gc_general = self.clasificacion.loc[self.clasificacion['EQUIPO'] == equipo, 'GC'].values[0]
            pts_general = self.clasificacion.loc[self.clasificacion['EQUIPO'] == equipo, 'PTS'].values[0]
            pj_general = self.clasificacion.loc[self.clasificacion['EQUIPO'] == equipo, 'PJ'].values[0]
            pg_general = self.clasificacion.loc[self.clasificacion['EQUIPO'] == equipo, 'PG'].values[0]
            pe_general = self.clasificacion.loc[self.clasificacion['EQUIPO'] == equipo, 'PE'].values[0]
            pp_general = self.clasificacion.loc[self.clasificacion['EQUIPO'] == equipo, 'PP'].values[0]

            # Update the temporary DataFrame with these general statistics
            self.temp.loc[i + 1, 'DIF_GENERAL'] = dif_goles_general
            self.temp.loc[i + 1, 'GF_GENERAL'] = gf_general
            self.temp.loc[i + 1, 'GC_GENERAL'] = gc_general
            self.temp.loc[i + 1, 'PTS_GENERAL'] = pts_general
            self.temp.loc[i + 1, 'PJ_GENERAL'] = pj_general
            self.temp.loc[i + 1, 'PG_GENERAL'] = pg_general
            self.temp.loc[i + 1, 'PE_GENERAL'] = pe_general
            self.temp.loc[i + 1, 'PP_GENERAL'] = pp_general

        # Apply tie-breaking rules if all encounters between the tied teams are two-legged
        if enf:
            # Sort the temporary DataFrame with the tied teams based on multiple criteria.
            # Criteria: points, goal difference, general goal difference, general goals for, and team name
            self.temp = self.temp.sort_values(by=['PTS', 'DIF', 'DIF_GENERAL', 'GF_GENERAL', 'EQUIPO'],
                                              ascending=[False, False, False, False, True])
            # Reset the index for sorted DataFrame
            self.temp.reset_index(drop=True, inplace=True)
            self.temp.index = range(1, self.rows + 1)

            # Find the positions of the tied teams in the main classification
            posicons_empatades = []
            for equipo in self.equiposTemp:
                posicion = self.clasificacion.index[self.clasificacion['EQUIPO'] == equipo].tolist()[0]
                posicons_empatades.append(posicion)

            # Reorder the teams in the main classification based on the sorted order
            equipos_reordenados = self.temp['EQUIPO'].tolist()
            for i, posicion in enumerate(posicons_empatades):
                equipo = equipos_reordenados[i]
                equipo_stats = self.temp[self.temp['EQUIPO'] == equipo].iloc[0]

                # Update each statistic for the team in the main classification
                for columna in ['EQUIPO', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DIF', 'PTS']:
                    # Use general stats for updating if the column isn't 'EQUIPO'
                    if columna != 'EQUIPO':
                        self.clasificacion.at[posicion, columna] = equipo_stats[columna + '_GENERAL']
                    else:
                        self.clasificacion.at[posicion, columna] = equipo_stats[columna]


        # Apply tie-breaking rules if not all encounters between the tied teams are two-legged
        else:
            # Sort the temporary DataFrame with the tied teams based on different criteria.
            # Criteria: general goal difference, general goals for, and team name
            self.temp = self.temp.sort_values(by=['DIF_GENERAL', 'GF_GENERAL', 'EQUIPO'],
                                              ascending=[False, False, True])
            # Reset the index for sorted DataFrame
            self.temp.reset_index(drop=True, inplace=True)
            self.temp.index = range(1, self.rows + 1)
            # Find the positions of the tied teams in the main classification
            posicons_empatades = []
            for equipo in self.equiposTemp:
                posicion = self.clasificacion.index[self.clasificacion['EQUIPO'] == equipo].tolist()[0]
                posicons_empatades.append(posicion)
            # Reorder the teams in the main classification based on the sorted order
            equipos_reordenados = self.temp['EQUIPO'].tolist()
            for i, posicion in enumerate(posicons_empatades):
                equipo = equipos_reordenados[i]
                equipo_stats = self.temp[self.temp['EQUIPO'] == equipo].iloc[0]
                # Update each statistic for the team in the main classification
                for columna in ['EQUIPO', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DIF', 'PTS']:
                    # Use general stats for updating if the column isn't 'EQUIPO'
                    if columna != 'EQUIPO':
                        self.clasificacion.at[posicion, columna] = equipo_stats[columna + '_GENERAL']
                    else:
                        self.clasificacion.at[posicion, columna] = equipo_stats[columna]

    def updateGA(self, equipo1, equipo2, average):
        # Check if the goal average is positive
        if average > 0:
            # Find the indices of the two teams in the main classification
            indice_1 = self.clasificacion[self.clasificacion['EQUIPO'] == equipo1].index[0]
            indice_2 = self.clasificacion[self.clasificacion['EQUIPO'] == equipo2].index[0]
            # Check if the team with higher goal average should be moved up in the classification
            if indice_1 < indice_2:
                return
            # Swap the positions of the two teams in the classification
            a, b = self.clasificacion.iloc[indice_1 - 1].copy(), self.clasificacion.iloc[indice_2 - 1].copy()
            self.clasificacion.iloc[indice_1 - 1], self.clasificacion.iloc[indice_2 - 1] = b, a

        # Check if the goal average is negative
        elif average < 0:
            # Find the indices of the two teams in the main classification
            indice_2 = self.clasificacion[self.clasificacion['EQUIPO'] == equipo1].index[0]
            indice_1 = self.clasificacion[self.clasificacion['EQUIPO'] == equipo2].index[0]
            # Check if the team with higher goal average should be moved up in the classification
            if indice_1 < indice_2:
                return
            # Swap the positions of the two teams in the classification
            a, b = self.clasificacion.iloc[indice_1 - 1].copy(), self.clasificacion.iloc[indice_2 - 1].copy()
            self.clasificacion.iloc[indice_1 - 1], self.clasificacion.iloc[indice_2 - 1] = b, a

        # Handle the case when goal average is zero
        else:
            self.equiposTemp = self.par['EQUIPO'].tolist()
            self.par = self.par.sort_values(by=['PTS', 'DIF', 'GF', 'EQUIPO'],
                                            ascending=[False, False, False, True])
            posicons_empatades = []
            for i in self.equiposTemp:
                posicion = self.clasificacion.index[self.clasificacion['EQUIPO'] == i].tolist()[0]
                posicons_empatades.append(posicion)
            equipos_reordenados = self.par['EQUIPO'].tolist()
            for i, posicion in enumerate(posicons_empatades):
                equipo = equipos_reordenados[i]
                equipo_stats = self.par[self.par['EQUIPO'] == equipo].iloc[0]
                # Update each statistic for the team in the main classification
                for columna in ['EQUIPO', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DIF', 'PTS']:
                    self.clasificacion.at[posicion, columna] = equipo_stats[columna]


    def guardar_historica(self):
        # Create a temporary file path and name for the historical classification
        self.file_path_temp = self.file_path
        self.file_path_temp = self.file_path_temp.replace('.csv', 'clasificacion.csv')
        self.file_name_temp = self.file_path_temp.split('/')[-1].replace('.csv', '')

        # Read the historical classification from the temporary file path
        self.df_hist = pd.read_csv(self.file_path_temp)

        # Get the current matchday from the current classification
        jornada_actual = self.clasificacion['PJ'].iloc[0]

        # Iterate through each team in the current classification
        for equipo in self.clasificacion['EQUIPO'].tolist():
            # Get the current position of the team in the current classification
            posicion_actual = self.clasificacion[self.clasificacion['EQUIPO'] == equipo].index[0]

            # Find the row in the historical classification that matches the current matchday and team
            filtro = (self.df_hist['Jornada'] == jornada_actual) & (self.df_hist['Equipo'] == equipo)
            indices = self.df_hist[filtro].index

            # Get the index of the matching row
            ind = indices[0]

            # Update the 'Posicion' column in the historical classification with the current position
            self.df_hist.loc[ind, 'Posicion'] = posicion_actual

        # Save the updated historical classification to a CSV file
        self.df_hist.to_csv(self.file_name_temp + '.csv', index=False)


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

        self.viewResultados()  # Set up the interface to view league results

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
        # Create and pack the 'Cargar CSV' button
        boton_cargar_csv = tk.Button(self.master, text="Cargar CSV", command=self.cargar_csv)
        boton_cargar_csv.pack()

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
        self.texto_df = tk.Text(self.master, height=height, width=width, wrap='none')
        self.texto_df.pack(expand=True, fill='both')

    def cargar_csv(self):
        """
        Handle the loading of CSV files.

        This method opens a file dialog to select a CSV file, loads it,
        and displays its content in the text widget.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])  # Open file dialog to choose a CSV file
        if file_path:
            file_name = file_path.split('/')[-1].replace('.csv', '')  # Extract the file name

            df = pd.read_csv(file_path, index_col=0)  # Load the CSV file into a pandas DataFrame

            # Update the text widget with the DataFrame's content
            self.texto_df.config(state=tk.NORMAL)
            self.texto_df.delete('1.0', tk.END)
            self.texto_df.insert(tk.END, df.to_string())
            self.texto_df.config(state=tk.DISABLED)

            # Display the name of the loaded file
            self.nombre_archivo_label = tk.Label(self.master, text=f"Archivo: {file_name}")
            self.nombre_archivo_label.pack()


class App:
    """
    Main application class for the Football Tables application.

    This class initializes the main window and sets up the main screen with
    various options related to football league management.
    """

    def __init__(self, master):
        """
        Initialize the application.

        Args:
            master (tk.Tk): The main tkinter window.
        """
        self.master = master
        self.master.title("TABLAS DE FUTBOL")  # Set the window title

        self.master.configure(bg='black')  # Set the background color of the window

        # Calculate the width and height for the window to be half of the screen size
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        width = int(screen_width / 2)
        height = int(screen_height / 2)

        # Set the geometry of the window (size and position)
        self.master.geometry(f'{width}x{height}')
        self.master.geometry(f'+{screen_width // 4}+{screen_height // 4}')

        self.setup_main_screen()  # Setup the main screen with buttons

    def setup_main_screen(self):
        """
        Set up the main screen of the application.

        This method adds various buttons to the main screen for different functionalities
        like creating leagues, updating results, and visualizing leagues and standings.
        """
        top_padding = 100  # Padding at the top of the window
        button_pady = 20   # Padding around buttons

        # Create and pack a spacer frame for top padding
        top_spacer = tk.Frame(self.master, height=top_padding, bg='black')
        top_spacer.pack(side=tk.TOP, fill=tk.X)

        # Create and pack buttons for different functionalities
        boton_crear = tk.Button(self.master, text="Crear Liga", command=self.open_crear_liga, bg='white', width=50)
        boton_crear.pack(pady=button_pady)

        boton_actualizar = tk.Button(self.master, text="Actualizar Resultados", command=self.open_actualizar_resultados,
                                     bg='white', width=50)
        boton_actualizar.pack(pady=20)

        boton_visualizar = tk.Button(self.master, text="Visualizar Liga", command=self.open_visualizar_liga, bg='white',
                                     width=50)
        boton_visualizar.pack(pady=20)

        boton_clasificacion = tk.Button(self.master, text="Visualizar Clasificacion",
                                        command=self.open_visualizar_clasificacion, bg='white', width=50)
        boton_clasificacion.pack(pady=20)

        boton_clasificacion_grafico = tk.Button(self.master, text="Visualizar Gráfico Jornada a Jornada",
                                                command=self.open_visualizar_clasificacion_grafico, bg='white', width=50)
        boton_clasificacion_grafico.pack(pady=20)


    def open_crear_liga(self):
        """
        Open the 'Crear Liga' window.

        This method minimizes the main application window and opens the interface
        for creating a new football league.
        """
        self.master.iconify()  # Minimize the main window
        CrearLiga(self.master)  # Initialize and open the 'Crear Liga' window

    def open_actualizar_resultados(self):
        """
        Open the 'Actualizar Resultados' window.

        This method minimizes the main application window and opens the interface
        for updating match results in the league.
        """
        self.master.iconify()  # Minimize the main window
        ActualizarResultados(self.master)  # Initialize and open the 'Actualizar Resultados' window

    def open_visualizar_liga(self):
        """
        Open the 'Visualizar Liga' window.

        This method minimizes the main application window and opens the interface
        for viewing the current standings and results of the league.
        """
        self.master.iconify()  # Minimize the main window
        VisualizarLiga(self.master)  # Initialize and open the 'Visualizar Liga' window

    def open_visualizar_clasificacion(self):
        """
        Open the 'Visualizar Clasificacion' window.

        This method minimizes the main application window and opens the interface
        for viewing the league classification.
        """
        self.master.iconify()  # Minimize the main window
        VisualizarClasificacion(self.master)  # Initialize and open the 'Visualizar Clasificacion' window

    def open_visualizar_clasificacion_grafico(self):
        """
        Open the 'Visualizar Clasificación Gráfico' window.

        This method minimizes the main application window and opens the interface
        for viewing the graphical representation of the league classification over time.
        """
        self.master.iconify()  # Minimize the main window
        VisualizarClasificacionGrafico(self.master)  # Initialize and open the 'Visualizar Clasificación Gráfico' window

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
