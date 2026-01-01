# Real Estate Analytics - Desktop Application

A simple desktop interface for the Real Estate Analytics system where users can fill out property forms and get standardized CSV output.

## 🚀 Quick Start

### Option 1: Using the launcher (Recommended)
```bash
python3 run_desktop.py
```

### Option 2: Direct execution
```bash
python3 desktop_app.py
```

## 📋 Features

### 1. Property Form Interface
- **Información Básica**: Address, operation type (Venta/Arriendo)
- **Detalles de la Propiedad**: Area, bedrooms, bathrooms, parking, stratum
- **Amenidades**: Checkboxes for terrace, elevator, walking closet, loft, study room
- **Información de Precios**: Price per m², administration fees
- **Información Adicional**: Construction age, observations

### 2. CSV Upload Interface
- Upload existing CSV files for batch processing
- Automatic conversion to standardized format
- Progress tracking and results display

### 3. Results Display
- Real-time processing logs
- Success/error messages
- File location information
- Conversion statistics

## 🎯 How to Use

### Step 1: Fill Property Form
1. Open the application
2. Go to "Formulario de Propiedad" tab
3. Fill in the required fields (marked with *)
4. Check relevant amenities
5. Click "Procesar Propiedad"

### Step 2: View Results
1. Go to "Resultados" tab
2. View processing logs
3. Check conversion statistics
4. Note the output file location

### Step 3: Process CSV Files
1. Go to "Cargar CSV" tab
2. Click "Seleccionar Archivo"
3. Choose your CSV file
4. Click "Procesar CSV"
5. View results in the Results tab

## 📁 Output Files

All generated files are saved in the `outputs/` directory:
- `raw_property_YYYYMMDD_HHMMSS.csv` - Raw scraped data
- `standardized_property_YYYYMMDD_HHMMSS.csv` - Standardized format
- `standardized_YYYYMMDD_HHMMSS_filename.csv` - Converted CSV files

## 🔧 Requirements

- Python 3.7+
- tkinter (usually included with Python)
- All dependencies from `requirements.txt`

## 📊 Example Workflow

1. **Fill Form**:
   - Address: "Calle 100 #15-20, Bogotá"
   - Operation: "Venta"
   - Area: 80 m²
   - Bedrooms: 2
   - Bathrooms: 2
   - Price per m²: 5000000

2. **Process**: Click "Procesar Propiedad"

3. **Results**:
   - Properties found: 42
   - Properties converted: 42
   - Output file: `outputs/standardized_property_20250919_193240.csv`

## 🎨 Interface Features

### Form Sections
- **Información Básica**: Core property information
- **Detalles de la Propiedad**: Physical characteristics
- **Amenidades**: Boolean amenities checkboxes
- **Información de Precios**: Financial data
- **Información Adicional**: Extra details

### Navigation
- **Tabbed Interface**: Easy navigation between functions
- **Scrollable Forms**: Handle long forms efficiently
- **Real-time Feedback**: Immediate processing updates

### Error Handling
- **Validation**: Required field checking
- **Error Messages**: Clear error descriptions
- **Progress Logging**: Step-by-step processing logs

## 🛠️ Troubleshooting

### Common Issues

1. **"tkinter not found"**
   ```bash
   sudo apt-get install python3-tkinter
   ```

2. **"Module not found"**
   ```bash
   pip install -r requirements.txt
   ```

3. **"Permission denied"**
   ```bash
   chmod +x run_desktop.py
   ```

### Debug Mode
Run with verbose output:
```bash
python3 -u desktop_app.py
```

## 📈 Performance

- **Processing Time**: ~2-3 seconds per property
- **Memory Usage**: Minimal (desktop app)
- **File Size**: Small output files
- **Compatibility**: Works on Windows, macOS, Linux

## 🔄 Workflow Summary

```
Property Form → Process → Search URL → Scrape Data → Convert → Standardized CSV
```

## 📞 Support

For issues or questions:
1. Check the Results tab for error messages
2. Verify all required fields are filled
3. Ensure internet connection for web scraping
4. Check file permissions in outputs/ directory

## 🎉 Success Indicators

- ✅ "Procesamiento completado exitosamente!" message
- ✅ Properties found count > 0
- ✅ Output file created in outputs/ directory
- ✅ No error messages in Results tab
