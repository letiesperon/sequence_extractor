import pandas as pd

def read_excel_file(file):
    """
    Read an Excel file and return the DataFrame.

    Args:
        file: File object to read

    Returns:
        pd.DataFrame: The data from the Excel file
    """
    return pd.read_excel(file)
