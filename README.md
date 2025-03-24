# Sequence Extractor

The app creates a table that displays DNA sequence codes for each individual.

Available at: https://sequence-extractor.streamlit.app/

Here's how it works:

### Input Files

1. **RS Totales File**:
   - Contains RS IDs (e.g., "rs123") and their associated codes
   - Required columns: 'dbSNP ID', 'Reference Allele', 'Codigo reference allele', 'Variant Allele', 'Codigo variant allele'
   - Each RS ID appears in one row

2. **Variant Tables**:
   - Contains genotype data for each individual, showing genetic variations at each RS ID
   - Each file corresponds to one individual
   - Shows which RS IDs were found and their variant frequency

### Output Table

The output table shows:
- **Rows**: Two rows per individual (from Variant Table files) - one for each allele
- **Columns**: One for each RS ID (from the RS Totales file)
- **Cells**: Contain the genetic code for that position (not the nucleotide itself)

### Rules for Cell Values

For each cell, the app applies these rules:

1. **RS ID not found in the individual's data**:
   - Display the reference code in both rows (blue text)
   - Example: If reference code is "101", both rows show "101"

2. **RS ID found with frequency = 1 (homozygous for variant)**:
   - Display the variant code in both rows (red text, blue background)
   - Example: If variant code is "102", both rows show "102"

3. **RS ID found with frequency = 0.5 (heterozygous)**:
   - Display reference code in first row, variant code in second row (orange background)
   - Example: First row shows "101" (blue), second row shows "102" (red)

### Color Coding

The table uses colors to make patterns easier to identify:
- Blue text: Reference code
- Red text: Variant code
- Blue background: Homozygous variant (frequency = 1)
- Orange background: Heterozygous variant (frequency = 0.5)
- No background: Reference genotype (RS not found in variant file)

---

## Development

Developed as a streamlit application for processing Excel files.

### Requirements

- Python 3.13 or higher

### Setup with UV

Declare new dependencies:
```bash
uv add streamlit pandas openpyxl
uv add --dev pytest
```

## Usage

Run the application:
```bash
uv run -m streamlit run main.py
```

## Development

Run tests (none for now):
```bash
pytest
```
