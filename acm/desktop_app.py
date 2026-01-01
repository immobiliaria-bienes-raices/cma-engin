#!/usr/bin/env python3
"""
Real Estate Analytics Desktop Application

A simple desktop interface for the Real Estate Analytics system.
Users can fill out property forms and get standardized CSV output.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import json
import csv
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
from real_estate_analytics.converters.csv_converter import CSVConverter
from real_estate_analytics.outputs.property_type_csv_generator import PropertyTypeCSVGenerator
from real_estate_analytics.formatters.property_type_analysis_formatter import PropertyTypeAnalysisFormatter
from csv_to_xlsx_parser import CSVToXLSXParser


class RealEstateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real Estate Analytics - Property Form")
        self.root.geometry("800x900")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.mapper = FincaraizMapper()
        self.orchestrator = FincaraizOrchestrator(delay_between_requests=0.5, max_retries=2)
        self.converter = CSVConverter()
        self.property_type_csv_generator = PropertyTypeCSVGenerator()
        self.analysis_formatter = PropertyTypeAnalysisFormatter()
        self.csv_to_xlsx_parser = CSVToXLSXParser()
        
        # Default output directory
        self.output_dir = "/mnt/c/Users/Asus/Downloads/"
        self.output_dir_var = tk.StringVar(value=self.output_dir)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Real Estate Analytics", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Property Form Tab
        self.create_property_form_tab(notebook)
        
        # CSV Upload Tab
        self.create_csv_upload_tab(notebook)
        
        # Results Tab
        self.create_results_tab(notebook)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
    
    def create_property_form_tab(self, notebook):
        # Property Form Frame
        form_frame = ttk.Frame(notebook, padding="10")
        notebook.add(form_frame, text="Formulario de Propiedad")
        
        # Create scrollable frame
        canvas = tk.Canvas(form_frame)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Basic Information Section
        basic_frame = ttk.LabelFrame(scrollable_frame, text="Información Básica", padding="10")
        basic_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(basic_frame, text="Dirección *").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.address_var = tk.StringVar()
        ttk.Entry(basic_frame, textvariable=self.address_var, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(basic_frame, text="Operación *").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.operation_var = tk.StringVar(value="VENTA")
        operation_combo = ttk.Combobox(basic_frame, textvariable=self.operation_var, 
                                      values=["VENTA", "ARRIENDO"], state="readonly")
        operation_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Property type dropdown
        ttk.Label(basic_frame, text="Tipo de Propiedad *").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.property_type_var = tk.StringVar(value="Apartamento")
        property_type_values = [
            "Casa", "Apartamento", "Apartaestudio", "Cabaña", "Casa Campestre", 
            "Casa Lote", "Finca", "Habitación", "Lote", "Bodega", "Consultorio", 
            "Local", "Oficina", "Parqueadero", "Edificio"
        ]
        property_type_combo = ttk.Combobox(basic_frame, textvariable=self.property_type_var, 
                                          values=property_type_values, state="readonly")
        property_type_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Zone dropdown
        ttk.Label(basic_frame, text="Zona (Localidad)").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.zone_var = tk.StringVar()
        zone_values = [
            "", "usaquen", "chapinero", "santa-fe", "san-cristobal", "usme", 
            "tunjuelito", "bosa", "kennedy", "fontibon", "engativa", "suba", 
            "barrios-unidos", "teusaquillo", "los-martires", "antonio-narino", 
            "puente-aranda", "candelaria", "rafael-uribe-uribe", "ciudad-bolivar", "sumapaz"
        ]
        zone_combo = ttk.Combobox(basic_frame, textvariable=self.zone_var, 
                                 values=zone_values, state="readonly")
        zone_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Neighborhood text field
        ttk.Label(basic_frame, text="Barrios (opcional)").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.neighborhoods_var = tk.StringVar()
        neighborhood_entry = ttk.Entry(basic_frame, textvariable=self.neighborhoods_var, width=50)
        neighborhood_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Help text for neighborhoods
        help_text = "Ingrese barrios separados por comas (ej: Cedritos, Niza, Zona Rosa, La Macarena)"
        ttk.Label(basic_frame, text=help_text, font=('Arial', 8), foreground='gray').grid(row=5, column=1, sticky=tk.W, pady=(0, 5))
        
        # Output Directory Section
        output_frame = ttk.LabelFrame(scrollable_frame, text="Directorio de Salida", padding="10")
        output_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(output_frame, text="Carpeta de resultados:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.output_dir_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var, width=60)
        self.output_dir_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 5))
        
        ttk.Button(output_frame, text="Seleccionar Carpeta", 
                  command=self.select_output_directory).grid(row=0, column=2, padx=5)
        
        output_frame.columnconfigure(1, weight=1)
        
        # Property Details Section
        details_frame = ttk.LabelFrame(scrollable_frame, text="Detalles de la Propiedad", padding="10")
        details_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Area and rooms
        ttk.Label(details_frame, text="Área Habitable (m²)").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.area_habitable_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.area_habitable_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(details_frame, text="Área Total (m²) *").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.area_total_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.area_total_var, width=20).grid(row=0, column=3, sticky=tk.W, pady=2)
        
        ttk.Label(details_frame, text="Alcobas").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.bedrooms_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.bedrooms_var, width=20).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(details_frame, text="Baños").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.bathrooms_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.bathrooms_var, width=20).grid(row=1, column=3, sticky=tk.W, pady=2)
        
        ttk.Label(details_frame, text="Parqueaderos").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.parking_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.parking_var, width=20).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(details_frame, text="Estrato").grid(row=2, column=2, sticky=tk.W, pady=2)
        self.stratum_var = tk.StringVar()
        stratum_combo = ttk.Combobox(details_frame, textvariable=self.stratum_var,
                                    values=["", "1", "2", "3", "4", "5", "6"], state="readonly")
        stratum_combo.grid(row=2, column=3, sticky=tk.W, pady=2)
        
        # Amenities Section
        amenities_frame = ttk.LabelFrame(scrollable_frame, text="Amenidades", padding="10")
        amenities_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.terrace_var = tk.BooleanVar()
        ttk.Checkbutton(amenities_frame, text="Terraza", variable=self.terrace_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.elevator_var = tk.BooleanVar()
        ttk.Checkbutton(amenities_frame, text="Ascensor", variable=self.elevator_var).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        self.walking_closet_var = tk.BooleanVar()
        ttk.Checkbutton(amenities_frame, text="Walking Closet", variable=self.walking_closet_var).grid(row=0, column=2, sticky=tk.W, pady=2)
        
        self.loft_var = tk.BooleanVar()
        ttk.Checkbutton(amenities_frame, text="Loft", variable=self.loft_var).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.study_room_var = tk.BooleanVar()
        ttk.Checkbutton(amenities_frame, text="Estudio/Sala TV", variable=self.study_room_var).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Pricing Section
        pricing_frame = ttk.LabelFrame(scrollable_frame, text="Información de Precios", padding="10")
        pricing_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(pricing_frame, text="Precio por m² *").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.price_per_m2_var = tk.StringVar()
        ttk.Entry(pricing_frame, textvariable=self.price_per_m2_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(pricing_frame, text="Administración (mensual)").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.administration_var = tk.StringVar()
        ttk.Entry(pricing_frame, textvariable=self.administration_var, width=20).grid(row=0, column=3, sticky=tk.W, pady=2)
        
        # Price tolerance
        ttk.Label(pricing_frame, text="Tolerancia de Precio (%)").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.price_tolerance_var = tk.StringVar(value="20")  # Default 20%
        ttk.Entry(pricing_frame, textvariable=self.price_tolerance_var, width=20).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(pricing_frame, text="(Ej: 20 = ±20% del precio)").grid(row=1, column=2, columnspan=2, sticky=tk.W, pady=2)
        
        # Area tolerance
        ttk.Label(pricing_frame, text="Tolerancia de Área (%)").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.area_tolerance_var = tk.StringVar(value="20")  # Default 20%
        ttk.Entry(pricing_frame, textvariable=self.area_tolerance_var, width=20).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(pricing_frame, text="(Ej: 20 = ±20% del área)").grid(row=2, column=2, columnspan=2, sticky=tk.W, pady=2)
        
        # Publication Date
        ttk.Label(pricing_frame, text="Fecha de publicación").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.publication_date_var = tk.StringVar(value="Indiferente")
        publication_date_values = [
            "Indiferente", "Hoy", "Desde ayer", "Última Semana", 
            "Últimos 15 días", "Últimos 30 días", "Últimos 40 días"
        ]
        publication_date_combo = ttk.Combobox(pricing_frame, textvariable=self.publication_date_var, 
                                             values=publication_date_values, state="readonly")
        publication_date_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Additional Information
        additional_frame = ttk.LabelFrame(scrollable_frame, text="Información Adicional", padding="10")
        additional_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(additional_frame, text="Edad Construcción (años)").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.construction_age_var = tk.StringVar()
        ttk.Entry(additional_frame, textvariable=self.construction_age_var, width=20).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(additional_frame, text="Observaciones").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.observations_var = tk.StringVar()
        ttk.Entry(additional_frame, textvariable=self.observations_var, width=50).grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=2)
        
        # Process Button
        process_button = ttk.Button(scrollable_frame, text="Procesar Propiedad", 
                                   command=self.process_property)
        process_button.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Configure grid weights
        form_frame.columnconfigure(0, weight=1)
        form_frame.rowconfigure(0, weight=1)
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def create_csv_upload_tab(self, notebook):
        # CSV Upload Frame
        csv_frame = ttk.Frame(notebook, padding="10")
        notebook.add(csv_frame, text="Cargar CSV")
        
        ttk.Label(csv_frame, text="Seleccionar archivo CSV para procesar:", 
                 font=('Arial', 12)).grid(row=0, column=0, pady=10)
        
        self.csv_file_var = tk.StringVar()
        ttk.Entry(csv_frame, textvariable=self.csv_file_var, width=60, state="readonly").grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(csv_frame, text="Seleccionar Archivo", 
                  command=self.select_csv_file).grid(row=1, column=1, padx=5)
        
        ttk.Button(csv_frame, text="Procesar CSV", 
                  command=self.process_csv).grid(row=2, column=0, columnspan=2, pady=20)
        
        csv_frame.columnconfigure(0, weight=1)
    
    def create_results_tab(self, notebook):
        # Results Frame
        results_frame = ttk.Frame(notebook, padding="10")
        notebook.add(results_frame, text="Resultados")
        
        self.results_text = tk.Text(results_frame, height=20, width=80, wrap=tk.WORD)
        scrollbar_results = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar_results.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_results.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        ttk.Button(results_frame, text="Limpiar Resultados", 
                  command=self.clear_results).grid(row=1, column=0, pady=10)
        
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
    
    def select_csv_file(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.csv_file_var.set(filename)
    
    def select_output_directory(self):
        """Select output directory for results"""
        directory = filedialog.askdirectory(
            title="Seleccionar carpeta para guardar resultados",
            initialdir=self.output_dir_var.get()
        )
        if directory:
            self.output_dir_var.set(directory)
            self.output_dir = directory
    
    
    def process_property(self):
        try:
            # Update output directory from form
            self.output_dir = self.output_dir_var.get()
            
            # Create output directory if it doesn't exist
            os.makedirs(self.output_dir, exist_ok=True)
            
            self.log_result(f"Directorio de salida: {self.output_dir}")
            
            # Get neighborhoods from text field
            neighborhoods_text = self.neighborhoods_var.get().strip()
            if neighborhoods_text:
                # Split by comma and clean up each neighborhood
                selected_neighborhoods = [neighborhood.strip() for neighborhood in neighborhoods_text.split(',') if neighborhood.strip()]
            else:
                selected_neighborhoods = []
            
            # Get form data
            property_data = {
                'address': self.address_var.get(),
                'operation': self.operation_var.get(),
                'property_type': self.property_type_var.get(),  # Added property type
                'zone': self.zone_var.get(),
                'neighborhoods': selected_neighborhoods,  # List of neighborhoods from text field
                'area_habitable': float(self.area_habitable_var.get() or 0) if self.area_habitable_var.get() else None,
                'area_total': float(self.area_total_var.get() or 0),
                'bedrooms': int(self.bedrooms_var.get() or 0) if self.bedrooms_var.get() else None,  # Optional, default to None
                'bathrooms': float(self.bathrooms_var.get() or 0) if self.bathrooms_var.get() else None,  # Optional, default to None
                'stratum': int(self.stratum_var.get() or 0),
                'terrace': self.terrace_var.get(),
                'walking_closet': self.walking_closet_var.get(),
                'loft': self.loft_var.get(),
                'study_room': self.study_room_var.get(),
                'elevator': self.elevator_var.get(),
                'parking': int(self.parking_var.get() or 0),
                'price_tolerance': float(self.price_tolerance_var.get() or 20),  # Added price tolerance
                'area_tolerance': float(self.area_tolerance_var.get() or 20),  # Added area tolerance
                'publication_date': self.publication_date_var.get(),  # Added publication date
                'pricing': {
                    'price_per_m2': float(self.price_per_m2_var.get() or 0),
                    'area': float(self.area_total_var.get() or 0)
                },
                'administration': float(self.administration_var.get() or 0),
                'construction_age': int(self.construction_age_var.get() or 0),
                'observations': self.observations_var.get()
            }
            
            # Validate required fields
            if not property_data['address'] or not property_data['area_total']:
                messagebox.showerror("Error", "Por favor complete todos los campos requeridos (*)")
                return
            
            self.log_result("Procesando propiedad...")
            
            # Generate search URL(s)
            search_result = self.mapper.map_property_to_search(property_data)
            
            if 'error' in search_result:
                self.log_result(f"Error al generar URL: {search_result['error']}")
                return
            
            # Check if we have multiple URLs (multiple neighborhoods)
            if 'search_urls' in search_result and len(search_result['search_urls']) > 1:
                search_urls = search_result['search_urls']
                self.log_result(f"URLs generadas para {len(search_urls)} barrios:")
                for i, url in enumerate(search_urls):
                    self.log_result(f"  {i+1}. {url}")
                
                # Generate output filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                raw_filename = os.path.join(self.output_dir, f"raw_property_multiple_{timestamp}.csv")
                standardized_filename = os.path.join(self.output_dir, f"standardized_property_multiple_{timestamp}.csv")
                
                # Scrape properties from multiple URLs
                self.log_result("Scrapeando propiedades de múltiples barrios...")
                scrape_result = self.orchestrator.process_multiple_search_urls(search_urls, raw_filename)
            else:
                # Single URL (backward compatibility)
                search_url = search_result['search_url']
                self.log_result(f"URL generada: {search_url}")
                
                # Generate output filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                raw_filename = os.path.join(self.output_dir, f"raw_property_{timestamp}.csv")
                standardized_filename = os.path.join(self.output_dir, f"standardized_property_{timestamp}.csv")
                
                # Scrape properties
                self.log_result("Scrapeando propiedades...")
                scrape_result = self.orchestrator.process_search_url(search_url, raw_filename)
            
            if not scrape_result['success']:
                self.log_result(f"Error en scraping: {scrape_result.get('error', 'Unknown error')}")
                return
            
            # Log results based on whether we used multiple URLs
            if 'urls_processed' in scrape_result:
                # Multiple URLs processed
                self.log_result(f"URLs procesadas: {scrape_result['urls_processed']}")
                self.log_result(f"URLs exitosas: {scrape_result['urls_successful']}")
                self.log_result(f"URLs fallidas: {scrape_result['urls_failed']}")
                self.log_result(f"Total propiedades encontradas: {scrape_result['total_properties']}")
            else:
                # Single URL processed
                self.log_result(f"Propiedades encontradas: {len(scrape_result['properties'])}")
            
            # Convert to property-type-specific format
            self.log_result("Convirtiendo a formato específico del tipo de propiedad...")
            
            # Determine property type for CSV generation
            property_type = property_data['property_type'].lower()
            if property_type in ['lote', 'terreno']:
                csv_type = 'lote'
            elif property_type in ['casa', 'casa campestre', 'casa lote', 'finca']:
                csv_type = 'house'
            else:
                csv_type = 'apartment'  # Default for apartments, apartaestudios, etc.
            
            # Generate property-type-specific CSV
            property_type_csv_result = self.property_type_csv_generator.generate_csv(
                scrape_result['properties'],
                standardized_filename,
                csv_type
            )
            
            if not property_type_csv_result['success']:
                self.log_result(f"Error en conversión específica: {property_type_csv_result.get('error', 'Unknown error')}")
                return
            
            self.log_result(f"Propiedades convertidas: {property_type_csv_result['properties_count']}")
            self.log_result(f"Tipo de propiedad: {property_type_csv_result['property_type']}")
            self.log_result(f"Columnas generadas: {len(property_type_csv_result['columns'])}")
            self.log_result(f"Archivo específico generado: {standardized_filename}")
            
            # Generate well-formatted XLSX file from CSV
            self.log_result("Generando archivo Excel formateado...")
            xlsx_filename = standardized_filename.replace('.csv', '.xlsx')
            xlsx_result = self.csv_to_xlsx_parser.parse_csv_to_xlsx(
                csv_file=standardized_filename,
                xlsx_file=xlsx_filename,
                property_address=property_data['address'],
                city="Bogotá",
                analyst_name=None
            )
            
            if xlsx_result['success']:
                self.log_result(f"✅ Archivo Excel generado: {xlsx_filename}")
                self.log_result(f"   Propiedades procesadas: {xlsx_result['properties_processed']}")
            else:
                self.log_result(f"⚠️  Advertencia: No se pudo generar Excel: {xlsx_result.get('error', 'Unknown error')}")
            
            # Also generate the old standardized format for backward compatibility
            self.log_result("Generando formato estandarizado adicional...")
            old_standardized_filename = standardized_filename.replace('.csv', '_old_format.csv')
            convert_result = self.converter.convert_csv_file(raw_filename, old_standardized_filename)
            
            if convert_result['success']:
                self.log_result(f"Archivo estandarizado adicional: {old_standardized_filename}")
            else:
                self.log_result(f"Advertencia: No se pudo generar formato estandarizado adicional")
            
            # Create market analysis files
            self.log_result("Generando análisis de mercado...")
            analysis_base_filename = f"analisis_mercado_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Read the standardized properties for analysis
            properties_for_analysis = []
            try:
                with open(standardized_filename, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    properties_for_analysis = list(reader)
                self.log_result(f"Propiedades leídas para análisis: {len(properties_for_analysis)}")
                if properties_for_analysis:
                    self.log_result(f"Primera propiedad: {list(properties_for_analysis[0].keys())}")
            except Exception as e:
                self.log_result(f"Error leyendo propiedades estandarizadas: {str(e)}")
                properties_for_analysis = []
            
            # Create analysis files
            analysis_result = self.analysis_formatter.format_analysis_files(
                properties_for_analysis,
                property_data['address'],
                self.output_dir,
                analysis_base_filename,
                "Bogotá",
                csv_type  # Pass the property type for proper formatting
            )
            
            if analysis_result['success']:
                self.log_result(f"Análisis CSV generado: {analysis_result['csv_file']}")
                self.log_result(f"Análisis Excel generado: {analysis_result['excel_file']}")
                self.log_result(f"Precio promedio calculado: ${analysis_result['average_price']:,.0f}")
            else:
                error_msg = analysis_result.get('error', 'Unknown error')
                csv_error = analysis_result.get('csv_error', '')
                excel_error = analysis_result.get('excel_error', '')
                self.log_result(f"Error generando análisis: {error_msg}")
                if csv_error:
                    self.log_result(f"  CSV Error: {csv_error}")
                if excel_error:
                    self.log_result(f"  Excel Error: {excel_error}")
            
            self.log_result("¡Procesamiento completado exitosamente!")
            
            # Show success message
            success_message = "Procesamiento completado!\n\n"
            if 'urls_processed' in scrape_result:
                success_message += f"Barrios procesados: {scrape_result['urls_successful']}/{scrape_result['urls_processed']}\n"
                success_message += f"Propiedades encontradas: {scrape_result['total_properties']}\n"
            else:
                success_message += f"Propiedades encontradas: {len(scrape_result['properties'])}\n"
            
            success_message += f"\nArchivos generados:\n"
            success_message += f"• Estandarizado CSV: {os.path.basename(standardized_filename)}\n"
            # Add XLSX file if generated
            xlsx_filename = standardized_filename.replace('.csv', '.xlsx')
            if os.path.exists(xlsx_filename):
                success_message += f"• Excel Formateado: {os.path.basename(xlsx_filename)}\n"
            if analysis_result['success']:
                success_message += f"• Análisis CSV: {os.path.basename(analysis_result['csv_file'])}\n"
                success_message += f"• Análisis Excel: {os.path.basename(analysis_result['excel_file'])}\n"
                success_message += f"• Precio promedio: ${analysis_result['average_price']:,.0f}"
            
            messagebox.showinfo("Éxito", success_message)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.log_result(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def process_csv(self):
        try:
            csv_file = self.csv_file_var.get()
            if not csv_file:
                messagebox.showerror("Error", "Por favor seleccione un archivo CSV")
                return
            
            # Update output directory from form
            self.output_dir = self.output_dir_var.get()
            
            # Create output directory if it doesn't exist
            os.makedirs(self.output_dir, exist_ok=True)
            
            self.log_result(f"Procesando archivo: {csv_file}")
            self.log_result(f"Directorio de salida: {self.output_dir}")
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(os.path.basename(csv_file))[0]
            output_filename = os.path.join(self.output_dir, f"standardized_{timestamp}_{base_name}.csv")
            
            # Convert CSV
            result = self.converter.convert_csv_file(csv_file, output_filename)
            
            if result['success']:
                self.log_result(f"Conversión exitosa!")
                self.log_result(f"Propiedades convertidas: {result['converted_properties']}")
                self.log_result(f"Tasa de conversión: {result['conversion_rate']:.2%}")
                self.log_result(f"Archivo estandarizado generado: {output_filename}")
                
                # Generate well-formatted XLSX file from CSV
                self.log_result("Generando archivo Excel formateado...")
                xlsx_filename = output_filename.replace('.csv', '.xlsx')
                xlsx_result = self.csv_to_xlsx_parser.parse_csv_to_xlsx(
                    csv_file=output_filename,
                    xlsx_file=xlsx_filename,
                    property_address="Propiedades CSV",
                    city="Bogotá",
                    analyst_name=None
                )
                
                if xlsx_result['success']:
                    self.log_result(f"✅ Archivo Excel generado: {xlsx_filename}")
                    self.log_result(f"   Propiedades procesadas: {xlsx_result['properties_processed']}")
                else:
                    self.log_result(f"⚠️  Advertencia: No se pudo generar Excel: {xlsx_result.get('error', 'Unknown error')}")
                
                # Create market analysis files
                self.log_result("Generando análisis de mercado...")
                analysis_base_filename = f"analisis_mercado_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Read the standardized properties for analysis
                properties_for_analysis = []
                try:
                    with open(output_filename, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        properties_for_analysis = list(reader)
                    self.log_result(f"Propiedades leídas para análisis: {len(properties_for_analysis)}")
                    if properties_for_analysis:
                        self.log_result(f"Primera propiedad: {list(properties_for_analysis[0].keys())}")
                except Exception as e:
                    self.log_result(f"Error leyendo propiedades estandarizadas: {str(e)}")
                    properties_for_analysis = []
                
                # Create analysis files
                analysis_result = self.analysis_formatter.format_analysis_files(
                    properties_for_analysis,
                    "Propiedades CSV",  # Generic address for CSV uploads
                    self.output_dir,
                    analysis_base_filename,
                    "Bogotá"
                )
                
                if analysis_result['success']:
                    self.log_result(f"Análisis CSV generado: {analysis_result['csv_file']}")
                    self.log_result(f"Análisis Excel generado: {analysis_result['excel_file']}")
                    self.log_result(f"Precio promedio calculado: ${analysis_result['average_price']:,.0f}")
                else:
                    error_msg = analysis_result.get('error', 'Unknown error')
                    csv_error = analysis_result.get('csv_error', '')
                    excel_error = analysis_result.get('excel_error', '')
                    self.log_result(f"Error generando análisis: {error_msg}")
                    if csv_error:
                        self.log_result(f"  CSV Error: {csv_error}")
                    if excel_error:
                        self.log_result(f"  Excel Error: {excel_error}")
                
                # Show success message
                success_message = f"Conversión completada!\nPropiedades convertidas: {result['converted_properties']}\n\nArchivos generados:\n• Estandarizado CSV: {os.path.basename(output_filename)}"
                # Add XLSX file if generated
                xlsx_filename = output_filename.replace('.csv', '.xlsx')
                if os.path.exists(xlsx_filename):
                    success_message += f"\n• Excel Formateado: {os.path.basename(xlsx_filename)}"
                if analysis_result['success']:
                    success_message += f"\n• Análisis CSV: {os.path.basename(analysis_result['csv_file'])}\n• Análisis Excel: {os.path.basename(analysis_result['excel_file'])}\n• Precio promedio: ${analysis_result['average_price']:,.0f}"
                
                messagebox.showinfo("Éxito", success_message)
            else:
                error_msg = f"Error en conversión: {result.get('error', 'Unknown error')}"
                self.log_result(error_msg)
                messagebox.showerror("Error", error_msg)
                
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.log_result(error_msg)
            messagebox.showerror("Error", error_msg)
    
    def log_result(self, message):
        self.results_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def clear_results(self):
        self.results_text.delete(1.0, tk.END)


def main():
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
