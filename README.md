# Sequence Extractor

The app creates a table that displays DNA sequence data for each individual.

Available at: https://sequence-extractor.streamlit.app/

Here's how it works:

### Input Files

1. **RS Totales File**:
   - Contains RS IDs (e.g., "rs123") and their associated reference alleles (nucleotides at a specific position in the genome)
   - Each RS ID appears in one row

2. **Variant Tables**:
   - Contains genotype data for each individual, showing genetic variations at each RS ID
   - Each file corresponds to one individual
   - Shows how each individual's genotype at a specific RS ID differs from the reference allele

### Ouput Table

The output table shows:
- **Rows**: One for each individual (from Variant Table files)
- **Columns**: One for each RS ID (from the RS Totales file)
- **Cells**: Contain the genotype of each individual at each RS ID, represented by the actual alleles (nucleotides)

### Rules for Cell Values

For each cell, the app follows these rules:

1. **RS ID not found in the individual's data**:
   - Display the reference allele twice (e.g., "AA")

2. **RS ID found on the variant file and frequency column rounds to 1**:
   - Display the reference allele twice
   - Example: If the reference allele is "G", returns "GG"

3. **RS ID found on the variant file and frequency column rounds to 0.5**:
   - Display one reference allele and one variant allele
   - Example: If the reference allele is "T" and the variant allele is "C", returns "TC"

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
