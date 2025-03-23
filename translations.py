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
    "color_homozygous": "Azul: Referencia homocigota (frecuencia = 1)",
    "color_heterozygous": "Naranja: Heterocigoto (frecuencia = 0.5)",
    "color_reference": "Sin color: Solo referencia (RS no encontrado en el archivo de variantes)",

    # Error messages
    "error_processing": "Error al procesar los archivos: {}"
}
