import streamlit as st
import pandas as pd
import io
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

    # Display file upload interface
    rs_totales_file, variant_tables_files = display_file_inputs()

    # Submit button
    if st.button(T["submit_button"]):
        if rs_totales_file is None or not variant_tables_files:
            st.error(T["please_upload_error"])
        else:
            # Process files and display results
            process_files(rs_totales_file, variant_tables_files)

def display_file_inputs():
    """Display the file upload sections and return the uploaded files"""
    # First input for single file
    st.subheader(T["input_files_header"])
    rs_totales_file = st.file_uploader(T["rs_totales_label"], type=["xlsx", "xls"])
    # Add hint about required columns for RS totales file
    st.caption(T["rs_totales_hint"])

    # Second input for multiple files
    variant_tables_files = st.file_uploader(T["variant_tables_label"], type=["xlsx", "xls"], accept_multiple_files=True)
    # Add hint about required columns and filename format for variant files
    st.caption(T["variant_tables_hint"])
    # Add separate hint about filename format
    st.caption(T["filename_hint"])

    return rs_totales_file, variant_tables_files

def process_files(rs_totales_file, variant_tables_files):
    """Process the uploaded files and display results"""
    # Show spinner while processing
    with st.spinner(T["processing_spinner"]):
        try:
            # Load and validate files
            rs_file, variant_files = load_and_validate_files(rs_totales_file, variant_tables_files)
            if rs_file is None:
                return

            # Generate data tables
            codes_table, case_matrix, code_type_matrix = create_statistics_table(variant_files, rs_file.rs_data)
            nucleotides_table, nucleotides_case_matrix = create_nucleotides_table(variant_files, rs_file.rs_data)

            # Store the nucleotides case matrix as an attribute for later use
            process_files.nucleotides_case_matrix = nucleotides_case_matrix

            # Display statistics
            all_dfs = [rs_file.data] + [vf.data for vf in variant_files]
            total_rows = count_total_rows(all_dfs)
            st.success(T["processing_complete"])
            st.metric(T["total_rows_parsed"], total_rows)

            # Create and display tabs for different views
            display_tabbed_results(codes_table, case_matrix, code_type_matrix, nucleotides_table)

        except ValueError as e:
            st.error(T["error_processing"].format(str(e)))

# Initialize the attribute to store the nucleotides case matrix
process_files.nucleotides_case_matrix = None

def load_and_validate_files(rs_totales_file, variant_tables_files):
    """Load and validate all input files"""
    # Process the RS totales file
    rs_file = RSTotalesFile(rs_totales_file)

    if not rs_file.is_valid():
        st.error(rs_file.error)
        return None, None

    # Process variant files
    variant_files = [VariantFile(file) for file in variant_tables_files]

    return rs_file, variant_files

def create_statistics_table(variant_files, rs_reference_values):
    """
    Create a statistics table with individual IDs and RS values as columns.
    Each individual has TWO rows, one for each allele.
    Also create a case matrix for styling and a code_type_matrix to track reference vs variant.

    Args:
        variant_files: List of VariantFile objects
        rs_reference_values: Dictionary with RS values as keys and allele codes as values

    Returns:
        tuple: (stats_df, case_matrix, code_type_matrix)
    """
    # Create rows for each individual (two rows per individual)
    statistics = []
    for vf in variant_files:
        # Add two rows for this individual
        individual_id = vf.individual_id()
        statistics.append({T["individual_column"]: individual_id})
        statistics.append({T["individual_column"]: individual_id})

    # Create the initial DataFrame
    stats_df = pd.DataFrame(statistics)

    # Create a dataframe to store cases (one case per individual)
    num_individuals = len(variant_files)
    case_matrix = pd.DataFrame(index=range(num_individuals * 2), columns=rs_reference_values.keys())

    # Create a dataframe to store code types (reference vs variant)
    code_type_matrix = pd.DataFrame(index=range(num_individuals * 2), columns=rs_reference_values.keys())

    # For each variant file and each RS value, find the data
    for i, vf in enumerate(variant_files):
        for rs_id in rs_reference_values.keys():
            # Get the case for this RS ID (same for both rows)
            case = vf.get_sequence_case(rs_id, rs_reference_values)

            # Set case for both rows of this individual
            case_matrix.at[i*2, rs_id] = case
            case_matrix.at[i*2+1, rs_id] = case

            # Get the sequence value for this RS ID for each position
            first_code = vf.sequence_for(rs_id, rs_reference_values, 0)
            second_code = vf.sequence_for(rs_id, rs_reference_values, 1)

            # Set values in corresponding rows - ensure they're stored as integers if numeric
            stats_df.at[i*2, rs_id] = first_code
            stats_df.at[i*2+1, rs_id] = second_code

            # Record if code is reference (True) or variant (False)
            rs_codes = rs_reference_values[rs_id]
            code_type_matrix.at[i*2, rs_id] = (first_code == rs_codes['ref_code'])
            code_type_matrix.at[i*2+1, rs_id] = (second_code == rs_codes['ref_code'])

    # Convert numeric columns to integers where appropriate
    for col in stats_df.columns:
        if col != T["individual_column"]:
            # Check if all non-null values in this column are numeric
            if stats_df[col].dropna().apply(lambda x: str(x).replace('.', '', 1).isdigit()).all():
                stats_df[col] = stats_df[col].apply(lambda x: int(float(x)) if pd.notna(x) and str(x).replace('.', '', 1).isdigit() else x)

    return stats_df, case_matrix, code_type_matrix

