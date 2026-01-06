// TDD PHASE: GREEN
// Orchestrator service that coordinates the CMA workflow
// This is a simplified version - no convergence loop yet (that's the Verifier Agent's job)

#nullable enable

using CRM.Application.CmaPlugin.Interfaces;
using CRM.Application.CmaPlugin.Dtos;
using CRM.Domain.ValueObjects;

namespace CRM.Application.CmaPlugin.Services;

/// <summary>
/// Orchestrates the CMA report generation workflow.
/// Coordinates between the UI, agent, and persistence layers.
///
/// MINIMAL IMPLEMENTATION: Direct call to analyzer, no convergence yet.
/// </summary>
public class CmaOrchestrator
{
    private readonly IAnalyzerAgent _analyzerAgent;

    public CmaOrchestrator(IAnalyzerAgent analyzerAgent)
    {
        _analyzerAgent = analyzerAgent ?? throw new ArgumentNullException(nameof(analyzerAgent));
    }

    /// <summary>
    /// Generates a CMA report for the given property input.
    /// </summary>
    /// <param name="propertyInput">The subject property to analyze</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Analysis result containing CSV path</returns>
    /// <exception cref="ArgumentNullException">When propertyInput is null</exception>
    public async Task<AnalysisResult> GenerateReportAsync(
        PropertyInput propertyInput,
        CancellationToken cancellationToken)
    {
        if (propertyInput == null)
            throw new ArgumentNullException(nameof(propertyInput));

        // For minimal implementation, directly call the analyzer agent
        // In the full implementation, this would call the Verifier Agent which
        // would run the Analyzer Agent multiple times until convergence

        var result = await _analyzerAgent.AnalyzeAsync(propertyInput, cancellationToken);

        return result;
    }
}
