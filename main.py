import streamlit as st
import pandas as pd
import time
import io

def read_excel_file(file):
    """Read an Excel file and return the DataFrame."""
    return pd.read_excel(file)

def count_total_rows(dataframes):
    """Count total rows across all dataframes."""
    return sum(len(df) for df in dataframes if df is not None)

def create_statistics_table(variant_files, variant_dfs):
    """Create a statistics table with file names and row counts."""
    statistics = []
    for file, df in zip(variant_files, variant_dfs):
        statistics.append({
            "File Name": file.name,
            "Row Count": len(df)
        })
    return pd.DataFrame(statistics)

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

                # Generate statistics table
                stats_df = create_statistics_table(variant_tables_files, variant_dfs)

                # Combine all dataframes for counting
                all_dfs = [rs_df] + variant_dfs

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
