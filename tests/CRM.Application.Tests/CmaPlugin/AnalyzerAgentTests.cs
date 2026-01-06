// TDD PHASE: RED
// These tests define the contract for IAnalyzerAgent
// We test through a stub implementation to verify the interface contract

using FluentAssertions;
using Xunit;
using CRM.Application.CmaPlugin.Interfaces;
using CRM.Application.CmaPlugin.Dtos;
using CRM.Domain.ValueObjects;

namespace CRM.Application.Tests.CmaPlugin;

public class AnalyzerAgentTests
{
    [Fact]
    public async Task AnalyzeAsync_WithValidPropertyInput_ShouldReturnAnalysisResult()
    {
        // Arrange
        var propertyInput = CreateValidPropertyInput();
        var agent = new StubAnalyzerAgent();

        // Act
        var result = await agent.AnalyzeAsync(propertyInput, CancellationToken.None);

        // Assert
        result.Should().NotBeNull();
        result.CsvFilePath.Should().NotBeNullOrEmpty();
        result.PropertyCount.Should().BeGreaterThanOrEqualTo(0);
        result.GeneratedAt.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(5));
    }

    [Fact]
    public async Task AnalyzeAsync_WithNullInput_ShouldThrowArgumentNullException()
    {
        // Arrange
        var agent = new StubAnalyzerAgent();

        // Act
        var act = async () => await agent.AnalyzeAsync(null!, CancellationToken.None);

        // Assert
        await act.Should().ThrowAsync<ArgumentNullException>();
    }

    [Fact]
    public async Task AnalyzeAsync_WithCancellationToken_ShouldRespectCancellation()
    {
        // Arrange
        var propertyInput = CreateValidPropertyInput();
        var agent = new StubAnalyzerAgent();
        var cts = new CancellationTokenSource();
        cts.Cancel(); // Cancel immediately

        // Act
        var act = async () => await agent.AnalyzeAsync(propertyInput, cts.Token);

        // Assert
        await act.Should().ThrowAsync<OperationCanceledException>();
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

    // Stub implementation for testing the interface contract
    private class StubAnalyzerAgent : IAnalyzerAgent
    {
        public Task<AnalysisResult> AnalyzeAsync(PropertyInput propertyInput, CancellationToken cancellationToken)
        {
            if (propertyInput == null)
                throw new ArgumentNullException(nameof(propertyInput));

            cancellationToken.ThrowIfCancellationRequested();

            // Return a stub result
            var result = new AnalysisResult(
                CsvFilePath: "/tmp/analysis_stub.csv",
                PropertyCount: 5,
                GeneratedAt: DateTime.UtcNow
            );

            return Task.FromResult(result);
        }
    }
}
