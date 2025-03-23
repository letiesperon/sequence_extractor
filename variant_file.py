import re
from file_utils import read_excel_file

class VariantFile:
    def __init__(self, file):
        """
        Initialize a VariantFile object.

        Args:
            file: A file object representing the variant table file
        """
        self.file = file
        self.name = file.name
        self.data = read_excel_file(file)

    def individual_id(self):
        """
        Extract the individual ID from the filename.

        Returns:
            str: The extracted individual ID or "Unknown" if not found
        """
        match = re.match(r'(\d+)', self.name)
        return match.group(1) if match else self.name

    def find_rs_data(self, rs_id):
        """
        Find row numbers and variant frequencies where the given RS ID appears.

        Args:
            rs_id (str): The RS ID to search for

        Returns:
            list: List of tuples (row_number, variant_frequency) where the RS ID is found
        """
        # Try to find the dbSNP ID column
        if 'dbSNP ID' in self.data.columns:
            id_column = 'dbSNP ID'
        # If not found by name, use column H (index 7 in 0-based indexing)
        elif len(self.data.columns) > 7:
            id_column = self.data.columns[7]
        else:
            return []

        # Try to find the Variant Frequency column
        if 'Variant Frequency' in self.data.columns:
            freq_column = 'Variant Frequency'
        # If not found by name, use column M (index 12 in 0-based indexing)
        elif len(self.data.columns) > 12:
            freq_column = self.data.columns[12]
        else:
            return []

        # Convert values to string and make comparison case-insensitive
        mask = self.data[id_column].astype(str).str.lower() == rs_id.lower()

        # Get matching rows
        matching_rows = self.data[mask]

        # Return list of tuples (row_number, variant_frequency)
        return [(idx + 1, freq) for idx, freq in zip(matching_rows.index, matching_rows[freq_column])]
