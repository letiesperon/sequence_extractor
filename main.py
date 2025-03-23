import streamlit as st
import pandas as pd
from variant_file import VariantFile
from rs_totales_file import RSTotalesFile
from translations import SPANISH as T

# Set the page to wide mode at the very beginning
st.set_page_config(
    page_title=T["app_title"],
    layout="wide"
)

def main():
    st.title(T["app_title"])

    # First input for single file
    st.subheader(T["input_files_header"])
    rs_totales_file = st.file_uploader(T["rs_totales_label"], type=["xlsx"])
    # Add hint about required columns for RS totales file
    st.caption(T["rs_totales_hint"])

    # Second input for multiple files
    variant_tables_files = st.file_uploader(T["variant_tables_label"], type=["xlsx"], accept_multiple_files=True)
    # Add hint about required columns and filename format for variant files
    st.caption(T["variant_tables_hint"])
    # Add separate hint about filename format
    st.caption(T["filename_hint"])

    # Submit button
    if st.button(T["submit_button"]):
        if rs_totales_file is None or not variant_tables_files:
            st.error(T["please_upload_error"])
        else:
            # Show spinner while processing
            with st.spinner(T["processing_spinner"]):
                try:
                    # Process the RS totales file
                    rs_file = RSTotalesFile(rs_totales_file)

                    if not rs_file.is_valid():
                        st.error(rs_file.error)
                        return

                    # Process variant files
                    variant_files = [VariantFile(file) for file in variant_tables_files]

                    # Generate statistics table and its styling
                    stats_df, case_matrix = create_statistics_table(variant_files, rs_file.rs_reference_values)

                    # Combine all dataframes for counting
                    all_dfs = [rs_file.data] + [vf.data for vf in variant_files]

                    # Display results
                    total_rows = count_total_rows(all_dfs)
                    st.success(T["processing_complete"])
                    st.metric(T["total_rows_parsed"], total_rows)

                    # Apply styling based on case matrix and display
                    st.subheader(T["stats_table_header"])
                    styled_df = style_dataframe(stats_df, case_matrix)
                    st.dataframe(styled_df, hide_index=True)

                    # Download button for CSV (unstyled)
                    csv = stats_df.to_csv(index=False)
                    st.download_button(
                        label=T["download_button"],
                        data=csv,
                        file_name="variant_files_statistics.csv",
                        mime="text/csv"
                    )

                    # Display color legend
                    st.markdown(f"""
                    ### {T["color_legend_header"]}
                    - 🔵 **{T["color_homozygous"]}**
                    - 🟠 **{T["color_heterozygous"]}**
                    - ⚪ **{T["color_reference"]}**
                    """)

                except ValueError as e:
                    st.error(T["error_processing"].format(str(e)))

def count_total_rows(dataframes):
    """Count total rows across all dataframes."""
    return sum(len(df) for df in dataframes if df is not None)

def style_dataframe(df, case_matrix):
    """
    Apply styling to the dataframe based on case matrix.

    Args:
        df: The dataframe to style
        case_matrix: Matrix with same shape as df containing case values

    Returns:
        pd.Styler: The styled dataframe
    """
    # Create a copy of the dataframe to avoid modifying the original
    styled_df = df.copy()

    # Function that will be applied to the entire dataframe to set cell background colors
    def highlight_cells(val, i, j):
        if j == 0:  # Skip styling the 'Individual' column
            return ''

        # Get column name and convert index to original row index
        col_name = styled_df.columns[j]

        # Check if this is a valid cell to style
        if col_name in case_matrix.columns and i < len(case_matrix):
            case = case_matrix.at[i, col_name]

            if case == VariantFile.CASE_HOMOZYGOUS:
                return 'background-color: #add8e6'  # Light blue
            elif case == VariantFile.CASE_HETEROZYGOUS:
                return 'background-color: #ffa500'  # Orange

        return ''

    # Create a 2D matrix of styles with the same shape as our dataframe
    style_matrix = pd.DataFrame('', index=styled_df.index, columns=styled_df.columns)

    # Fill the style matrix with appropriate background colors
    for i in range(len(styled_df)):
        for j in range(len(styled_df.columns)):
            if j > 0:  # Skip the 'Individual' column
                col_name = styled_df.columns[j]
                if i < len(case_matrix) and col_name in case_matrix.columns:
                    case = case_matrix.at[i, col_name]
                    if case == VariantFile.CASE_HOMOZYGOUS:
                        style_matrix.iloc[i, j] = 'background-color: #add8e6'  # Light blue
                    elif case == VariantFile.CASE_HETEROZYGOUS:
                        style_matrix.iloc[i, j] = 'background-color: #ffa500'  # Orange

    # Apply the style matrix to the dataframe
    return styled_df.style.apply(lambda _: style_matrix, axis=None)

def create_statistics_table(variant_files, rs_reference_values):
    """
    Create a statistics table with individual IDs and RS values as columns.
    Also create a case matrix for styling.

    Args:
        variant_files: List of VariantFile objects
        rs_reference_values: Dictionary with RS values as keys and Reference Allele values as values

    Returns:
        tuple: (stats_df, case_matrix)
    """
    # Initialize dict with Individual column
    statistics = [{"Individual": vf.individual_id()} for vf in variant_files]

    # Create the initial DataFrame
    stats_df = pd.DataFrame(statistics)

    # Create a dataframe to store cases
    case_matrix = pd.DataFrame(index=range(len(variant_files)), columns=rs_reference_values.keys())

    # For each variant file and each RS value, find the data
    for i, vf in enumerate(variant_files):
        for rs_id in rs_reference_values.keys():
            # Get the case for this RS ID
            case = vf.get_sequence_case(rs_id, rs_reference_values)
            case_matrix.at[i, rs_id] = case

            # Get the sequence value for this RS ID
            stats_df.at[i, rs_id] = vf.sequence_for(rs_id, rs_reference_values)

    return stats_df, case_matrix

if __name__ == "__main__":
    main()
