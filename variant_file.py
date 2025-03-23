import re
from decimal import Decimal, ROUND_HALF_UP
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

    def sequence_for(self, rs_id):
        """
        Get the sequence value for a given RS ID.

        Args:
            rs_id (str): The RS ID to search for

        Returns:
            str: Comma-separated list of sequence values ("0.5", "1", or error message)
                 Empty string if RS ID not found
        """
        # Find the data for this RS ID
        rs_data = self._find_rs_data(rs_id)

        if not rs_data:
            return ""

        # Process each result if multiple matches found
        results = []
        for _, freq in rs_data:
            results.append(self._determine_frequency_value(freq))

        # Join with commas if multiple results
        return ", ".join(results)

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
