from charset_normalizer import detect


class DocChecker:
    """
    A class for checking a markdown file for common errors.

    :param file_path: A string representing the path of the file being checked.
    :type file_path: str
    :param file_display_path: A string representing the path of the file being checked for display purpose only, can be empty.
    :type file_display_path: str
    """

    def __init__(self, file_path: str, file_display_path: str):
        with open(file_path, 'rb') as f:
            file_data = f.read()
        if file_display_path:
            self.display_path = file_display_path
        else:
            self.display_path = file_path
        self.data = file_data
        self.pass_carriage_return = None
        self.pass_encoding = None

    def __repr__(self):
        return f"{{\"display_path\": {self.display_path}, \"pass_carriage_return\": {self.pass_carriage_return}, \"pass_encoding\": {self.pass_encoding}}}"

    def __str__(self):
        return f"{self.display_path}    {self.pass_carriage_return}    {self.pass_encoding}"

    def validate_carriage_return(self) -> bool:
        """
        Check the carriage return in the file content and print a warning message if not correct.
        """
        if b'\r' in self.data:
            print(f"WARNING: Please change carriage return to LF for the file '{self.display_path}'")
            self.pass_carriage_return = False
            return False
        self.pass_carriage_return = True
        return True

    def validate_encoding(self) -> bool:
        """
        Detect the encoding of the file content and print a warning message if it is not UTF-8 or ASCII.
        """
        encoding = detect(self.data).get('encoding')
        if encoding != 'utf-8' and encoding != 'ascii':
            print(f"WARNING: Please convert to utf-8 encoding for the file '{self.display_path}'")
            self.pass_encoding = False
            return False
        self.pass_encoding = True
        return True
