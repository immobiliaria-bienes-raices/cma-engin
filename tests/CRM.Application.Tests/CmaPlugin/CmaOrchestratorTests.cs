// TDD PHASE: RED
// Tests for the orchestrator that coordinates the entire CMA workflow

using FluentAssertions;
using Xunit;
using Moq;
using CRM.Application.CmaPlugin.Services;
using CRM.Application.CmaPlugin.Interfaces;
using CRM.Application.CmaPlugin.Dtos;
using CRM.Domain.ValueObjects;

namespace CRM.Application.Tests.CmaPlugin;

public class CmaOrchestratorTests
{
    private readonly Mock<IAnalyzerAgent> _mockAnalyzerAgent;
    private readonly CmaOrchestrator _orchestrator;

    public CmaOrchestratorTests()
    {
        _mockAnalyzerAgent = new Mock<IAnalyzerAgent>();
        _orchestrator = new CmaOrchestrator(_mockAnalyzerAgent.Object);
    }

    [Fact]
    public async Task GenerateReportAsync_WithValidInput_ShouldCallAnalyzerAndReturnResult()
    {
        // Arrange
        var propertyInput = CreateValidPropertyInput();
        var expectedResult = new AnalysisResult(
            CsvFilePath: "/tmp/test.csv",
            PropertyCount: 5,
            GeneratedAt: DateTime.UtcNow
        );

        _mockAnalyzerAgent
            .Setup(a => a.AnalyzeAsync(propertyInput, It.IsAny<CancellationToken>()))
            .ReturnsAsync(expectedResult);

        // Act
        var result = await _orchestrator.GenerateReportAsync(propertyInput, CancellationToken.None);

        // Assert
        result.Should().NotBeNull();
        result.CsvFilePath.Should().Be(expectedResult.CsvFilePath);
        result.PropertyCount.Should().Be(5);

        _mockAnalyzerAgent.Verify(
            a => a.AnalyzeAsync(propertyInput, It.IsAny<CancellationToken>()),
            Times.Once
        );
    }

    [Fact]
    public async Task GenerateReportAsync_WithNullInput_ShouldThrowArgumentNullException()
    {
        // Arrange & Act
        var act = async () => await _orchestrator.GenerateReportAsync(null!, CancellationToken.None);

        // Assert
        await act.Should().ThrowAsync<ArgumentNullException>();
    }

    [Fact]
    public async Task GenerateReportAsync_WhenAnalyzerFails_ShouldPropagateException()
    {
        // Arrange
        var propertyInput = CreateValidPropertyInput();

        _mockAnalyzerAgent
            .Setup(a => a.AnalyzeAsync(It.IsAny<PropertyInput>(), It.IsAny<CancellationToken>()))
            .ThrowsAsync(new InvalidOperationException("Agent failed"));

        // Act
        var act = async () => await _orchestrator.GenerateReportAsync(propertyInput, CancellationToken.None);

        // Assert
        await act.Should().ThrowAsync<InvalidOperationException>()
            .WithMessage("Agent failed");
    }

    [Fact]
    public async Task GenerateReportAsync_WhenCancelled_ShouldRespectCancellation()
    {
        // Arrange
        var propertyInput = CreateValidPropertyInput();
        var cts = new CancellationTokenSource();
        cts.Cancel();

        _mockAnalyzerAgent
            .Setup(a => a.AnalyzeAsync(It.IsAny<PropertyInput>(), It.IsAny<CancellationToken>()))
            .ThrowsAsync(new OperationCanceledException());

        // Act
        var act = async () => await _orchestrator.GenerateReportAsync(propertyInput, cts.Token);

        // Assert
        await act.Should().ThrowAsync<OperationCanceledException>();
    }

    [Fact]
    public async Task GenerateReportAsync_ShouldReturnResultWithTimestamp()
    {
        // Arrange
        var propertyInput = CreateValidPropertyInput();
        var beforeCall = DateTime.UtcNow;

        _mockAnalyzerAgent
            .Setup(a => a.AnalyzeAsync(It.IsAny<PropertyInput>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new AnalysisResult("/tmp/test.csv", 5, DateTime.UtcNow));

        // Act
        var result = await _orchestrator.GenerateReportAsync(propertyInput, CancellationToken.None);

        // Assert
        result.GeneratedAt.Should().BeOnOrAfter(beforeCall);
        result.GeneratedAt.Should().BeOnOrBefore(DateTime.UtcNow);
    }

    [Fact]
    public async Task GenerateReportAsync_ShouldValidateCsvFileExists()
    {
        // Arrange
        var propertyInput = CreateValidPropertyInput();
        var csvPath = Path.Combine(Path.GetTempPath(), $"test_{Guid.NewGuid()}.csv");

        // Create a temporary CSV file
        await File.WriteAllTextAsync(csvPath, "test,data\n1,2");

        _mockAnalyzerAgent
            .Setup(a => a.AnalyzeAsync(It.IsAny<PropertyInput>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new AnalysisResult(csvPath, 5, DateTime.UtcNow));

        try
        {
            // Act
            var result = await _orchestrator.GenerateReportAsync(propertyInput, CancellationToken.None);

            // Assert
            result.CsvFilePath.Should().Be(csvPath);
            File.Exists(result.CsvFilePath).Should().BeTrue();
        }
        finally
        {
            // Cleanup
            if (File.Exists(csvPath))
                File.Delete(csvPath);
        }
    }

    private static PropertyInput CreateValidPropertyInput()
    {
        return new PropertyInput(
            address: "Calle 123 #45-67, Cedritos, Bogotá",
            operation: "ARRIENDO",
            areaHabitable: 45.5m,
            bedrooms: 2,
            bathrooms: 1.5m,
            pricePerM2: 50000m
        );
    }
}
