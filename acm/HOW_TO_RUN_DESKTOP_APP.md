# How to Run the Desktop App

## Quick Start

### 1. Run the Desktop Application

```bash
cd /root/work/bienes-raices/crm/acm
python3 desktop_app.py
```

This will open a graphical window with the Real Estate Analytics form.

## Testing with Address "cll 118A #13-42"

### Step-by-Step Instructions

1. **Open the Desktop App** (run the command above)

2. **Fill in the Form with the following data:**

   **Información Básica (Basic Information):**
   - Dirección: `cll 118A #13-42`
   - Operación: `VENTA`
   - Tipo de Propiedad: `Apartamento`
   - Zona (Localidad): Leave empty or select appropriate zone
   - Barrios: Leave empty

   **Detalles de la Propiedad (Property Details):**
   - Área Habitable (m²): `95`
   - Área Total (m²): `95`
   - Alcobas: `3`
   - Baños: `3`
   - Parqueaderos: `1` (or leave empty)
   - Estrato: `4`

   **Amenidades (Amenities):**
   - Check/uncheck as needed (optional)

   **Información de Precios (Pricing Information):**
   - Precio por m²: `6315789.47` (or `6315789`)
   - Administración (mensual): Leave empty or enter if known
   - Tolerancia de Precio (%): `20` (default)
   - Tolerancia de Área (%): `20` (default)
   - Fecha de publicación: `Última Semana` (default)

   **Información Adicional (Additional Information):**
   - **Edad Construcción (años): `16`** ← IMPORTANT: Enter 16 here
   - Observaciones: Leave empty

   **Directorio de Salida (Output Directory):**
   - Select a folder where you want the results saved
   - Default: `/mnt/c/Users/Asus/Downloads/` (Windows path)
   - Click "Seleccionar Carpeta" to choose a different folder

3. **Click "Procesar Propiedad"** button

4. **Check the Results Tab** to see:
   - Generated search URL
   - Number of properties found
   - Conversion status
   - File paths

5. **Output Files Generated:**
   - `raw_property_[timestamp].csv` - Raw scraped data
   - `standardized_property_[timestamp].csv` - Standardized format
   - `analisis_mercado_[timestamp].csv` - Market analysis CSV
   - `analisis_mercado_[timestamp].xlsx` - Market analysis Excel

## What Happens When You Click "Procesar Propiedad"

1. **Mapper** generates a Fincaraiz search URL with all your parameters including construction age
2. **Orchestrator** scrapes real properties from Fincaraiz matching your criteria
3. **Converter** converts the scraped data to standardized format
4. **Analysis Formatter** generates market analysis files

## Expected Search URL

The app will generate a URL like:
```
https://www.fincaraiz.com.co/venta/bogota-dc/publicado-ultimos-7-dias?
IDmoneda=4&tipo[]=apartamentos&stratum[]=4&habitaciones[]=3&banos[]=3.0
&precio_desde=598500000&precio_hasta=601500000&area_desde=95&area_hasta=95
&extras[]=con-parqueadero&antiguedad[]=De%2016%20a%2030%20a%C3%B1os
```

Notice the `antiguedad[]=De%2016%20a%2030%20a%C3%B1os` parameter which filters for properties with construction age between 16-30 years.

## Troubleshooting

- **If the app doesn't open**: Make sure you have tkinter installed (`sudo apt-get install python3-tk` on Linux)
- **If scraping fails**: Check your internet connection
- **If no properties found**: The search criteria might be too specific, try adjusting tolerances
- **Check the Results tab**: All processing logs are shown there

## Alternative: Run from Command Line

You can also test using the test script:

```bash
python3 test_address_118a.py
```

This will run the same workflow programmatically without the GUI.

