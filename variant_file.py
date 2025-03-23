import re
from decimal import Decimal, ROUND_HALF_UP
from file_utils import read_excel_file

class VariantFile:
    # Define column name constants
    COL_VARIANT_FREQUENCY = 'Variant Frequency'
    COL_REFERENCE_ALLELE = 'Reference Allele'
    COL_VARIANT_ALLELE = 'Variant Allele'
    COL_DBSNP_ID = 'dbSNP ID'

    # List of all relevant columns to extract
    RELEVANT_COLUMNS = [COL_VARIANT_FREQUENCY, COL_REFERENCE_ALLELE, COL_VARIANT_ALLELE]

    def __init__(self, file):
        """
        Initialize a VariantFile object.

        Args:
            file: A file object representing the variant table file
        """
        self.file = file
        self.name = file.name
        self.data = read_excel_file(file)

        self._validate_columns()

    def _validate_columns(self):
        """
        Validate that all required columns exist in the dataframe.

        Raises:
            ValueError: If any required column is missing
        """
        missing_columns = []

        for col in self.RELEVANT_COLUMNS + [self.COL_DBSNP_ID]:
            if col not in self.data.columns:
                missing_columns.append(col)

        if missing_columns:
            raise ValueError(f"Missing required columns in variant file '{self.name}': {', '.join(missing_columns)}")

    def individual_id(self):
        """
        Extract the individual ID from the filename.

        Returns:
            str: The extracted individual ID or "Unknown" if not found
        """
        match = re.match(r'(\d+)', self.name)
        return match.group(1) if match else self.name

    def sequence_for(self, rs_id):
        """
        Get the sequence value for a given RS ID.

        Args:
            rs_id (str): The RS ID to search for

        Returns:
            str: Sequence value ("0.5", "1", or error message)
                 Empty string if RS ID not found
        """
        # Find the data for this RS ID
        rs_data = self._find_rs_data(rs_id)

        if not rs_data or self.COL_VARIANT_FREQUENCY not in rs_data:
            return ""

        # Process the variant frequency
        return self._determine_frequency_value(rs_data[self.COL_VARIANT_FREQUENCY])

    def _determine_frequency_value(self, frequency):
        """
        Determine if frequency is closer to 0.5 or 1.

        Args:
            frequency (float or str): The variant frequency

        Returns:
            str: "0.5", "1", or "ERROR" if outside valid range
        """
        try:
            # First convert to string regardless of input type
            freq_str = str(frequency)

            # Special case: if it looks like "1,000" or similar patterns that represent 1.0
            if freq_str.startswith('1') or freq_str.startswith('1'):
              return "1"

            # Normalize string representation (replace comma with period)
            freq_str = freq_str.replace(',', '.')

            freq = Decimal(freq_str)

            # Check if frequency is in valid range
            if Decimal('0') <= freq <= Decimal('1'):
                # Use rounding to determine which value it's closer to
                # Round to nearest 0.5
                rounded = (freq * 2).quantize(Decimal('1'), rounding=ROUND_HALF_UP) / 2
                return str(rounded)
            else:
                return f"ERROR (Invalid frequency: {freq})"
        except (ValueError, TypeError) as e:
            return f"ERROR: {str(e)}"

    def _find_rs_data(self, rs_id):
        """
        Find the first occurrence of the given RS ID and extract relevant column values.

        Args:
            rs_id (str): The RS ID to search for

        Returns:
            dict: Dictionary with column names as keys and their values
                  Empty dict if RS ID not found
        """
        # Convert values to string and make comparison case-insensitive
        mask = self.data[self.COL_DBSNP_ID].astype(str).str.lower() == rs_id.lower()

        # Get matching rows
        matching_rows = self.data[mask]

        if matching_rows.empty:
            return {}

        # Get just the first matching row
        first_match = matching_rows.iloc[0]

        # Extract relevant columns to dictionary
        result = {}
        for col in self.RELEVANT_COLUMNS:
            result[col] = first_match[col]

        return result
