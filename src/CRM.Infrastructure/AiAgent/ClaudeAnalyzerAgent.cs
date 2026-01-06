// Claude-based implementation of IAnalyzerAgent
// Uses official Anthropic API with the cma-analyzer skill prompt

#nullable enable

using System.Text;
using Anthropic;
using Anthropic.Models.Messages;
using CRM.Application.CmaPlugin.Interfaces;
using CRM.Application.CmaPlugin.Dtos;
using CRM.Domain.ValueObjects;

namespace CRM.Infrastructure.AiAgent;

/// <summary>
/// Implementation of IAnalyzerAgent that calls Claude API with the cma-analyzer skill.
/// Searches real estate portals and returns comparable properties as CSV.
/// </summary>
public class ClaudeAnalyzerAgent : IAnalyzerAgent
{
    private readonly AnthropicClient _client;
    private readonly string _skillPrompt;

    public ClaudeAnalyzerAgent(string? apiKey = null)
    {
        // Use provided key or fall back to environment variable
        var key = apiKey ?? Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY");

        if (string.IsNullOrEmpty(key))
        {
            throw new InvalidOperationException(
                "ANTHROPIC_API_KEY environment variable not set. " +
                "Set it or provide an API key to the constructor.");
        }

        _client = new AnthropicClient { APIKey = key };
        _skillPrompt = LoadSkillPrompt();
    }

    public async Task<AnalysisResult> AnalyzeAsync(PropertyInput propertyInput, CancellationToken cancellationToken)
    {
        if (propertyInput == null)
            throw new ArgumentNullException(nameof(propertyInput));

        cancellationToken.ThrowIfCancellationRequested();

        // Build the user message with property details
        var userMessage = BuildUserMessage(propertyInput);

        // Configure request parameters
        var parameters = new MessageCreateParams
        {
            MaxTokens = 8192,
            Model = "claude-sonnet-4-20250514",
            System = _skillPrompt,
            Messages = new List<MessageParam>
            {
                new MessageParam
                {
                    Role = Role.User,
                    Content = userMessage
                }
            }
        };

        // Call Claude API
        var response = await _client.Messages.Create(parameters, cancellationToken);

        // Extract CSV from response
        var responseText = response.ToString() ?? "";
        var csvContent = ExtractCsvFromResponse(responseText);

        // Save to file
        var timestamp = DateTime.UtcNow.ToString("yyyyMMddHHmmss");
        var csvFilePath = Path.Combine(Path.GetTempPath(), $"cma_claude_{timestamp}.csv");
        await File.WriteAllTextAsync(csvFilePath, csvContent, cancellationToken);

        // Count properties (lines minus header)
        var propertyCount = csvContent.Split('\n', StringSplitOptions.RemoveEmptyEntries).Length - 1;

        return new AnalysisResult(
            CsvFilePath: csvFilePath,
            PropertyCount: Math.Max(0, propertyCount),
            GeneratedAt: DateTime.UtcNow
        );
    }

    private string LoadSkillPrompt()
    {
        // Try to load from file, fall back to embedded prompt
        var skillPath = Path.Combine(
            AppDomain.CurrentDomain.BaseDirectory,
            ".claude", "skills", "cma-analyzer", "SKILL.md");

        if (File.Exists(skillPath))
        {
            return File.ReadAllText(skillPath);
        }

        // Embedded minimal prompt if file not found
        return GetEmbeddedSkillPrompt();
    }

