import re
from decimal import Decimal, ROUND_HALF_UP
from file_utils import read_excel_file

class VariantFile:
    # Define column name constants
    COL_VARIANT_FREQUENCY = 'Variant Frequency'
    COL_REFERENCE_ALLELE = 'Reference Allele'
    COL_VARIANT_ALLELE = 'Variant Allele'
    COL_DBSNP_ID = 'dbSNP ID'

    # Case constants for coloring
    CASE_HOMOZYGOUS = "HOMOZYGOUS"  # frequency = 1
    CASE_HETEROZYGOUS = "HETEROZYGOUS"  # frequency = 0.5
    CASE_REFERENCE = "REFERENCE"  # RS not found in variant file

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

    def get_sequence_case(self, rs_id, rs_data):
        """
        Determine which case applies for a given RS ID.

        Args:
            rs_id (str): The RS ID to search for
            rs_data (dict): Dictionary with RS ID data

        Returns:
            str: One of the case constants
        """
        # Find the data for this RS ID
        variant_data = self._find_variant_data(rs_id)

        # If the RS ID is not found in the variant file
        if not variant_data:
            return self.CASE_REFERENCE

        # Process the variant frequency
        frequency_value = self._determine_frequency_value(variant_data[self.COL_VARIANT_FREQUENCY])

        # Determine case based on frequency
        if frequency_value == "1":
            return self.CASE_HOMOZYGOUS
        elif frequency_value == "0.5":
            return self.CASE_HETEROZYGOUS
        else:
            # For error cases, treat as reference
            return self.CASE_REFERENCE

    def sequence_for(self, rs_id, rs_reference_values, position):
        """
        Get the code value for a given RS ID at the specified position.

        Args:
            rs_id (str): The RS ID to search for
            rs_reference_values (dict): Dictionary with RS ID data
            position (int): Which position to return (0 for first allele, 1 for second)

        Returns:
            int/str: Code value for the specified position
        """
        return self.code_for_position(rs_id, rs_reference_values, position)

    def code_for_position(self, rs_id, rs_data, position):
        """
        Get the code value for a given RS ID at the specified position.

        Args:
            rs_id (str): The RS ID to search for
            rs_data (dict): Dictionary with RS ID data
            position (int): Which position to return (0 for first allele, 1 for second)

        Returns:
            int/str: Code value for the specified position
        """
        # Find the data for this RS ID
        variant_data = self._find_variant_data(rs_id)

        # Get the codes for this RS
        ref_code = rs_data[rs_id]['ref_code']
        var_code = rs_data[rs_id]['var_code']

        # If the RS ID is not found in the variant file,
        # return the reference code for both positions
        if not variant_data:
            return ref_code

        # Process the variant frequency
        frequency_value = self._determine_frequency_value(variant_data[self.COL_VARIANT_FREQUENCY])

        # If frequency is 1, return variant code for both positions
        if frequency_value == "1":
            return var_code

        # If frequency is 0.5, return ref code for position 0, variant code for position 1
        if frequency_value == "0.5":
            if position == 0:
                return ref_code
            else:
                return var_code

        # Return error message for unexpected cases
        return frequency_value  # This will be the error message

    def nucleotide_pair(self, rs_id, rs_data):
        """
        Get the concatenated nucleotide pair for a given RS ID.

        Args:
            rs_id (str): The RS ID to search for
            rs_data (dict): Dictionary with RS ID data

        Returns:
            str: Concatenated nucleotide pair
        """
        # Find the data for this RS ID
        variant_data = self._find_variant_data(rs_id)

        # Get the nucleotides for this RS
        ref_allele = rs_data[rs_id]['ref_allele']
        var_allele = rs_data[rs_id]['var_allele']

        # If the RS ID is not found in the variant file,
        # return the reference allele duplicated
        if not variant_data:
            return f"{ref_allele}{ref_allele}"

        # Process the variant frequency
        frequency_value = self._determine_frequency_value(variant_data[self.COL_VARIANT_FREQUENCY])

        # If frequency is 1, return variant allele duplicated
        if frequency_value == "1":
            return f"{var_allele}{var_allele}"

        # If frequency is 0.5, return reference + variant allele
        if frequency_value == "0.5":
            return f"{ref_allele}{var_allele}"

        # Return error message for unexpected cases
        return frequency_value  # This will be the error message

    def _find_variant_data(self, rs_id):
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
