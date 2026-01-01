#!/usr/bin/env python3
"""
Real Estate Analytics Web Interface

A simple web interface for the Real Estate Analytics system.
Users can fill out property forms and get standardized CSV output.
"""

import os
import sys
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from real_estate_analytics.mappers.fincaraiz_mapper import FincaraizMapper
from real_estate_analytics.orchestrators.fincaraiz_orchestrator import FincaraizOrchestrator
from real_estate_analytics.converters.csv_converter import CSVConverter

app = Flask(__name__)
app.secret_key = 'real_estate_analytics_2025'

# Initialize components
mapper = FincaraizMapper()
orchestrator = FincaraizOrchestrator(delay_between_requests=0.5, max_retries=2)
converter = CSVConverter()

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'csv'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with property form"""
    return render_template('index.html')

@app.route('/api/process_property', methods=['POST'])
def process_property():
    """Process a single property and return results"""
    try:
        # Get form data
        property_data = {
            'address': request.form.get('address', ''),
            'operation': request.form.get('operation', 'VENTA'),
            'area_habitable': float(request.form.get('area_habitable', 0)),
            'bedrooms': int(request.form.get('bedrooms', 0)),
            'bathrooms': float(request.form.get('bathrooms', 0)),
            'stratum': int(request.form.get('stratum', 0)),
            'terrace': request.form.get('terrace') == 'true',
            'walking_closet': request.form.get('walking_closet') == 'true',
            'loft': request.form.get('loft') == 'true',
            'study_room': request.form.get('study_room') == 'true',
            'elevator': request.form.get('elevator') == 'true',
            'parking': int(request.form.get('parking', 0)),
            'deposit': int(request.form.get('deposit', 0)),
            'floor': int(request.form.get('floor', 0)),
            'construction_age': int(request.form.get('construction_age', 0)),
            'interior_exterior': request.form.get('interior_exterior', 'I'),
            'finish_quality': int(request.form.get('finish_quality', 3)),
            'conservation_state': int(request.form.get('conservation_state', 3)),
            'location_quality': int(request.form.get('location_quality', 3)),
            'observations': request.form.get('observations', ''),
            'contact_method': request.form.get('contact_method', ''),
            'contact_info': request.form.get('contact_info', ''),
            'pricing': {
                'price_per_m2': float(request.form.get('price_per_m2', 0)),
                'area': float(request.form.get('area_habitable', 0))
            }
        }
        
        # Generate search URL
        search_result = mapper.map_property_to_search(property_data)
        
        if 'error' in search_result:
            return jsonify({
                'success': False,
                'error': search_result['error']
            })
        
        search_url = search_result['search_url']
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_filename = os.path.join(OUTPUT_FOLDER, f"raw_property_{timestamp}.csv")
        standardized_filename = os.path.join(OUTPUT_FOLDER, f"standardized_property_{timestamp}.csv")
        
        # Scrape properties
        scrape_result = orchestrator.process_search_url(search_url, raw_filename)
        
        if not scrape_result['success']:
            return jsonify({
                'success': False,
                'error': f"Scraping failed: {scrape_result.get('error', 'Unknown error')}"
            })
        
        # Convert to standardized format
        convert_result = converter.convert_csv_file(raw_filename, standardized_filename)
        
        if not convert_result['success']:
            return jsonify({
                'success': False,
                'error': f"Conversion failed: {convert_result.get('error', 'Unknown error')}"
            })
        
        return jsonify({
            'success': True,
            'search_url': search_url,
            'properties_found': scrape_result['properties'],
            'converted_properties': convert_result['converted_properties'],
            'raw_file': raw_filename,
            'standardized_file': standardized_filename,
            'download_url': url_for('download_file', filename=os.path.basename(standardized_filename))
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Processing error: {str(e)}"
        })

@app.route('/api/process_csv', methods=['POST'])
def process_csv():
    """Process uploaded CSV file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            input_filename = os.path.join(UPLOAD_FOLDER, f"{timestamp}_{filename}")
            output_filename = os.path.join(OUTPUT_FOLDER, f"standardized_{timestamp}_{filename}")
            
            # Save uploaded file
            file.save(input_filename)
            
            # Convert CSV
            result = converter.convert_csv_file(input_filename, output_filename)
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'converted_properties': result['converted_properties'],
                    'conversion_rate': result['conversion_rate'],
                    'output_file': output_filename,
                    'download_url': url_for('download_file', filename=os.path.basename(output_filename))
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f"Conversion failed: {result.get('error', 'Unknown error')}"
                })
        else:
            return jsonify({'success': False, 'error': 'Invalid file type'})
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Processing error: {str(e)}"
        })

@app.route('/download/<filename>')
def download_file(filename):
    """Download generated files"""
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('File not found')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Download error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/api/schema')
def get_schema():
    """Get property schema information"""
    return jsonify({
        'required_fields': [
            'address', 'operation', 'area_habitable', 'bedrooms', 'bathrooms', 'pricing'
        ],
        'optional_fields': [
            'terrace', 'area_total', 'administration', 'parking', 'walking_closet',
            'loft', 'study_room', 'floor', 'deposit', 'terrace_area',
            'construction_age', 'interior_exterior', 'elevator', 'finish_quality',
            'conservation_state', 'location_quality', 'stratum', 'observations',
            'contact_method', 'contact_info'
        ],
        'operation_options': ['VENTA', 'ARRIENDO'],
        'interior_exterior_options': ['I', 'E'],
        'quality_scale': {'min': 1, 'max': 5},
        'stratum_scale': {'min': 1, 'max': 6}
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
