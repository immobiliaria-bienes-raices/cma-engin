// TDD PHASE: GREEN
// ViewModel implementation following MVVM pattern
// All properties implement INotifyPropertyChanged for WPF data binding

#nullable enable

using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;
using CRM.Domain.ValueObjects;
using CRM.Application.CmaPlugin.Services;
using CRM.Application.CmaPlugin.Dtos;

namespace CRM.WPF.ViewModels.CmaPlugin;

/// <summary>
/// ViewModel for the property input form.
/// Handles validation, commands, and data binding.
/// </summary>
public class PropertyFormViewModel : INotifyPropertyChanged
{
    private readonly CmaOrchestrator? _orchestrator;
    private string? _address;
    private string _operation = "ARRIENDO"; // Default to rent
    private decimal? _areaHabitable;
    private int? _bedrooms;
    private decimal? _bathrooms;
    private decimal? _pricePerM2;
    private decimal? _areaTotal;
    private int _parking;
    private int? _stratum;
    private int? _floor;
    private int? _constructionAge;
    private decimal? _administration;
    private bool _terrace;
    private bool _elevator;
    private bool _walkingCloset;
    private bool _loft;
    private bool _studyRoom;
    private int _deposit;
    private string? _interiorExterior;
    private int? _finishQuality;
    private int? _conservationState;
    private int? _locationQuality;
    private string? _observations;
    private bool _isBusy;
    private List<string> _validationErrors = new();

    // Parameterless constructor for XAML designer
    public PropertyFormViewModel() : this(null)
    {
    }

    // Constructor with dependency injection
    public PropertyFormViewModel(CmaOrchestrator? orchestrator)
    {
        _orchestrator = orchestrator;
        SubmitCommand = new RelayCommand(async (param) => await ExecuteSubmitAsync(), CanExecuteSubmit);
        ClearCommand = new RelayCommand(ExecuteClear);
    }

    // Required Properties
    public string? Address
    {
        get => _address;
        set
        {
            if (SetProperty(ref _address, value))
            {
                ValidateForm();
            }
        }
    }

    public string Operation
    {
        get => _operation;
        set
        {
            if (SetProperty(ref _operation, value))
            {
                ValidateForm();
            }
        }
    }

    public decimal? AreaHabitable
    {
        get => _areaHabitable;
        set
        {
            if (SetProperty(ref _areaHabitable, value))
            {
                ValidateForm();
            }
        }
    }

    public int? Bedrooms
    {
        get => _bedrooms;
        set
        {
            if (SetProperty(ref _bedrooms, value))
            {
                ValidateForm();
            }
        }
    }

    public decimal? Bathrooms
    {
        get => _bathrooms;
        set
        {
            if (SetProperty(ref _bathrooms, value))
            {
                ValidateForm();
            }
        }
    }

    public decimal? PricePerM2
    {
        get => _pricePerM2;
        set
        {
            if (SetProperty(ref _pricePerM2, value))
            {
                ValidateForm();
            }
        }
    }

    // Optional Properties
    public decimal? AreaTotal
    {
        get => _areaTotal;
        set => SetProperty(ref _areaTotal, value);
    }

    public int Parking
    {
        get => _parking;
        set => SetProperty(ref _parking, value);
    }

    public int? Stratum
    {
        get => _stratum;
        set => SetProperty(ref _stratum, value);
    }

    public int? Floor
    {
        get => _floor;
        set => SetProperty(ref _floor, value);
    }

    public int? ConstructionAge
    {
        get => _constructionAge;
        set => SetProperty(ref _constructionAge, value);
    }

    public decimal? Administration
    {
        get => _administration;
        set => SetProperty(ref _administration, value);
    }

    public bool Terrace
    {
        get => _terrace;
        set => SetProperty(ref _terrace, value);
    }

    public bool Elevator
    {
        get => _elevator;
        set => SetProperty(ref _elevator, value);
    }

    public bool WalkingCloset
    {
        get => _walkingCloset;
        set => SetProperty(ref _walkingCloset, value);
    }

    public bool Loft
    {
        get => _loft;
        set => SetProperty(ref _loft, value);
    }

    public bool StudyRoom
    {
        get => _studyRoom;
        set => SetProperty(ref _studyRoom, value);
    }

    public int Deposit
    {
        get => _deposit;
        set => SetProperty(ref _deposit, value);
    }

    public string? InteriorExterior
    {
        get => _interiorExterior;
        set => SetProperty(ref _interiorExterior, value);
    }

    public int? FinishQuality
    {
        get => _finishQuality;
        set => SetProperty(ref _finishQuality, value);
    }

    public int? ConservationState
    {
        get => _conservationState;
        set => SetProperty(ref _conservationState, value);
    }

    public int? LocationQuality
    {
        get => _locationQuality;
        set => SetProperty(ref _locationQuality, value);
    }

    public string? Observations
    {
        get => _observations;
        set => SetProperty(ref _observations, value);
    }

    // UI State Properties
    public bool IsBusy
    {
        get => _isBusy;
        set
        {
            if (SetProperty(ref _isBusy, value))
            {
                ((RelayCommand)SubmitCommand).RaiseCanExecuteChanged();
            }
        }
    }

    public bool IsFormValid { get; private set; }

