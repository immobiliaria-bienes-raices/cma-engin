#!/bin/bash
# Activate virtual environment and convert CSV to XLSX

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found, creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
fi

# Install required packages
echo "📦 Installing required packages..."
pip install --quiet --upgrade pip
pip install --quiet pandas openpyxl

# Check if CSV file argument provided
if [ -z "$1" ]; then
    echo "Usage: $0 <csv_file> [output_xlsx_file] [property_address]"
    echo ""
    echo "Example:"
    echo "  $0 outputs/standardized_property_20250919_200114.csv"
    echo "  $0 outputs/standardized_property.csv output.xlsx 'Calle 123 #45-67'"
    exit 1
fi

CSV_FILE="$1"
OUTPUT_FILE="${2:-${CSV_FILE%.csv}.xlsx}"
ADDRESS="${3:-}"

# Run the converter
echo "🔄 Converting CSV to XLSX..."
python3 csv_to_xlsx_parser.py "$CSV_FILE" -o "$OUTPUT_FILE" ${ADDRESS:+-a "$ADDRESS"}

echo "✅ Done!"

