from file_utils import read_excel_file

class RSTotalesFile:
    # Define column name constants
    COL_DBSNP_ID = 'dbSNP ID'
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
        missing_columns = []
        required_columns = [self.COL_DBSNP_ID, self.COL_REFERENCE_ALLELE]

        for col in required_columns:
            if col not in self.data.columns:
                missing_columns.append(col)

        if missing_columns:
            raise ValueError(f"Missing required columns in RS totales file: {', '.join(missing_columns)}")

    def _extract_rss(self):
        """
        Extract RS values and their corresponding Reference Allele value.

        Returns:
            dict: Dictionary with RS values as keys and Reference Allele values as values
        """
        # Get the RS ID values from the dbSNP ID column
        rs_column = self.data[self.COL_DBSNP_ID].dropna()

        # Convert to string and strip whitespace
        rs_column = rs_column.astype(str).str.strip()

        # Check if all values start with "rs" (case insensitive)
        invalid_values = [val for val in rs_column if not val.lower().startswith("rs")]

        if invalid_values:
            error_message = f"Invalid RS values found in the RS totales file: {', '.join(invalid_values)}"
            return None, error_message

        # Create a dictionary with RS values as keys and Reference Allele values as values
        rs_dict = {}
        for index, rs_id in zip(rs_column.index, rs_column):
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
