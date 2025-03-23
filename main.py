import streamlit as st
import pandas as pd
import time
import io
from file_utils import read_excel_file
from variant_file import VariantFile
from rs_totales_file import RSTotalesFile

def count_total_rows(dataframes):
    """Count total rows across all dataframes."""
    return sum(len(df) for df in dataframes if df is not None)

def create_statistics_table(variant_files, rs_values):
    """
    Create a statistics table with individual IDs and RS values as columns.
    Each cell shows "0.5" or "1" based on the variant frequency.

    Args:
        variant_files: List of VariantFile objects
        rs_values: List of RS values to use as columns

    Returns:
        pd.DataFrame: Statistics table
    """
    # Initialize dict with Individual column
    statistics = [{"Individual": vf.individual_id()} for vf in variant_files]

    # Create the initial DataFrame
    stats_df = pd.DataFrame(statistics)

    # For each variant file and each RS value, find the data
    for i, vf in enumerate(variant_files):
        for rs_val in rs_values:
            # Get the sequence value for this RS ID
            stats_df.at[i, rs_val] = vf.sequence_for(rs_val)

    return stats_df

def main():
    st.title("Excel File Sequence Extractor")

    # First input for single file
    st.subheader("Input Files")
    rs_totales_file = st.file_uploader("RS totales", type=["xlsx"])

    # Second input for multiple files
    variant_tables_files = st.file_uploader("Variant tables", type=["xlsx"], accept_multiple_files=True)

    # Submit button
    if st.button("Submit"):
        if rs_totales_file is None or not variant_tables_files:
            st.error("Please upload all required files.")
        else:
            # Show spinner while processing
            with st.spinner("Processing files..."):
                # Process the RS totales file
                rs_file = RSTotalesFile(rs_totales_file)

                if not rs_file.is_valid():
                    st.error(rs_file.error)
                    return

                # Process variant files
                variant_files = [VariantFile(file) for file in variant_tables_files]

                # Generate statistics table
                stats_df = create_statistics_table(variant_files, rs_file.rs_values)

                # Combine all dataframes for counting
                all_dfs = [rs_file.data] + [vf.data for vf in variant_files]

                # Simulate processing time
                time.sleep(1)

            # Display results
            total_rows = count_total_rows(all_dfs)
            st.success(f"Processing complete!")
            st.metric("Total rows parsed across all files", total_rows)

            # Display statistics table
            st.subheader("Variant Files Statistics")
            st.dataframe(stats_df)

            # Download button for CSV
            csv = stats_df.to_csv(index=False)
            st.download_button(
                label="Download Statistics as CSV",
                data=csv,
                file_name="variant_files_statistics.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
