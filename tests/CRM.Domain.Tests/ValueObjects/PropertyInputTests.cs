// TDD PHASE: RED
// These tests are written FIRST to define the behavior we expect from PropertyInput
// All tests will FAIL initially because PropertyInput doesn't exist yet

using FluentAssertions;
using Xunit;
using CRM.Domain.ValueObjects;

namespace CRM.Domain.Tests.ValueObjects;

public class PropertyInputTests
{
    // Test naming convention: MethodName_Scenario_ExpectedBehavior

    [Fact]
    public void Constructor_WithValidRequiredFields_ShouldCreateInstance()
    {
        // Arrange
        var address = "Calle 123 #45-67, Cedritos, Bogotá";
        var operation = "ARRIENDO";
        var areaHabitable = 45.5m;
        var bedrooms = 2;
        var bathrooms = 1.5m;
        var pricePerM2 = 50000m;

        // Act
        var propertyInput = new PropertyInput(
            address,
            operation,
            areaHabitable,
            bedrooms,
            bathrooms,
            pricePerM2
        );

        // Assert
        propertyInput.Should().NotBeNull();
        propertyInput.Address.Should().Be(address);
        propertyInput.Operation.Should().Be(operation);
        propertyInput.AreaHabitable.Should().Be(areaHabitable);
        propertyInput.Bedrooms.Should().Be(bedrooms);
        propertyInput.Bathrooms.Should().Be(bathrooms);
        propertyInput.PricePerM2.Should().Be(pricePerM2);
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void Constructor_WithInvalidAddress_ShouldThrowArgumentException(string? invalidAddress)
    {
        // Arrange & Act
        var act = () => new PropertyInput(
            invalidAddress!,
            "ARRIENDO",
            45.5m,
            2,
            1.5m,
            50000m
        );

        // Assert
        act.Should().Throw<ArgumentException>()
            .WithParameterName("address");
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("INVALID")]
    public void Constructor_WithInvalidOperation_ShouldThrowArgumentException(string? invalidOperation)
    {
        // Arrange & Act
        var act = () => new PropertyInput(
            "Valid Address",
            invalidOperation!,
            45.5m,
            2,
            1.5m,
            50000m
        );

        // Assert
        act.Should().Throw<ArgumentException>()
            .WithParameterName("operation");
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(-10.5)]
    public void Constructor_WithInvalidAreaHabitable_ShouldThrowArgumentException(decimal invalidArea)
    {
        // Arrange & Act
        var act = () => new PropertyInput(
            "Valid Address",
            "VENTA",
            invalidArea,
            2,
            1.5m,
            50000m
        );

        // Assert
        act.Should().Throw<ArgumentException>()
            .WithParameterName("areaHabitable");
    }

    [Theory]
    [InlineData(-1)]
    [InlineData(-10)]
    public void Constructor_WithNegativeBedrooms_ShouldThrowArgumentException(int invalidBedrooms)
    {
        // Arrange & Act
        var act = () => new PropertyInput(
            "Valid Address",
            "VENTA",
            45.5m,
            invalidBedrooms,
            1.5m,
            50000m
        );

        // Assert
        act.Should().Throw<ArgumentException>()
            .WithParameterName("bedrooms");
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(-0.5)]
    public void Constructor_WithInvalidBathrooms_ShouldThrowArgumentException(decimal invalidBathrooms)
    {
        // Arrange & Act
        var act = () => new PropertyInput(
            "Valid Address",
            "ARRIENDO",
            45.5m,
            2,
            invalidBathrooms,
            50000m
        );

        // Assert
        act.Should().Throw<ArgumentException>()
            .WithParameterName("bathrooms");
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(-50000)]
    public void Constructor_WithInvalidPricePerM2_ShouldThrowArgumentException(decimal invalidPrice)
    {
        // Arrange & Act
        var act = () => new PropertyInput(
            "Valid Address",
            "VENTA",
            45.5m,
            2,
            1.5m,
            invalidPrice
        );

        // Assert
        act.Should().Throw<ArgumentException>()
            .WithParameterName("pricePerM2");
    }

    [Fact]
    public void Constructor_WithOptionalFields_ShouldSetThemCorrectly()
    {
        // Arrange & Act
        var propertyInput = new PropertyInput(
            address: "Valid Address",
            operation: "ARRIENDO",
            areaHabitable: 45.5m,
            bedrooms: 2,
            bathrooms: 1.5m,
            pricePerM2: 50000m,
            areTotal: 50m,
            parking: 1,
            stratum: 3,
            floor: 5,
            constructionAge: 10,
            administration: 150000m,
            terrace: true,
            elevator: true,
            walkingCloset: false,
            loft: false,
            studyRoom: true,
            deposit: 1,
            interiorExterior: "I",
            finishQuality: 4,
            conservationState: 4,
            locationQuality: 5,
            observations: "Nice view"
        );

        // Assert
        propertyInput.AreaTotal.Should().Be(50m);
        propertyInput.Parking.Should().Be(1);
        propertyInput.Stratum.Should().Be(3);
        propertyInput.Floor.Should().Be(5);
        propertyInput.ConstructionAge.Should().Be(10);
        propertyInput.Administration.Should().Be(150000m);
        propertyInput.Terrace.Should().BeTrue();
        propertyInput.Elevator.Should().BeTrue();
        propertyInput.WalkingCloset.Should().BeFalse();
        propertyInput.Loft.Should().BeFalse();
        propertyInput.StudyRoom.Should().BeTrue();
        propertyInput.Deposit.Should().Be(1);
        propertyInput.InteriorExterior.Should().Be("I");
        propertyInput.FinishQuality.Should().Be(4);
        propertyInput.ConservationState.Should().Be(4);
        propertyInput.LocationQuality.Should().Be(5);
        propertyInput.Observations.Should().Be("Nice view");
    }

    [Theory]
    [InlineData(0)]
    [InlineData(7)]
    [InlineData(-1)]
    public void Constructor_WithInvalidStratum_ShouldThrowArgumentException(int invalidStratum)
    {
        // Arrange & Act
        var act = () => new PropertyInput(
            "Valid Address",
            "VENTA",
            45.5m,
            2,
            1.5m,
            50000m,
            stratum: invalidStratum
        );

        // Assert
        act.Should().Throw<ArgumentException>()
            .WithParameterName("stratum");
    }

    [Theory]
    [InlineData("X")]
    [InlineData("INVALID")]
    [InlineData("i")]
    public void Constructor_WithInvalidInteriorExterior_ShouldThrowArgumentException(string? invalidValue)
    {
        // Arrange & Act
        var act = () => new PropertyInput(
            "Valid Address",
            "ARRIENDO",
            45.5m,
            2,
            1.5m,
            50000m,
            interiorExterior: invalidValue
        );

        // Assert
        act.Should().Throw<ArgumentException>()
            .WithParameterName("interiorExterior");
    }

    [Theory]
    [InlineData(0)]
    [InlineData(6)]
    [InlineData(-1)]
    public void Constructor_WithInvalidFinishQuality_ShouldThrowArgumentException(int invalidQuality)
    {
        // Arrange & Act
        var act = () => new PropertyInput(
            "Valid Address",
            "VENTA",
            45.5m,
            2,
            1.5m,
            50000m,
            finishQuality: invalidQuality
        );

        // Assert
        act.Should().Throw<ArgumentException>()
            .WithParameterName("finishQuality");
    }

    [Fact]
    public void PropertyInput_ShouldBeImmutable()
    {
        // This test verifies that PropertyInput is a value object (immutable)
        // We'll use C# records for this, which are immutable by default

        // Arrange
        var input1 = new PropertyInput(
            "Address 1",
            "ARRIENDO",
            45.5m,
            2,
            1.5m,
            50000m
        );

        var input2 = new PropertyInput(
            "Address 1",
            "ARRIENDO",
            45.5m,
            2,
            1.5m,
            50000m
        );

        // Assert - value equality for records
        input1.Should().Be(input2);
        input1.GetHashCode().Should().Be(input2.GetHashCode());
    }
}
