import os
from pathlib import Path

class DocsDirHandler():
    """
    """
    def __init__(self, dir=None, file=None):
        """Initialize the DocsDirHandler with a directory and a file.

        Parameters:
            dir (str, optional): The name of the directory. Defaults to None.
            file (str, optional): The name of the file. Defaults to None.
        """
        self.dir = dir
        self.file = file
        self.fs_path = self.createValidateDir(dir)

    def createValidateDir(self, directory):
        """Create and validate the directory.

        Parameters:
            directory (str): The name of the directory.

        Returns:
            str: The absolute path of the directory.
        """
        dir_path = self.dirPath(directory)
        if not Path(dir_path).is_dir():
            os.mkdir(dir_path)
        return dir_path
    
    def dirPath(self, directory):
        """Get the absolute path of the directory.

        Parameters:
            directory (str): The name of the directory.

        Returns:
            str: The absolute path of the directory.
        """
        return os.path.abspath(directory)