    public List<string> ValidationErrors
    {
        get => _validationErrors;
        private set => SetProperty(ref _validationErrors, value);
    }

    // Commands
    public ICommand SubmitCommand { get; }
    public ICommand ClearCommand { get; }

    // Events
    public event EventHandler<PropertyInput>? PropertySubmitted;
    public event EventHandler<AnalysisResult>? AnalysisCompleted;

    // INotifyPropertyChanged implementation
    public event PropertyChangedEventHandler? PropertyChanged;

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

    private void ValidateForm()
    {
        var errors = new List<string>();

        // Required field validation
        if (string.IsNullOrWhiteSpace(Address))
            errors.Add("Address is required");

        if (string.IsNullOrWhiteSpace(Operation) || (Operation != "ARRIENDO" && Operation != "VENTA"))
            errors.Add("Operation must be ARRIENDO or VENTA");

        if (!AreaHabitable.HasValue || AreaHabitable.Value <= 0)
            errors.Add("Area Habitable must be greater than zero");

        if (!Bedrooms.HasValue || Bedrooms.Value < 0)
            errors.Add("Bedrooms must be zero or greater");

        if (!Bathrooms.HasValue || Bathrooms.Value <= 0)
            errors.Add("Bathrooms must be greater than zero");

        if (!PricePerM2.HasValue || PricePerM2.Value <= 0)
            errors.Add("Price per m² must be greater than zero");

        ValidationErrors = errors;
        IsFormValid = errors.Count == 0;
        OnPropertyChanged(nameof(IsFormValid));

        ((RelayCommand)SubmitCommand).RaiseCanExecuteChanged();
    }

    private bool CanExecuteSubmit(object? parameter)
    {
        return IsFormValid && !IsBusy;
    }

    private async Task ExecuteSubmitAsync()
    {
        if (!CanExecuteSubmit(null))
            return;

        try
        {
            IsBusy = true;

            var propertyInput = new PropertyInput(
                address: Address!,
                operation: Operation,
                areaHabitable: AreaHabitable!.Value,
                bedrooms: Bedrooms!.Value,
                bathrooms: Bathrooms!.Value,
                pricePerM2: PricePerM2!.Value,
                areTotal: AreaTotal,
                parking: Parking,
                stratum: Stratum,
                floor: Floor,
                constructionAge: ConstructionAge,
                administration: Administration,
                terrace: Terrace,
                elevator: Elevator,
                walkingCloset: WalkingCloset,
                loft: Loft,
                studyRoom: StudyRoom,
                deposit: Deposit,
                interiorExterior: InteriorExterior,
                finishQuality: FinishQuality,
                conservationState: ConservationState,
                locationQuality: LocationQuality,
                observations: Observations
            );

            // Raise event for legacy support
            PropertySubmitted?.Invoke(this, propertyInput);

            // If orchestrator is available, call it and raise completion event
            if (_orchestrator != null)
            {
                var result = await _orchestrator.GenerateReportAsync(propertyInput, CancellationToken.None);
                AnalysisCompleted?.Invoke(this, result);
            }
        }
        catch (ArgumentException ex)
        {
            ValidationErrors = new List<string> { ex.Message };
            OnPropertyChanged(nameof(ValidationErrors));
        }
        catch (Exception ex)
        {
            ValidationErrors = new List<string> { $"Error generating report: {ex.Message}" };
            OnPropertyChanged(nameof(ValidationErrors));
        }
        finally
        {
            IsBusy = false;
        }
    }

    private void ExecuteClear(object? parameter)
    {
        Address = null;
        Operation = "ARRIENDO";
        AreaHabitable = null;
        Bedrooms = null;
        Bathrooms = null;
        PricePerM2 = null;
        AreaTotal = null;
        Parking = 0;
        Stratum = null;
        Floor = null;
        ConstructionAge = null;
        Administration = null;
        Terrace = false;
        Elevator = false;
        WalkingCloset = false;
        Loft = false;
        StudyRoom = false;
        Deposit = 0;
        InteriorExterior = null;
        FinishQuality = null;
        ConservationState = null;
        LocationQuality = null;
        Observations = null;

        ValidateForm();
    }

    // RelayCommand implementation supporting async operations
    private class RelayCommand : ICommand
    {
        private readonly Func<object?, Task> _executeAsync;
        private readonly Func<object?, bool>? _canExecute;

        public RelayCommand(Action<object?> execute, Func<object?, bool>? canExecute = null)
        {
            if (execute == null) throw new ArgumentNullException(nameof(execute));
            _executeAsync = (param) => { execute(param); return Task.CompletedTask; };
            _canExecute = canExecute;
        }

        public RelayCommand(Func<object?, Task> executeAsync, Func<object?, bool>? canExecute = null)
        {
            _executeAsync = executeAsync ?? throw new ArgumentNullException(nameof(executeAsync));
            _canExecute = canExecute;
        }

        public event EventHandler? CanExecuteChanged;

        public bool CanExecute(object? parameter)
        {
            return _canExecute?.Invoke(parameter) ?? true;
        }

        public async void Execute(object? parameter)
        {
            await _executeAsync(parameter);
        }

        public void RaiseCanExecuteChanged()
        {
            CanExecuteChanged?.Invoke(this, EventArgs.Empty);
        }
    }
}
