import pandas as pd
from file_utils import read_excel_file

class RSTotalesFile:
    # Define column name constants
    COL_DBSNP_ID = 'dbSNP ID'
    COL_REFERENCE_ALLELE = 'Reference Allele'
    COL_CODIGO_REFERENCE = 'Codigo reference allele'
    COL_VARIANT_ALLELE = 'Variant Allele'
    COL_CODIGO_VARIANT = 'Codigo variant allele'

    def __init__(self, file):
        """
        Initialize an RSTotalesFile object.

        Args:
            file: A file object representing the RS totales file
        """
        self.file = file
        self.data = read_excel_file(file)
        self._validate_columns()
        self.rs_data, self.error = self._extract_rss()

    def _validate_columns(self):
        """
        Validate that all required columns exist in the dataframe.

        Raises:
            ValueError: If any required column is missing
        """
        missing_columns = []
        required_columns = [
            self.COL_DBSNP_ID,
            self.COL_REFERENCE_ALLELE,
            self.COL_CODIGO_REFERENCE,
            self.COL_VARIANT_ALLELE,
            self.COL_CODIGO_VARIANT
        ]

        for col in required_columns:
            if col not in self.data.columns:
                missing_columns.append(col)

        if missing_columns:
            raise ValueError(f"Missing required columns in RS totales file: {', '.join(missing_columns)}")

    def is_valid(self):
        """
        Check if the file has valid RS values.

        Returns:
            bool: True if the file has valid RS values, False otherwise
        """
        return self.error is None

    def _extract_rss(self):
        """
        Extract RS values and their associated data.

        Returns:
            tuple: A tuple containing:
                - rs_data: Dictionary with RS IDs as keys and all related data as values
                - error_message: String with error if any, None otherwise
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

        # Create a dictionary with RS values as keys and all data as values
        rs_data = {}

        for index, rs_id in zip(rs_column.index, rs_column):
            ref_code = self._format_code(self.data.at[index, self.COL_CODIGO_REFERENCE])
            var_code = self._format_code(self.data.at[index, self.COL_CODIGO_VARIANT])
            ref_allele = self.data.at[index, self.COL_REFERENCE_ALLELE]
            var_allele = self.data.at[index, self.COL_VARIANT_ALLELE]

            rs_data[rs_id] = {
                'ref_code': ref_code,
                'var_code': var_code,
                'ref_allele': ref_allele,
                'var_allele': var_allele
            }

        return rs_data, None

    def _format_code(self, code):
        """
        Format a code value to an integer if it's a number.

        Args:
            code: The code value to format

        Returns:
            int or str: The formatted code
        """
        try:
            # Check if the value is numeric
            if pd.notna(code) and str(code).replace('.', '', 1).isdigit():
                # Convert to integer by first removing any decimal point
                formatted_code = int(float(code))
                return formatted_code
            return code
        except:
            # If any error occurs, return the code as is
            return code
