# CRM - Real Estate CMA Plugin

A .NET 8 WPF application implementing a Comparative Market Analysis (CMA) plugin for real estate professionals, built using Test-Driven Development (TDD) methodology.

## Project Overview

This solution implements a minimal WPF GUI for the CMA Plugin that allows users to:

1. Fill in property details via a WPF form (PropertyFormView)
2. Submit the form to trigger the cma-analyzer agent
3. Receive comparable properties as CSV from the agent
4. Display the CSV results in the UI

## Architecture

The solution follows Clean Architecture principles with clear separation of concerns:

```
/CRM.sln
├── /src
│   ├── /CRM.Domain                  # Domain entities and value objects
│   │   └── /ValueObjects
│   │       └── PropertyInput.cs      # Immutable property input value object
│   │
│   ├── /CRM.Application             # Application logic and interfaces
│   │   └── /CmaPlugin
│   │       ├── /Dtos
│   │       │   └── AnalysisResult.cs
│   │       ├── /Interfaces
│   │       │   └── IAnalyzerAgent.cs
│   │       └── /Services
│   │           └── CmaOrchestrator.cs
│   │
│   ├── /CRM.Infrastructure          # External dependencies
│   │   └── /AiAgent
│   │       └── StubAnalyzerAgent.cs  # Stub implementation for testing
│   │
│   └── /CRM.WPF                     # WPF presentation layer
│       ├── /Views/CmaPlugin
│       │   ├── PropertyFormView.xaml
│       │   ├── PropertyFormView.xaml.cs
│       │   ├── CsvResultsView.xaml
│       │   └── CsvResultsView.xaml.cs
│       └── /ViewModels/CmaPlugin
│           ├── PropertyFormViewModel.cs
│           └── CsvResultsViewModel.cs
│
└── /tests
    ├── /CRM.Domain.Tests
    │   └── /ValueObjects
    │       └── PropertyInputTests.cs
    ├── /CRM.Application.Tests
    │   └── /CmaPlugin
    │       ├── AnalyzerAgentTests.cs
    │       └── CmaOrchestratorTests.cs
    └── /CRM.WPF.Tests
        └── /ViewModels
            └── PropertyFormViewModelTests.cs
```

## TDD Methodology Applied

This project was built using strict Test-Driven Development following the Red-Green-Refactor cycle:

### Component 1: PropertyInput Value Object

**RED Phase** - `/tests/CRM.Domain.Tests/ValueObjects/PropertyInputTests.cs`
- Tests written first defining all validation rules
- Tests for required fields (address, operation, area, bedrooms, bathrooms, price/m²)
- Tests for optional fields and edge cases
- Tests for immutability (value object pattern)

**GREEN Phase** - `/src/CRM.Domain/ValueObjects/PropertyInput.cs`
- Minimal implementation using C# record for immutability
- All validation in constructor to maintain invariants
- Supports nullable reference types

**REFACTOR Phase**
- Code was clean from the start, no refactoring needed

### Component 2: IAnalyzerAgent Interface

**RED Phase** - `/tests/CRM.Application.Tests/CmaPlugin/AnalyzerAgentTests.cs`
- Tests define the contract through a stub implementation
- Tests for async operation with cancellation support
- Tests for null argument validation

**GREEN Phase** - `/src/CRM.Application/CmaPlugin/Interfaces/IAnalyzerAgent.cs`
- Interface definition driven by test requirements
- Stub implementation in Infrastructure layer for testing

### Component 3: PropertyFormViewModel

**RED Phase** - `/tests/CRM.WPF.Tests/ViewModels/PropertyFormViewModelTests.cs`
- Tests for INotifyPropertyChanged behavior
- Tests for command execution and CanExecute logic
- Tests for form validation
- Tests for event raising on submission

**GREEN Phase** - `/src/CRM.WPF/ViewModels/CmaPlugin/PropertyFormViewModel.cs`
- Full MVVM implementation with INotifyPropertyChanged
- RelayCommand implementation for Submit and Clear
- Real-time validation with error collection
- PropertySubmitted event for orchestration

### Component 4: CmaOrchestrator Service

**RED Phase** - `/tests/CRM.Application.Tests/CmaPlugin/CmaOrchestratorTests.cs`
- Tests using Moq for dependency mocking
- Tests for workflow coordination
- Tests for error propagation and cancellation

