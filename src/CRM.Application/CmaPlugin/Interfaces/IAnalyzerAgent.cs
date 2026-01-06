// TDD PHASE: GREEN
// Interface definition driven by the test requirements

#nullable enable

using CRM.Application.CmaPlugin.Dtos;
using CRM.Domain.ValueObjects;

namespace CRM.Application.CmaPlugin.Interfaces;

/// <summary>
/// Interface for the Analyzer Agent that searches real estate portals
/// and returns comparable properties as CSV.
///
/// This is the "inner agent" in the convergence architecture.
/// Each invocation should be stateless and independent.
/// </summary>
public interface IAnalyzerAgent
{
    /// <summary>
    /// Analyzes the property market for comparables based on the input criteria.
    /// </summary>
    /// <param name="propertyInput">The subject property to find comparables for</param>
    /// <param name="cancellationToken">Cancellation token to abort the operation</param>
    /// <returns>Analysis result containing path to CSV file with comparables</returns>
    /// <exception cref="ArgumentNullException">When propertyInput is null</exception>
    /// <exception cref="OperationCanceledException">When operation is cancelled</exception>
    Task<AnalysisResult> AnalyzeAsync(PropertyInput propertyInput, CancellationToken cancellationToken);
}
