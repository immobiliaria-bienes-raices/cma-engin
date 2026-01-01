import pandas as pd
import os
import sys

def convert_excel_to_csv(excel_file_path, csv_file_path):
    """Convert an Excel file to CSV format."""
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file_path)
        
        # Save as CSV
        df.to_csv(csv_file_path, index=False)
        print(f"Successfully converted {excel_file_path} to {csv_file_path}")
        return True
    except Exception as e:
        print(f"Error converting {excel_file_path}: {str(e)}")
        return False

def main():
    # Define the examples directory
    examples_dir = "examples"
    
    # Check if the directory exists
    if not os.path.exists(examples_dir):
        print(f"Directory {examples_dir} does not exist.")
        return
    
    # Get all .xlsx files in the examples directory
    excel_files = [f for f in os.listdir(examples_dir) if f.endswith('.xlsx')]
    
    if not excel_files:
        print(f"No Excel files found in {examples_dir} directory.")
        return
    
    print(f"Found {len(excel_files)} Excel file(s) to convert.")
    
    # Convert each Excel file to CSV
    success_count = 0
    for excel_file in excel_files:
        # Create the full path for the Excel file
        excel_file_path = os.path.join(examples_dir, excel_file)
        
        # Create the CSV file name by replacing .xlsx extension with .csv
        csv_file = excel_file.replace('.xlsx', '.csv')
        csv_file_path = os.path.join(examples_dir, csv_file)
        
        # Convert the file
        if convert_excel_to_csv(excel_file_path, csv_file_path):
            success_count += 1
    
    print(f"\nConversion complete: {success_count}/{len(excel_files)} files converted successfully.")

if __name__ == "__main__":
    main()