**GREEN Phase** - `/src/CRM.Application/CmaPlugin/Services/CmaOrchestrator.cs`
- Minimal orchestrator that coordinates the workflow
- Delegates to IAnalyzerAgent
- Note: Full convergence loop (Verifier Agent) not yet implemented

## Property Input Schema

### Required Fields
- **address** (string) - Full property address
- **operation** (enum) - ARRIENDO (rent) or VENTA (sale)
- **area_habitable** (decimal) - Habitable area in m²
- **bedrooms** (integer) - Number of bedrooms
- **bathrooms** (decimal) - Number of bathrooms (supports .5 for half-bath)
- **price_per_m2** (decimal) - Target price per square meter

### Optional Fields
- area_total, parking, stratum (1-6), floor, construction_age
- administration, terrace, elevator, walking_closet, loft, study_room
- deposit, interior_exterior (I/E), finish_quality (1-5)
- conservation_state (1-5), location_quality (1-5), observations

## Building and Running

### Prerequisites
- .NET 8 SDK
- Windows OS (WPF is Windows-only)
- Visual Studio 2022 or Rider (recommended for WPF development)

### Build
```bash
dotnet restore
dotnet build
```

### Run Tests
```bash
dotnet test
```

### Run Application
```bash
cd src/CRM.WPF
dotnet run
```

Or open `CRM.sln` in Visual Studio and press F5.

## Workflow

1. User opens the PropertyFormView
2. User fills in required property details
3. Form validates in real-time
4. User clicks Submit
5. PropertyFormViewModel raises PropertySubmitted event
6. CmaOrchestrator receives the PropertyInput
7. Orchestrator calls IAnalyzerAgent.AnalyzeAsync()
8. StubAnalyzerAgent generates mock CSV data
9. CSV file path is returned
10. CsvResultsView displays the comparable properties

## Testing Philosophy

- **Unit Tests**: All business logic is unit tested in isolation
- **Mocking**: Moq is used to mock dependencies (IAnalyzerAgent)
- **Assertions**: FluentAssertions for readable, expressive assertions
- **Coverage**: Aim for 80%+ coverage on business logic

### Example Test Pattern
```csharp
[Fact]
public void MethodName_Scenario_ExpectedBehavior()
{
    // Arrange - Set up test data and dependencies
    var input = CreateValidInput();

    // Act - Execute the method under test
    var result = systemUnderTest.Method(input);

    // Assert - Verify the outcome
    result.Should().NotBeNull();
    result.Property.Should().Be(expectedValue);
}
```

## Current Limitations (Minimal Implementation)

1. **No Real AI Agent**: Uses `StubAnalyzerAgent` that generates mock data
2. **No Convergence Loop**: Direct call to analyzer, no Verifier Agent yet
3. **No Database Persistence**: Results are not saved to SQLite
4. **No Report Conversion**: CSV only, no XLSX or PDF generation yet
5. **No Portal Integration**: No real portal searching (Tier 1, 2, 3)
6. **No Dependency Injection**: Manual object construction in App.xaml.cs

## Next Steps (Future Implementation)

1. Implement real AI Agent using Claude/OpenAI API
2. Implement Verifier Agent with convergence loop
3. Add database persistence (SQLite)
4. Implement report converters (ClosedXML for XLSX, QuestPDF for PDF)
5. Add portal tier architecture (Tier 1: public, Tier 2: social media, Tier 3: manual)
6. Set up proper dependency injection with Microsoft.Extensions.DependencyInjection
7. Add integration tests
8. Add logging with Serilog

## Design Documents

See `/docs/cma-plugin-design.md` for the complete architecture specification including:
- Convergence-based verification architecture
- Two-agent system (Analyzer + Verifier)
- Portal tier architecture
- Database schema
- Performance targets

## Technology Stack

- **Language**: C# 12
- **Framework**: .NET 8.0
- **UI**: WPF (MVVM pattern)
- **Testing**: xUnit, FluentAssertions, Moq
- **Future**: ClosedXML (Excel), QuestPDF (PDF), SQLite, Serilog

## Quality Gates

Before considering implementation complete:
- [x] All tests pass
- [x] Code follows SOLID principles
- [x] Nullable reference types enabled
- [x] Immutability where appropriate (value objects as records)
- [ ] Code coverage 80%+ (requires test runner)
- [x] No tests testing implementation details
- [x] Edge cases covered

## License

This project is part of the bienes-raices CRM system.

## Contact

For questions about this implementation, refer to the design documents in `/docs/`.
