import tkinter as tk


import ActualizarResultados
import CrearLiga
import VisualizarLiga
import VisualizarClasificacion
import VisualizarClasificacionGrafico

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
        top_padding = 50  # Padding at the top of the window
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

        boton_visualizar = tk.Button(self.master, text="Visualizar Resultados", command=self.open_visualizar_liga, bg='white',
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
        crearLiga = CrearLiga
        self.master.iconify()  # Minimize the main window
        crearLiga.CrearLiga(self.master)  # Initialize and open the 'Crear Liga' window

    def open_actualizar_resultados(self):
        """
        Open the 'Actualizar Resultados' window.

        This method minimizes the main application window and opens the interface
        for updating match results in the league.
        """
        act = ActualizarResultados
        self.master.iconify()  # Minimize the main window
        act.ActualizarResultados(self.master)  # Initialize and open the 'Actualizar Resultados' window

    def open_visualizar_liga(self):
        """
        Open the 'Visualizar Liga' window.

        This method minimizes the main application window and opens the interface
        for viewing the current standings and results of the league.
        """
        vl = VisualizarLiga
        self.master.iconify()  # Minimize the main window
        vl.VisualizarLiga(self.master)  # Initialize and open the 'Visualizar Liga' window

    def open_visualizar_clasificacion(self):
        """
        Open the 'Visualizar Clasificacion' window.

        This method minimizes the main application window and opens the interface
        for viewing the league classification.
        """
        vcl = VisualizarClasificacion
        self.master.iconify()  # Minimize the main window
        vcl.VisualizarClasificacion(self.master)  # Initialize and open the 'Visualizar Clasificacion' window

    def open_visualizar_clasificacion_grafico(self):
        """
        Open the 'Visualizar Clasificación Gráfico' window.

        This method minimizes the main application window and opens the interface
        for viewing the graphical representation of the league classification over time.
        """
        graf = VisualizarClasificacionGrafico
        self.master.iconify()  # Minimize the main window
        graf.VisualizarClasificacionGrafico(self.master)  # Initialize and open the 'Visualizar Clasificación Gráfico' window

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()

