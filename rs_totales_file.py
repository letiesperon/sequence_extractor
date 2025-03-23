from file_utils import read_excel_file

class RSTotalesFile:
    def __init__(self, file):
        """
        Initialize an RSTotalesFile object.

        Args:
            file: A file object representing the RS totales file
        """
        self.file = file
        self.data = read_excel_file(file)
        self.rs_values, self.error = self._extract_rs_values()

    def _extract_rs_values(self):
        """
        Extract RS values from the first column of the file.

        Returns:
            (list, str): A tuple containing either:
                - (rs_values, None) if all values are valid
                - (None, error_message) if invalid values are found
        """
        # Get the first column values, skipping the header (first row)
        first_column = self.data.iloc[1:, 0]

        # Convert to string and strip whitespace
        first_column = first_column.astype(str).str.strip()

        # Check if all values start with "rs" (case insensitive)
        invalid_values = [val for val in first_column if not val.lower().startswith("rs")]

        if invalid_values:
            error_message = f"Invalid RS values found in the RS totales file: {', '.join(invalid_values)}"
            return None, error_message

        return first_column.tolist(), None

    def is_valid(self):
        """
        Check if the file has valid RS values.

        Returns:
            bool: True if the file has valid RS values, False otherwise
        """
        return self.error is None
