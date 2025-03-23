# Sequence Extractor

A streamlit application for processing Excel files.

## Description

This application allows users to:
- Upload a single "RS totales" Excel file
- Upload multiple "Variant tables" Excel files
- Process these files and view statistics on the data

## Installation

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

Run tests:
```bash
pytest
```
