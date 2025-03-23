import streamlit as st
import pandas as pd
import time

def read_excel_file(file):
    """Read an Excel file and return the DataFrame."""
    return pd.read_excel(file)

def count_total_rows(dataframes):
    """Count total rows across all dataframes."""
    return sum(len(df) for df in dataframes if df is not None)

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
                # Read the RS totales file
                rs_df = read_excel_file(rs_totales_file)

                # Read all variant tables files
                variant_dfs = []
                for file in variant_tables_files:
                    variant_dfs.append(read_excel_file(file))

                # Combine all dataframes for counting
                all_dfs = [rs_df] + variant_dfs

                # Simulate processing time
                time.sleep(1)

            # Display results
            total_rows = count_total_rows(all_dfs)
            st.success(f"Processing complete!")
            st.metric("Total rows parsed across all files", total_rows)

if __name__ == "__main__":
    main()
