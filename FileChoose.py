from tkinter import filedialog

class FileChoose:
    """
    A class to handle file selection.

    This class implements the Singleton pattern to minimize redundant file dialog prompts
    and clicks when working with the same file throughout the application's lifetime.
    """

    _instance = None

    def __new__(cls):
        """
        Create a new instance of FileChoose or return the existing instance.

        This method overrides the default instantiation process to ensure that only one
        instance of FileChoose is created (Singleton pattern). The first time this method
        is called, it creates a new instance and opens a file dialog for file selection.
        On subsequent calls, it returns the existing instance without opening a new file dialog.
        """
        if cls._instance is None:
            cls._instance = super(FileChoose, cls).__new__(cls)
            cls._instance.filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        return cls._instance

    def get_filepath(self):
        """
        Get the currently selected file path.

        Returns:
            str: The path of the file selected by the user. If no file has been selected,
                 or the file dialog was closed without a selection, returns an empty string.
        """
        return self.filepath

    def choose_new_file(self):
        """
        Allow the user to select a new file.

        Opens a file dialog for the user to select a new file. If a file is selected,
        updates the filepath of the instance. If the dialog is closed without a selection,
        the filepath remains unchanged.
        """
        new_filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if new_filepath:  # Ensure that the user selected a file
            self.filepath = new_filepath