    private string BuildUserMessage(PropertyInput input)
    {
        var sb = new StringBuilder();
        sb.AppendLine("## Subject Property for CMA Analysis");
        sb.AppendLine();
        sb.AppendLine("```json");
        sb.AppendLine("{");
        sb.AppendLine($"  \"address\": \"{input.Address}\",");
        sb.AppendLine($"  \"operation\": \"{input.Operation}\",");
        sb.AppendLine($"  \"area_habitable\": {input.AreaHabitable},");
        sb.AppendLine($"  \"bedrooms\": {input.Bedrooms},");
        sb.AppendLine($"  \"bathrooms\": {input.Bathrooms},");
        sb.AppendLine($"  \"price_per_m2\": {input.PricePerM2}");

        if (input.AreaTotal.HasValue)
            sb.AppendLine($"  ,\"area_total\": {input.AreaTotal.Value}");
        if (input.Stratum.HasValue)
            sb.AppendLine($"  ,\"stratum\": {input.Stratum.Value}");
        if (input.Floor.HasValue)
            sb.AppendLine($"  ,\"floor\": {input.Floor.Value}");
        if (input.ConstructionAge.HasValue)
            sb.AppendLine($"  ,\"construction_age\": {input.ConstructionAge.Value}");
        if (input.Administration.HasValue)
            sb.AppendLine($"  ,\"administration\": {input.Administration.Value}");
        if (!string.IsNullOrEmpty(input.InteriorExterior))
            sb.AppendLine($"  ,\"interior_exterior\": \"{input.InteriorExterior}\"");
        if (!string.IsNullOrEmpty(input.Observations))
            sb.AppendLine($"  ,\"observations\": \"{input.Observations}\"");

        sb.AppendLine("}");
        sb.AppendLine("```");
        sb.AppendLine();
        sb.AppendLine("## Search Parameters");
        sb.AppendLine($"- Area Range: {input.AreaHabitable * 0.8m:F0} - {input.AreaHabitable * 1.2m:F0} m²");
        sb.AppendLine($"- Bedrooms: {Math.Max(0, input.Bedrooms - 1)} - {input.Bedrooms + 1}");
        sb.AppendLine($"- Price/m² Range: {input.PricePerM2 * 0.75m:F0} - {input.PricePerM2 * 1.25m:F0} COP");
        sb.AppendLine();
        sb.AppendLine("Search all Tier 1 portals (Fincaraiz, Metrocuadrado, Ciencuadras, Properati) and return the CSV with comparable properties.");

        return sb.ToString();
    }

    private string ExtractCsvFromResponse(string content)
    {
        // Try to extract CSV from markdown code block
        var csvStart = content.IndexOf("```csv", StringComparison.OrdinalIgnoreCase);
        if (csvStart >= 0)
        {
            csvStart = content.IndexOf('\n', csvStart) + 1;
            var csvEnd = content.IndexOf("```", csvStart);
            if (csvEnd > csvStart)
            {
                return content.Substring(csvStart, csvEnd - csvStart).Trim();
            }
        }

        // Try plain code block
        csvStart = content.IndexOf("```", StringComparison.OrdinalIgnoreCase);
        if (csvStart >= 0)
        {
            csvStart = content.IndexOf('\n', csvStart) + 1;
            var csvEnd = content.IndexOf("```", csvStart);
            if (csvEnd > csvStart)
            {
                return content.Substring(csvStart, csvEnd - csvStart).Trim();
            }
        }

        // If no code block, look for CSV header
        var headerIndex = content.IndexOf("direccion_link,", StringComparison.OrdinalIgnoreCase);
        if (headerIndex >= 0)
        {
            return content.Substring(headerIndex).Trim();
        }

        // Return as-is if nothing found
        return content;
    }

    private string GetEmbeddedSkillPrompt()
    {
        return @"# CMA Analyzer Agent

You are a real estate market analyst specialized in Colombian property markets.
Your task is to find comparable properties for valuation analysis.

## Available Portals
Search these Colombian real estate portals:
1. fincaraiz.com.co
2. metrocuadrado.com
3. ciencuadras.com
4. properati.com.co

## Output Format
Generate a CSV with these columns:
direccion_link,precio,area_habitable,precio_m2_habitable,terraza_area,area_total,precio_m2_total,administracion,admin_por_m2,alcobas,banos,parqueadero,walking_closet,loft,estudio_sala_tv,piso,alcoba_servicio,deposito,terraza_balcon,edad_construccion,interior_exterior,ascensor,calidad_acabados,estado_conservacion,ubicacion,estrato,observaciones,medio_contacto,contacto

## Instructions
1. Search each portal for properties matching the criteria
2. Extract ALL available property attributes
3. CRITICAL: Include the direct URL link to each property listing
4. Note the source portal for each property (F.R.=Fincaraiz, PP=Properati, M2=Metrocuadrado, CC=Ciencuadras)
5. Do NOT filter or deduplicate results

## Quality Requirements
- Minimum 5 properties per search
- Maximum 50 properties total
- All links must be complete URLs
- All required fields must be populated";
    }
}