def create_nucleotides_table(variant_files, rs_data):
    """
    Create a table with nucleotides instead of codes, with one row per individual.
    Uses the nucleotide_pair method of VariantFile to get concatenated nucleotide pairs.

    Args:
        variant_files: List of VariantFile objects
        rs_data: Dictionary with RS IDs as keys and all related data as values

    Returns:
        tuple: (nucl_df, nuc_case_matrix) - The nucleotides table and its case matrix
    """
    # Initialize dict with Individual column
    statistics = [{T["individual_column"]: vf.individual_id()} for vf in variant_files]

    # Create the initial DataFrame
    nucl_df = pd.DataFrame(statistics)

    # Create a case matrix for styling (one case per individual)
    nuc_case_matrix = pd.DataFrame(index=range(len(variant_files)), columns=rs_data.keys())

    # For each variant file and each RS value, get the nucleotide pair and case
    for i, vf in enumerate(variant_files):
        for rs_id in rs_data.keys():
            # Get the case for this RS ID
            case = vf.get_sequence_case(rs_id, rs_data)
            nuc_case_matrix.at[i, rs_id] = case

            # Get the nucleotide pair for this RS ID
            nucl_df.at[i, rs_id] = vf.nucleotide_pair(rs_id, rs_data)

    return nucl_df, nuc_case_matrix

def count_total_rows(dataframes):
    """Count total rows across all dataframes."""
    return sum(len(df) for df in dataframes if df is not None)

def display_tabbed_results(codes_table, case_matrix, code_type_matrix, nucleotides_table):
    """Display results in tabbed interface"""
    # Create tabs for the two different views
    tab1, tab2 = st.tabs([T["codes_tab"], T["nucleotides_tab"]])

    with tab1:
        display_codes_tab(codes_table, case_matrix, code_type_matrix)

    with tab2:
        # Get the nucleotides case matrix from the nucleotides table creator
        nucleotides_case_matrix = process_files.nucleotides_case_matrix
        display_nucleotides_tab(nucleotides_table, nucleotides_case_matrix)

def display_codes_tab(codes_table, case_matrix, code_type_matrix):
    """Display the codes table tab content"""
    # Display the codes table with styling
    st.subheader(T["codes_table_header"])
    styled_codes_df = style_dataframe(codes_table, case_matrix, code_type_matrix)
    st.dataframe(styled_codes_df, hide_index=True)

    # Display download buttons
    display_download_buttons(codes_table, "variant_codes_table")

    # Display color legend
    st.markdown(f"""
    ### {T["color_legend_header"]}
    - 🔵 **{T["color_homozygous"]}**
    - 🟠 **{T["color_heterozygous"]}**
    - 🔵 **{T["color_reference_code"]}**
    - 🔴 **{T["color_variant_code"]}**
    """)

