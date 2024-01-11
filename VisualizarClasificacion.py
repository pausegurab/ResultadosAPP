import tkinter as tk
from tkinter import filedialog

import pandas as pd
import itertools
from FileChoose import FileChoose

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
        filechoose = FileChoose()
        self.file_path = filechoose.get_filepath()
        if self.file_path is None or self.file_path == '':
            self.file_path = filechoose.choose_new_file()
        if self.file_path:
            if "clasificacion" in self.file_path:
                self.file_path = self.file_path.replace('clasificacion.csv', '.csv')
            self.file_name = self.file_path.split('/')[-1].replace('.csv', '')  # Extract the file name

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

        button_x = x_left - width//4
        width_button = width //2
        self.nombre_archivo_label = tk.Label(self.master, text="Archivo:")
        self.nombre_archivo_label.place(x=0, y=10, height=10)

        # Create and position the text widget for displaying the classification
        self.texto_clasificacion = tk.Text(self.master, height=height, width=width, wrap='none')
        self.texto_clasificacion.place(x=10, y=30, width=width - 20, height=height - 60)

        # Create and position the 'Guardar clasificacion' button
        self.boton_historica = tk.Button(self.master, text="Guardar clasificacion", command=self.guardar_historica)
        self.boton_historica.place(x=button_x, y=height - 30, width=width_button, height=30)

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

            self.nombre_archivo_label.config(text=f"Archivo: {self.file_name}")

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
