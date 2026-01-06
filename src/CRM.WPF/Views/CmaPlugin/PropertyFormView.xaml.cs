using System.Windows;
using CRM.WPF.ViewModels.CmaPlugin;

namespace CRM.WPF.Views.CmaPlugin;

/// <summary>
/// Interaction logic for PropertyFormView.xaml
/// Code-behind is kept minimal - all logic is in the ViewModel
/// </summary>
public partial class PropertyFormView : Window
{
    public PropertyFormView()
    {
        InitializeComponent();

        // Wire up navigation when analysis is completed
        if (DataContext is PropertyFormViewModel viewModel)
        {
            viewModel.AnalysisCompleted += OnAnalysisCompleted;
        }

        // Handle DataContext changes (for DI scenarios)
        DataContextChanged += (s, e) =>
        {
            if (e.OldValue is PropertyFormViewModel oldVm)
            {
                oldVm.AnalysisCompleted -= OnAnalysisCompleted;
            }

            if (e.NewValue is PropertyFormViewModel newVm)
            {
                newVm.AnalysisCompleted += OnAnalysisCompleted;
            }
        };
    }

    private void OnAnalysisCompleted(object? sender, Application.CmaPlugin.Dtos.AnalysisResult result)
    {
        // Get the subject property address from the ViewModel
        var viewModel = DataContext as PropertyFormViewModel;
        var subjectAddress = viewModel?.Address ?? "Unknown";
        var operation = viewModel?.Operation ?? "Unknown";

        // Create and show the results view
        var resultsView = new CsvResultsView();
        var resultsViewModel = new CsvResultsViewModel();

        resultsViewModel.LoadCsvData(result.CsvFilePath, subjectAddress, operation);
        resultsView.DataContext = resultsViewModel;

        // Wire up close event
        resultsViewModel.CloseRequested += (s, e) => resultsView.Close();

        resultsView.Show();
    }
}
