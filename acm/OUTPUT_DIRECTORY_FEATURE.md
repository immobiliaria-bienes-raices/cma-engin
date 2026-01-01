# Output Directory Feature - Desktop App

## 🎯 **New Feature: Custom Output Directory Selection**

The Real Estate Analytics Desktop App now includes a **custom output directory selection** feature that allows users to choose where their results are saved.

## ✨ **What's New**

### **📁 Output Directory Section**
- **Location**: Added between "Información Básica" and "Detalles de la Propiedad" sections
- **Default Path**: `/mnt/c/Users/Asus/Downloads/` (Windows Downloads folder via WSL)
- **User Control**: Users can change the output directory at any time

### **🔧 Features**
- **Text Field**: Shows current output directory path
- **Browse Button**: "Seleccionar Carpeta" button to choose a different directory
- **Auto-Creation**: Automatically creates the directory if it doesn't exist
- **Real-time Updates**: Changes apply immediately to both property processing and CSV upload

## 🖥️ **User Interface**

### **Form Layout**
```
┌─ Información Básica ─────────────────────────┐
│ Dirección: [________________]                │
│ Operación: [VENTA ▼]                        │
└─────────────────────────────────────────────┘

┌─ Directorio de Salida ──────────────────────┐
│ Carpeta de resultados:                      │
│ [/mnt/c/Users/Asus/Downloads/] [Seleccionar]│
└─────────────────────────────────────────────┘

┌─ Detalles de la Propiedad ──────────────────┐
│ ...                                         │
└─────────────────────────────────────────────┘
```

### **How to Use**
1. **View Current Directory**: The text field shows the current output path
2. **Change Directory**: Click "Seleccionar Carpeta" to browse for a new location
3. **Process Properties**: All results will be saved to the selected directory
4. **Upload CSV**: CSV conversions will also use the selected directory

## 📊 **Technical Implementation**

### **Code Changes**
- **New Variable**: `self.output_dir_var` for GUI binding
- **New Method**: `select_output_directory()` for folder selection
- **Updated Methods**: Both `process_property()` and `process_csv()` use the selected directory
- **Auto-Creation**: `os.makedirs(self.output_dir, exist_ok=True)` ensures directory exists

### **File Path Generation**
```python
# Property processing
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
raw_filename = os.path.join(self.output_dir, f"raw_property_{timestamp}.csv")
standardized_filename = os.path.join(self.output_dir, f"standardized_property_{timestamp}.csv")

# CSV processing
output_filename = os.path.join(self.output_dir, f"standardized_{timestamp}_{base_name}.csv")
```

## 🧪 **Testing Results**

### **✅ Test Results**
- **Default Directory**: Correctly set to `/mnt/c/Users/Asus/Downloads/`
- **Directory Creation**: Automatically creates non-existent directories
- **File Generation**: Successfully creates files in selected directory
- **Path Updates**: Real-time updates when directory is changed
- **Error Handling**: Graceful handling of invalid paths

### **📋 Test Scenarios**
1. **Default Path**: Verify default path is set correctly
2. **Directory Selection**: Test folder browser functionality
3. **Path Updates**: Confirm changes apply to processing
4. **File Creation**: Verify files are saved to selected directory
5. **Error Handling**: Test with invalid/non-existent paths

## 🎯 **Benefits**

### **User Experience**
- **Flexibility**: Users can choose their preferred output location
- **Convenience**: Default path points to Windows Downloads folder
- **Organization**: Easy to organize results by project or date
- **Accessibility**: Results saved where users can easily find them

### **Technical Benefits**
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **WSL Compatible**: Default path works with Windows Subsystem for Linux
- **Error Prevention**: Auto-creation prevents "directory not found" errors
- **Consistency**: Same directory used for all processing operations

## 🚀 **Usage Examples**

### **Example 1: Default Usage**
1. Open desktop app
2. Default path shows: `/mnt/c/Users/Asus/Downloads/`
3. Fill form and process property
4. Files saved to Downloads folder

### **Example 2: Custom Directory**
1. Open desktop app
2. Click "Seleccionar Carpeta"
3. Choose: `/home/user/projects/real_estate/results/`
4. Fill form and process property
5. Files saved to custom directory

### **Example 3: Project Organization**
1. Create project folder: `/home/user/analysis_2025/`
2. Set as output directory
3. Process multiple properties
4. All results organized in one location

## 📁 **File Structure**

### **Default Output Structure**
```
/mnt/c/Users/Asus/Downloads/
├── raw_property_20250919_200114.csv
├── standardized_property_20250919_200114.csv
├── standardized_20250919_200115_example.csv
└── ...
```

### **Custom Output Structure**
```
/user/selected/directory/
├── raw_property_20250919_200114.csv
├── standardized_property_20250919_200114.csv
├── standardized_20250919_200115_example.csv
└── ...
```

## 🔧 **Configuration**

### **Default Path**
- **Windows WSL**: `/mnt/c/Users/Asus/Downloads/`
- **Linux**: Can be changed to any valid path
- **macOS**: Can be changed to any valid path

### **Path Validation**
- **Existence Check**: Automatically creates directories
- **Permission Check**: Handles permission errors gracefully
- **Path Format**: Supports both absolute and relative paths

## 🎉 **Success Metrics**

- **✅ Feature Added**: Output directory selection implemented
- **✅ Default Path**: Set to Windows Downloads folder
- **✅ User Interface**: Clean, intuitive folder selection
- **✅ Integration**: Works with both property processing and CSV upload
- **✅ Testing**: All functionality tested and working
- **✅ Documentation**: Complete usage instructions provided

The **Output Directory Feature** is now fully integrated into the desktop app, providing users with complete control over where their results are saved! 🏠📁
