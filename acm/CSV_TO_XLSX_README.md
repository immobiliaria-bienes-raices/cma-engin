# CSV to XLSX Parser - Well Formatted Excel Generator

This tool converts standardized CSV files to beautifully formatted XLSX files with proper headers, styling, colors, and formatting similar to the example format.

## Features

- ✅ **Professional Formatting**: Headers with colors, borders, and proper alignment
- ✅ **Auto-sizing Columns**: Automatically adjusts column widths
- ✅ **Statistics**: Calculates and displays average prices and totals
- ✅ **Header Section**: Includes title, date, address, and city
- ✅ **Footer Section**: Shows statistics and analyst information
- ✅ **Alternating Row Colors**: Easy to read data rows
- ✅ **Number Formatting**: Proper formatting for prices and areas

## Quick Start

### Option 1: Using the Activation Script (Recommended)

**Linux/Mac:**
```bash
./activate_and_convert.sh <csv_file> [output_xlsx] [property_address]
```

**Windows:**
```cmd
activate_and_convert.bat <csv_file> [output_xlsx] [property_address]
```

**Examples:**
```bash
# Basic usage (output will be same name with .xlsx extension)
./activate_and_convert.sh outputs/standardized_property.csv

# Specify output file
./activate_and_convert.sh outputs/standardized_property.csv report.xlsx

# With property address
./activate_and_convert.sh outputs/standardized_property.csv report.xlsx "Calle 123 #45-67"
```

### Option 2: Manual Activation

**Linux/Mac:**
```bash
# Activate virtual environment
source venv/bin/activate

# Install packages (first time only)
pip install pandas openpyxl

# Run converter
python csv_to_xlsx_parser.py <csv_file> -o <output.xlsx> -a "Property Address"
```

**Windows:**
```cmd
# Activate virtual environment
venv\Scripts\activate

# Install packages (first time only)
pip install pandas openpyxl

# Run converter
python csv_to_xlsx_parser.py <csv_file> -o <output.xlsx> -a "Property Address"
```

## Command Line Options

```bash
python csv_to_xlsx_parser.py <csv_file> [options]

Options:
  -o, --output    Output XLSX file path (default: same name as CSV)
  -a, --address  Property address for header
  -c, --city     City name (default: Bogotá)
  -n, --analyst  Analyst name for footer
```

## Examples

### Example 1: Basic Conversion
```bash
python csv_to_xlsx_parser.py standardized_property.csv
```
Output: `standardized_property.xlsx`

### Example 2: With Custom Output and Address
```bash
python csv_to_xlsx_parser.py standardized_property.csv \
  -o market_analysis.xlsx \
  -a "Calle 118A #13-42" \
  -c "Bogotá" \
  -n "Diana Patricia Barrera"
```

### Example 3: Using in Python Script
```python
from csv_to_xlsx_parser import CSVToXLSXParser

parser = CSVToXLSXParser()
result = parser.parse_csv_to_xlsx(
    csv_file='standardized_property.csv',
    xlsx_file='output.xlsx',
    property_address='Calle 118A #13-42',
    city='Bogotá',
    analyst_name='Analyst Name'
)

if result['success']:
    print(f"✅ Converted {result['properties_processed']} properties")
else:
    print(f"❌ Error: {result['error']}")
```

## Output Format

The generated XLSX file includes:

1. **Header Section:**
   - Title: "ACM - Análisis de Mercado Comparativo"
   - Date: Current date
   - Property Address
   - City

2. **Column Headers:**
   - Formatted headers with blue background
   - Subheaders for price and area columns

3. **Data Rows:**
   - All property data from CSV
   - Alternating row colors for readability
   - Proper number formatting

4. **Footer Section:**
   - Average price per m²
   - Analyst name and date
   - Final suggested price including administration

## Integration with Desktop App

The parser can be integrated into the desktop app workflow:

```python
from csv_to_xlsx_parser import CSVToXLSXParser

# After generating standardized CSV
parser = CSVToXLSXParser()
xlsx_result = parser.parse_csv_to_xlsx(
    csv_file=standardized_csv_file,
    xlsx_file=standardized_csv_file.replace('.csv', '.xlsx'),
    property_address=property_data['address'],
    city='Bogotá'
)
```

## Requirements

- Python 3.7+
- pandas
- openpyxl

Install with:
```bash
pip install pandas openpyxl
```

## Troubleshooting

### "Module not found" Error
- Make sure virtual environment is activated
- Install packages: `pip install pandas openpyxl`

### "CSV file not found" Error
- Check the CSV file path is correct
- Use absolute path if relative path doesn't work

### "No data found" Error
- Verify CSV file has data rows
- Check CSV file encoding (should be UTF-8)

## File Structure

```
csv_to_xlsx_parser.py          # Main parser script
activate_and_convert.sh         # Linux/Mac activation script
activate_and_convert.bat        # Windows activation script
CSV_TO_XLSX_README.md          # This file
```

