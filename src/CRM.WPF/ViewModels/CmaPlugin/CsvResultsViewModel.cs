// ViewModel for displaying CSV results in a DataGrid

#nullable enable

using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.Dynamic;
using System.Globalization;
using System.IO;
using System.Runtime.CompilerServices;
using System.Windows.Input;

namespace CRM.WPF.ViewModels.CmaPlugin;

/// <summary>
/// ViewModel for displaying CSV analysis results.
/// Loads and parses CSV data for display in a DataGrid.
/// </summary>
public class CsvResultsViewModel : INotifyPropertyChanged
{
    private string _csvFilePath = string.Empty;
    private string _subjectAddress = string.Empty;
    private string _operation = string.Empty;
    private int _propertyCount;
    private DateTime _generatedAt;
    private ObservableCollection<dynamic> _properties = new();

    public CsvResultsViewModel()
    {
        OpenCsvCommand = new RelayCommand(ExecuteOpenCsv);
        ExportToExcelCommand = new RelayCommand(ExecuteExportToExcel, CanExecuteExportToExcel);
        CloseCommand = new RelayCommand(ExecuteClose);
    }

    public string CsvFilePath
    {
        get => _csvFilePath;
        set => SetProperty(ref _csvFilePath, value);
    }

    public string SubjectAddress
    {
        get => _subjectAddress;
        set => SetProperty(ref _subjectAddress, value);
    }

    public string Operation
    {
        get => _operation;
        set => SetProperty(ref _operation, value);
    }

    public int PropertyCount
    {
        get => _propertyCount;
        set => SetProperty(ref _propertyCount, value);
    }

    public DateTime GeneratedAt
    {
        get => _generatedAt;
        set => SetProperty(ref _generatedAt, value);
    }

    public ObservableCollection<dynamic> Properties
    {
        get => _properties;
        set => SetProperty(ref _properties, value);
    }

    public ICommand OpenCsvCommand { get; }
    public ICommand ExportToExcelCommand { get; }
    public ICommand CloseCommand { get; }

    public event EventHandler? CloseRequested;
    public event PropertyChangedEventHandler? PropertyChanged;

    /// <summary>
    /// Loads CSV data from the specified file path.
    /// </summary>
    public void LoadCsvData(string csvFilePath, string subjectAddress, string operation)
    {
        CsvFilePath = csvFilePath;
        SubjectAddress = subjectAddress;
        Operation = operation;
        GeneratedAt = DateTime.Now;

        if (!File.Exists(csvFilePath))
        {
            throw new FileNotFoundException($"CSV file not found: {csvFilePath}");
        }

        var lines = File.ReadAllLines(csvFilePath);
        if (lines.Length == 0)
        {
            PropertyCount = 0;
            return;
        }

        // Parse CSV header
        var headers = lines[0].Split(',');

        // Parse data rows
        var dataRows = new ObservableCollection<dynamic>();
        for (int i = 1; i < lines.Length; i++)
        {
            var values = lines[i].Split(',');
            if (values.Length != headers.Length)
                continue; // Skip malformed rows

            var row = new ExpandoObject() as IDictionary<string, object>;
            for (int j = 0; j < headers.Length; j++)
            {
                row[headers[j]] = values[j];
            }
            dataRows.Add(row);
        }

        Properties = dataRows;
        PropertyCount = dataRows.Count;
    }

    private void ExecuteOpenCsv(object? parameter)
    {
        if (File.Exists(CsvFilePath))
        {
            // Open with default CSV application
            Process.Start(new ProcessStartInfo
            {
                FileName = CsvFilePath,
                UseShellExecute = true
            });
        }
    }

    private bool CanExecuteExportToExcel(object? parameter)
    {
        // TODO: Implement Excel export
        return false;
    }

    private void ExecuteExportToExcel(object? parameter)
    {
        // TODO: Implement Excel export using ClosedXML
    }

    private void ExecuteClose(object? parameter)
    {
        CloseRequested?.Invoke(this, EventArgs.Empty);
    }

    protected virtual void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }

    protected bool SetProperty<T>(ref T field, T value, [CallerMemberName] string? propertyName = null)
    {
        if (EqualityComparer<T>.Default.Equals(field, value))
            return false;

        field = value;
        OnPropertyChanged(propertyName);
        return true;
    }

    private class RelayCommand : ICommand
    {
        private readonly Action<object?> _execute;
        private readonly Func<object?, bool>? _canExecute;

        public RelayCommand(Action<object?> execute, Func<object?, bool>? canExecute = null)
        {
            _execute = execute ?? throw new ArgumentNullException(nameof(execute));
            _canExecute = canExecute;
        }

        public event EventHandler? CanExecuteChanged;

        public bool CanExecute(object? parameter)
        {
            return _canExecute?.Invoke(parameter) ?? true;
        }

        public void Execute(object? parameter)
        {
            _execute(parameter);
        }
    }
}
