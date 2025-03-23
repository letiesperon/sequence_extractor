from file_utils import read_excel_file

class RSTotalesFile:
    # Define column name constants
    COL_RS_ID = 'RS ID'
    COL_REFERENCE_ALLELE = 'Reference Allele'

    def __init__(self, file):
        """
        Initialize an RSTotalesFile object.

        Args:
            file: A file object representing the RS totales file
        """
        self.file = file
        self.data = read_excel_file(file)
        self._validate_columns()
        self.rs_reference_values, self.error = self._extract_rss()

    def _validate_columns(self):
        """
        Validate that all required columns exist in the dataframe.

        Raises:
            ValueError: If any required column is missing
        """
        # Check if the Reference Allele column exists
        if self.COL_REFERENCE_ALLELE not in self.data.columns:
            raise ValueError(f"Missing required column '{self.COL_REFERENCE_ALLELE}' in RS totales file")

    def _extract_rss(self):
        """
        Extract RS values and their corresponding Reference Allele value.

        Returns:
            dict: Dictionary with RS values as keys and Reference Allele values as values
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

        # Create a dictionary with RS values as keys and Reference Allele values as values
        rs_dict = {}
        for index, rs_id in zip(first_column.index, first_column):
            reference_allele = self.data.at[index, self.COL_REFERENCE_ALLELE]
            rs_dict[rs_id] = reference_allele

        return rs_dict, None

    def is_valid(self):
        """
        Check if the file has valid RS values.

        Returns:
            bool: True if the file has valid RS values, False otherwise
        """
        return self.error is None
