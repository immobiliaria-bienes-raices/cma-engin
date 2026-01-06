using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using CRM.Application.CmaPlugin.Services;
using CRM.Application.CmaPlugin.Interfaces;
using CRM.Infrastructure.AiAgent;
using CRM.WPF.ViewModels.CmaPlugin;
using CRM.WPF.Views.CmaPlugin;

namespace CRM.WPF;

/// <summary>
/// Interaction logic for App.xaml
/// </summary>
public partial class App : System.Windows.Application
{
    private ServiceProvider? _serviceProvider;

    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        // Configure dependency injection
        var services = new ServiceCollection();

        // Register application services
        services.AddSingleton<IAnalyzerAgent, StubAnalyzerAgent>();
        services.AddSingleton<CmaOrchestrator>();

        // Register ViewModels
        services.AddTransient<PropertyFormViewModel>();
        services.AddTransient<CsvResultsViewModel>();

        // Register Views
        services.AddTransient<PropertyFormView>();
        services.AddTransient<CsvResultsView>();

        _serviceProvider = services.BuildServiceProvider();

        // Create and show the main window with DI
        var mainWindow = _serviceProvider.GetRequiredService<PropertyFormView>();
        var viewModel = _serviceProvider.GetRequiredService<PropertyFormViewModel>();
        mainWindow.DataContext = viewModel;
        mainWindow.Show();
    }

    protected override void OnExit(ExitEventArgs e)
    {
        _serviceProvider?.Dispose();
        base.OnExit(e);
    }
}