def style_dataframe(df, case_matrix, code_type_matrix):
    """
    Apply styling to the dataframe:
    - Cell text color based on reference (blue) or variant (red)
    - Background color based on homozygous/heterozygous status

    Args:
        df: The dataframe to style
        case_matrix: Matrix with case information
        code_type_matrix: Matrix with code type information (reference vs variant)

    Returns:
        pd.Styler: The styled dataframe
    """
    # Create a copy of the dataframe to avoid modifying the original
    styled_df = df.copy()

    # Create a matrix for cell styling
    style_matrix = pd.DataFrame('', index=styled_df.index, columns=styled_df.columns)

    # Fill the style matrix with appropriate styling
    for i in range(len(styled_df)):
        # Now add cell-specific styling (skipping the individual column)
        for j in range(1, len(styled_df.columns)):
            col_name = styled_df.columns[j]
            if col_name in code_type_matrix.columns:
                # Get case and code type for this cell
                if i < len(case_matrix) and i < len(code_type_matrix):
                    case = case_matrix.at[i, col_name]
                    is_reference = code_type_matrix.at[i, col_name]

                    # Set color based on reference vs variant
                    text_color = "color: blue;" if is_reference else "color: red;"

                    # Add background color based on case type
                    if case == VariantFile.CASE_HOMOZYGOUS:
                        style_matrix.iloc[i, j] = "background-color: #add8e6; " + text_color  # Light blue
                    elif case == VariantFile.CASE_HETEROZYGOUS:
                        style_matrix.iloc[i, j] = "background-color: #ffa500; " + text_color  # Orange
                    else:  # CASE_REFERENCE
                        style_matrix.iloc[i, j] = text_color

    # Apply the style matrix to the dataframe
    return styled_df.style.apply(lambda _: style_matrix, axis=None)

def display_nucleotides_tab(nucleotides_table, nucleotides_case_matrix):
    """Display the nucleotides table tab content"""
    # Display the nucleotides table with styling
    st.subheader(T["nucleotides_table_header"])

    # Apply styling to the nucleotides table
    styled_nucleotides_df = style_nucleotides_table(nucleotides_table, nucleotides_case_matrix)
    st.dataframe(styled_nucleotides_df, hide_index=True)

    # Display download buttons
    display_download_buttons(nucleotides_table, "variant_nucleotides_table")

def style_nucleotides_table(df, case_matrix):
    """
    Apply styling to the nucleotides table:
    - Background color based on homozygous/heterozygous status

    Args:
        df: The dataframe to style
        case_matrix: Matrix with case information

    Returns:
        pd.Styler: The styled dataframe
    """
    # Create a copy of the dataframe to avoid modifying the original
    styled_df = df.copy()

    # Create a matrix for cell styling
    style_matrix = pd.DataFrame('', index=styled_df.index, columns=styled_df.columns)

    # Fill the style matrix with appropriate styling
    for i in range(len(styled_df)):
        # Now add cell-specific styling (skipping the individual column)
        for j in range(1, len(styled_df.columns)):
            col_name = styled_df.columns[j]
            if col_name in case_matrix.columns:
                # Get case for this cell
                if i < len(case_matrix):
                    case = case_matrix.at[i, col_name]

                    # Add background color based on case type
                    if case == VariantFile.CASE_HOMOZYGOUS:
                        style_matrix.iloc[i, j] = "background-color: #add8e6;"  # Light blue
                    elif case == VariantFile.CASE_HETEROZYGOUS:
                        style_matrix.iloc[i, j] = "background-color: #ffa500;"  # Orange

    # Apply the style matrix to the dataframe
    return styled_df.style.apply(lambda _: style_matrix, axis=None)

def display_download_buttons(df, base_filename):
    """Display CSV and Excel download buttons for a dataframe"""
    st.write(T["download_options"])
    download_cols = st.columns([1, 1, 4])

    # CSV Download button
    csv_data = df.to_csv(index=False)
    with download_cols[0]:
        st.download_button(
            label=T["download_button_csv"],
            data=csv_data,
            file_name=f"{base_filename}.csv",
            mime="text/csv"
        )

    # Excel Download button
    excel_data = to_excel(df)
    with download_cols[1]:
        st.download_button(
            label=T["download_button_excel"],
            data=excel_data,
            file_name=f"{base_filename}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

def to_excel(df):
    """
    Convert a DataFrame to an Excel file.

    Args:
        df: The DataFrame to convert

    Returns:
        bytes: The Excel file as bytes
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Results")

    # Seek to the beginning of the stream
    output.seek(0)

    return output.getvalue()

if __name__ == "__main__":
    main()
