"""
Translations for the Sequence Extractor application.
"""

# Dictionary of strings in Spanish
SPANISH = {
    # Main UI elements
    "app_title": "Extractor de Secuencias",
    "input_files_header": "Archivos de Entrada",
    "rs_totales_label": "Archivo RS totales",
    "variant_tables_label": "Tablas de variantes",
    "submit_button": "Procesar",
    "please_upload_error": "Carga todos los archivos requeridos.",
    "processing_spinner": "Procesando archivos...",
    "processing_complete": "Procesamiento completado!",
    "total_rows_parsed": "Filas totales procesadas",
    "stats_table_header": "Estadísticas de Variantes",
    "download_button": "Descargar como CSV",

    # Input hints
    "rs_totales_hint": """📋 Este archivo debe contener las siguientes columnas:
    - 'dbSNP ID'
    - 'Reference Allele'""",

    "variant_tables_hint": """📋 Estos archivos deben contener las siguientes columnas:
    - 'dbSNP ID'
    - 'Variant Frequency'
    - 'Reference Allele'
    - 'Variant Allele'""",

    "filename_hint": "📋 El nombre de cada archivo debe contener un identificador del individuo numérico (ej. '73-variant-table.xlsx' significa individuo 73)",

    # Color legend
    "color_legend_header": "Leyenda de Colores",
    "color_homozygous": "Azul claro: Homocigoto (frecuencia = 1)",
    "color_heterozygous": "Naranja claro: Heterocigoto (frecuencia = 0.5)",
    "color_reference_code": "Texto azul: Código de referencia",
    "color_variant_code": "Texto rojo: Código de variante",

    # Column headers
    "column_headers_expander": "Mostrar IDs de RS (para copiar)",
    "column_headers_title": "Haz clic en cualquier ID para seleccionarlo y copiarlo:",

    # Table column names
    "individual_column": "Individuo",

    # Error messages
    "error_processing": "Error al procesar los archivos: {}",

    # Download options
    "download_options": "Descargar resultados:",
    "download_button_csv": "Descargar como CSV",
    "download_button_excel": "Descargar como Excel"
}
