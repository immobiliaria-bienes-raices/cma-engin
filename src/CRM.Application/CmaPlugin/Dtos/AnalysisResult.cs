#nullable enable

namespace CRM.Application.CmaPlugin.Dtos;

/// <summary>
/// Result from a single analyzer agent execution.
/// Contains the CSV file path with comparable properties.
/// </summary>
public record AnalysisResult(
    string CsvFilePath,
    int PropertyCount,
    DateTime GeneratedAt
);
