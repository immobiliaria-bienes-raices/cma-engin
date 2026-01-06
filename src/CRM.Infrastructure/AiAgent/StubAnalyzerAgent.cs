// TDD PHASE: GREEN
// Stub implementation for testing and initial development
// This will be replaced with the real AI agent implementation later

#nullable enable

using CRM.Application.CmaPlugin.Interfaces;
using CRM.Application.CmaPlugin.Dtos;
using CRM.Domain.ValueObjects;

namespace CRM.Infrastructure.AiAgent;

/// <summary>
/// Stub implementation of IAnalyzerAgent for testing purposes.
/// Returns mock data in CSV format.
///
/// TODO: Replace with real AI agent that calls LLM API and searches portals.
/// </summary>
public class StubAnalyzerAgent : IAnalyzerAgent
{
    private static readonly string[] MockAddresses = new[]
    {
        "Calle 100 #15-20, Cedritos, Bogotá",
        "Carrera 9 #120-30, Usaquén, Bogotá",
        "Calle 140 #9-25, Cedritos, Bogotá",
        "Carrera 7 #125-45, Usaquén, Bogotá",
        "Calle 127 #7A-10, Cedritos, Bogotá"
    };

    public async Task<AnalysisResult> AnalyzeAsync(PropertyInput propertyInput, CancellationToken cancellationToken)
    {
        if (propertyInput == null)
            throw new ArgumentNullException(nameof(propertyInput));

        cancellationToken.ThrowIfCancellationRequested();

        // Simulate async work
        await Task.Delay(100, cancellationToken);

        // Generate a unique filename
        var timestamp = DateTime.UtcNow.ToString("yyyyMMddHHmmss");
        var csvFilePath = Path.Combine(Path.GetTempPath(), $"cma_analysis_{timestamp}.csv");

        // Generate mock CSV data with properties similar to the input
        var csvContent = GenerateMockCsvData(propertyInput);

        // Write to file
        await File.WriteAllTextAsync(csvFilePath, csvContent, cancellationToken);

        return new AnalysisResult(
            CsvFilePath: csvFilePath,
            PropertyCount: 5,
            GeneratedAt: DateTime.UtcNow
        );
    }

    private string GenerateMockCsvData(PropertyInput input)
    {
        var csv = new System.Text.StringBuilder();

        // CSV header matching the schema
        csv.AppendLine("source_portal,property_link,address,operation,area_habitable,area_total,bedrooms,bathrooms,parking,stratum,floor,price_per_m2,total_price,administration,terrace,elevator,construction_age,observations");

        // Generate 5 mock comparable properties with variations
        var random = new Random();
        for (int i = 0; i < 5; i++)
        {
            var areaVariation = input.AreaHabitable * (decimal)(0.8 + random.NextDouble() * 0.4); // ±20%
            var priceVariation = input.PricePerM2 * (decimal)(0.85 + random.NextDouble() * 0.3); // ±15%
            var totalPrice = areaVariation * priceVariation;

            csv.AppendLine($"fincaraiz.com.co,https://fincaraiz.com.co/mock/{i + 1},{MockAddresses[i]},{input.Operation},{areaVariation:F2},{areaVariation * 1.1m:F2},{input.Bedrooms + (random.Next(3) - 1)},{input.Bathrooms},{random.Next(2)},{input.Stratum ?? 3},{random.Next(1, 10)},{priceVariation:F0},{totalPrice:F0},{random.Next(100000, 300000)},{random.Next(2) == 1},{random.Next(2) == 1},{random.Next(0, 20)},Good condition");
        }

        return csv.ToString();
    }
}
