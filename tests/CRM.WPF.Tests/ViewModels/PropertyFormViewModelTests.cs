// TDD PHASE: RED
// These tests define the behavior we expect from PropertyFormViewModel
// Follows MVVM pattern with INotifyPropertyChanged and ICommand

using FluentAssertions;
using Xunit;
using CRM.WPF.ViewModels.CmaPlugin;
using System.ComponentModel;

namespace CRM.WPF.Tests.ViewModels;

public class PropertyFormViewModelTests
{
    [Fact]
    public void Constructor_ShouldInitializePropertiesWithDefaults()
    {
        // Arrange & Act
        var viewModel = new PropertyFormViewModel();

        // Assert
        viewModel.Should().NotBeNull();
        viewModel.Address.Should().BeNull();
        viewModel.Operation.Should().Be("ARRIENDO"); // Default to rent
        viewModel.AreaHabitable.Should().BeNull();
        viewModel.Bedrooms.Should().BeNull();
        viewModel.Bathrooms.Should().BeNull();
        viewModel.PricePerM2.Should().BeNull();
        viewModel.IsFormValid.Should().BeFalse();
    }

    [Fact]
    public void PropertyChange_ShouldRaisePropertyChangedEvent()
    {
        // Arrange
        var viewModel = new PropertyFormViewModel();
        var propertyChangedRaised = false;
        var propertyName = string.Empty;

        viewModel.PropertyChanged += (sender, args) =>
        {
            propertyChangedRaised = true;
            propertyName = args.PropertyName;
        };

        // Act
        viewModel.Address = "Test Address";

        // Assert
        propertyChangedRaised.Should().BeTrue();
        propertyName.Should().Be(nameof(PropertyFormViewModel.Address));
    }

    [Fact]
    public void SubmitCommand_WhenFormIsInvalid_ShouldNotExecute()
    {
        // Arrange
        var viewModel = new PropertyFormViewModel();
        // Leave required fields empty

        // Act & Assert
        viewModel.SubmitCommand.CanExecute(null).Should().BeFalse();
    }

    [Fact]
    public void SubmitCommand_WhenFormIsValid_ShouldExecute()
    {
        // Arrange
        var viewModel = new PropertyFormViewModel
        {
            Address = "Calle 123 #45-67",
            Operation = "ARRIENDO",
            AreaHabitable = 45.5m,
            Bedrooms = 2,
            Bathrooms = 1.5m,
            PricePerM2 = 50000m
        };

        // Act & Assert
        viewModel.SubmitCommand.CanExecute(null).Should().BeTrue();
    }

    [Fact]
    public void ValidateForm_WithAllRequiredFields_ShouldSetIsFormValidToTrue()
    {
        // Arrange
        var viewModel = new PropertyFormViewModel();

        // Act
        viewModel.Address = "Calle 123 #45-67";
        viewModel.Operation = "VENTA";
        viewModel.AreaHabitable = 45.5m;
        viewModel.Bedrooms = 2;
        viewModel.Bathrooms = 1.5m;
        viewModel.PricePerM2 = 50000m;

        // Assert
        viewModel.IsFormValid.Should().BeTrue();
        viewModel.ValidationErrors.Should().BeEmpty();
    }

    [Fact]
    public void ValidateForm_WithMissingRequiredFields_ShouldSetIsFormValidToFalse()
    {
        // Arrange
        var viewModel = new PropertyFormViewModel();

        // Act
        viewModel.Address = "Calle 123 #45-67";
        // Missing other required fields

        // Assert
        viewModel.IsFormValid.Should().BeFalse();
        viewModel.ValidationErrors.Should().NotBeEmpty();
    }

    [Fact]
    public void SubmitCommand_Execute_ShouldRaiseSubmittedEvent()
    {
        // Arrange
        var viewModel = new PropertyFormViewModel
        {
            Address = "Calle 123 #45-67",
            Operation = "ARRIENDO",
            AreaHabitable = 45.5m,
            Bedrooms = 2,
            Bathrooms = 1.5m,
            PricePerM2 = 50000m
        };

        var eventRaised = false;
        viewModel.PropertySubmitted += (sender, propertyInput) =>
        {
            eventRaised = true;
            propertyInput.Should().NotBeNull();
            propertyInput.Address.Should().Be("Calle 123 #45-67");
        };

        // Act
        viewModel.SubmitCommand.Execute(null);

        // Assert
        eventRaised.Should().BeTrue();
    }

    [Fact]
    public void ClearCommand_ShouldResetAllFields()
    {
        // Arrange
        var viewModel = new PropertyFormViewModel
        {
            Address = "Calle 123 #45-67",
            Operation = "VENTA",
            AreaHabitable = 45.5m,
            Bedrooms = 2,
            Bathrooms = 1.5m,
            PricePerM2 = 50000m
        };

        // Act
        viewModel.ClearCommand.Execute(null);

        // Assert
        viewModel.Address.Should().BeNull();
        viewModel.AreaHabitable.Should().BeNull();
        viewModel.Bedrooms.Should().BeNull();
        viewModel.Bathrooms.Should().BeNull();
        viewModel.PricePerM2.Should().BeNull();
        viewModel.IsFormValid.Should().BeFalse();
    }

    [Theory]
    [InlineData("ARRIENDO")]
    [InlineData("VENTA")]
    public void Operation_ShouldOnlyAcceptValidValues(string operation)
    {
        // Arrange
        var viewModel = new PropertyFormViewModel();

        // Act
        viewModel.Operation = operation;

        // Assert
        viewModel.Operation.Should().Be(operation);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public void AreaHabitable_WithInvalidValue_ShouldAddValidationError(decimal invalidArea)
    {
        // Arrange
        var viewModel = new PropertyFormViewModel
        {
            Address = "Valid Address",
            Operation = "ARRIENDO",
            Bedrooms = 2,
            Bathrooms = 1.5m,
            PricePerM2 = 50000m
        };

        // Act
        viewModel.AreaHabitable = invalidArea;

        // Assert
        viewModel.IsFormValid.Should().BeFalse();
        viewModel.ValidationErrors.Should().Contain(e => e.Contains("Area"));
    }

    [Fact]
    public void IsBusy_WhenSubmitting_ShouldPreventMultipleSubmissions()
    {
        // Arrange
        var viewModel = new PropertyFormViewModel
        {
            Address = "Calle 123 #45-67",
            Operation = "ARRIENDO",
            AreaHabitable = 45.5m,
            Bedrooms = 2,
            Bathrooms = 1.5m,
            PricePerM2 = 50000m
        };

        // Act
        viewModel.IsBusy = true;

        // Assert
        viewModel.SubmitCommand.CanExecute(null).Should().BeFalse();
    }
}
