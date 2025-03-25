# Sequence Extractor

The app analyzes DNA sequence data and presents it in two different views.

Available at: https://sequence-extractor.streamlit.app/

Here's how it works:

### Input Files

1. **RS Totales File**:
   - Contains RS IDs (e.g., "rs123") and their associated data
   - Required columns: 'dbSNP ID', 'Reference Allele', 'Codigo reference allele', 'Variant Allele', 'Codigo variant allele'
   - Each RS ID appears in one row

2. **Variant Tables**:
   - Contains genotype data for each individual, showing genetic variations at each RS ID
   - Each file corresponds to one individual
   - Shows which RS IDs were found and their variant frequency

### Output Tables

The app provides two different ways to view the results:

#### 1. Codes Table (Two rows per individual)
- **Rows**: Two rows per individual - one for each allele in the pair
- **Columns**: One for each RS ID (from the RS Totales file)
- **Cells**: Contain the genetic code numbers for that position
- **Color Coding**: Uses colors to distinguish reference (blue text) from variant (red text)

#### 2. Nucleotides Table (One row per individual)
- **Rows**: One row per individual
- **Columns**: One for each RS ID (from the RS Totales file)
- **Cells**: Contain the concatenated nucleotide pairs (e.g., "GC")
- **Format**: Shows the actual nucleotides (A, C, G, T) rather than codes

### Rules for Cell Values

#### For the Codes Table:
1. **RS ID not found in the individual's data**:
   - Display the reference code in both rows (blue text)
   - Example: If reference code is "101", both rows show "101"

2. **RS ID found with frequency = 1 (homozygous for variant)**:
   - Display the variant code in both rows (red text, blue background)
   - Example: If variant code is "102", both rows show "102"

3. **RS ID found with frequency = 0.5 (heterozygous)**:
   - Display reference code in first row, variant code in second row (orange background)
   - Example: First row shows "101" (blue), second row shows "102" (red)

#### For the Nucleotides Table:
1. **RS ID not found in the individual's data**:
   - Display the reference allele twice (e.g., "GG")

2. **RS ID found with frequency = 1 (homozygous for variant)**:
   - Display the variant allele twice (e.g., "TT")

3. **RS ID found with frequency = 0.5 (heterozygous)**:
   - Display reference + variant allele (e.g., "GT")

### Color Coding (Codes Table)

The Codes Table uses colors to make patterns easier to identify:
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
