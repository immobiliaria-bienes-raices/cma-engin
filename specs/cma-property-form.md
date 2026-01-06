# CMA Property Form Component

**Component Name**: CMA Property Form
**Version**: 1.0
**Status**: Implemented

---

## 1. Overview

The CMA Property Form component provides a WPF user interface for inputting property data to trigger a Comparative Market Analysis. It follows MVVM pattern and integrates with the CMA Analyzer Agent to fetch comparable properties.

---

## 2. State Transition Table (STT)

| Current State | Event/Trigger | Next State | Action |
|---------------|---------------|------------|--------|
| **Idle** | User opens form | **Editing** | Display empty form with defaults |
| **Editing** | User types in field | **Editing** | Validate field, update ValidationErrors |
| **Editing** | User fills all required fields | **Valid** | Enable Submit button |
| **Valid** | User clears a required field | **Editing** | Disable Submit button |
| **Valid** | User clicks Submit | **Processing** | Create PropertyInput, call CmaOrchestrator |
| **Processing** | Analysis completes | **Results** | Show CsvResultsView with data |
| **Processing** | Analysis fails | **Error** | Show error message, return to Valid |
| **Processing** | User cancels | **Valid** | Cancel operation, re-enable form |
| **Results** | User clicks Close | **Idle** | Close results, optionally return to form |
| **Any** | User clicks Clear | **Editing** | Reset all fields to defaults |

### State Diagram

```
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    ▼                                         │
    ┌───────┐   open form   ┌─────────┐   all valid   ┌──────┴──┐
    │ Idle  │──────────────▶│ Editing │──────────────▶│  Valid  │
    └───────┘               └────┬────┘               └────┬────┘
        ▲                        │                         │
        │                        │ clear required          │ submit
        │                        ▼                         ▼
        │                   ┌─────────┐              ┌───────────┐
        │                   │ Editing │◀─────────────│Processing │
        │                   └─────────┘    cancel    └─────┬─────┘
        │                                                  │
        │                                                  │ success
        │         close                                    ▼
        └──────────────────────────────────────────┌───────────┐
                                                   │  Results  │
                                                   └───────────┘
```

---

## 3. Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DOMAIN LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────┐                                           │
│  │      PropertyInput          │  (Value Object - Immutable)               │
│  ├─────────────────────────────┤                                           │
│  │ + Address: string           │                                           │
│  │ + Operation: string         │  ◄── "ARRIENDO" | "VENTA"                 │
│  │ + AreaHabitable: decimal    │                                           │
│  │ + Bedrooms: int             │                                           │
│  │ + Bathrooms: decimal        │                                           │
│  │ + PricePerM2: decimal       │                                           │
│  │ + AreaTotal: decimal?       │                                           │
│  │ + Parking: int              │                                           │
│  │ + Stratum: int?             │  ◄── 1-6                                  │
│  │ + Floor: int?               │                                           │
│  │ + ConstructionAge: int?     │                                           │
│  │ + Administration: decimal?  │                                           │
│  │ + Terrace: bool             │                                           │
│  │ + Elevator: bool            │                                           │
│  │ + WalkingCloset: bool       │                                           │
│  │ + Loft: bool                │                                           │
│  │ + StudyRoom: bool           │                                           │
│  │ + Deposit: int              │                                           │
│  │ + InteriorExterior: string? │  ◄── "I" | "E"                            │
│  │ + FinishQuality: int?       │  ◄── 1-5                                  │
│  │ + ConservationState: int?   │  ◄── 1-5                                  │
│  │ + LocationQuality: int?     │  ◄── 1-5                                  │
│  │ + Observations: string?     │                                           │
│  └─────────────────────────────┘                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────┐       ┌─────────────────────────────┐     │
│  │    <<interface>>            │       │      AnalysisResult         │     │
│  │    IAnalyzerAgent           │       │        (Record)             │     │
│  ├─────────────────────────────┤       ├─────────────────────────────┤     │
│  │ + AnalyzeAsync(             │       │ + CsvFilePath: string       │     │
│  │     PropertyInput,          │──────▶│ + PropertyCount: int        │     │
│  │     CancellationToken)      │       │ + GeneratedAt: DateTime     │     │
│  │   : Task<AnalysisResult>    │       └─────────────────────────────┘     │
│  └──────────────┬──────────────┘                                           │
│                 │                                                           │
│                 │ uses                                                      │
│                 ▼                                                           │
│  ┌─────────────────────────────┐                                           │
│  │      CmaOrchestrator        │                                           │
│  ├─────────────────────────────┤                                           │
│  │ - _analyzerAgent            │                                           │
│  ├─────────────────────────────┤                                           │
│  │ + GenerateReportAsync(      │                                           │
│  │     PropertyInput,          │                                           │
│  │     CancellationToken)      │                                           │
│  │   : Task<AnalysisResult>    │                                           │
│  └─────────────────────────────┘                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          INFRASTRUCTURE LAYER                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────┐                                           │
│  │    StubAnalyzerAgent        │  implements IAnalyzerAgent                │
│  ├─────────────────────────────┤                                           │
│  │ + AnalyzeAsync(...)         │  Returns mock CSV data                    │
│  │ - GenerateMockCsvData(...)  │                                           │
│  └─────────────────────────────┘                                           │
│                                                                             │
│  (Future: McpAnalyzerAgent using MCP C# SDK)                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          PRESENTATION LAYER (WPF)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────┐       ┌─────────────────────────────┐     │
│  │  PropertyFormViewModel      │       │   CsvResultsViewModel       │     │
│  ├─────────────────────────────┤       ├─────────────────────────────┤     │
│  │ + Address: string?          │       │ + CsvFilePath: string       │     │
│  │ + Operation: string         │       │ + SubjectAddress: string    │     │
│  │ + AreaHabitable: decimal?   │       │ + Operation: string         │     │
│  │ + Bedrooms: int?            │       │ + PropertyCount: int        │     │
│  │ + Bathrooms: decimal?       │       │ + GeneratedAt: DateTime     │     │
│  │ + PricePerM2: decimal?      │       │ + Properties: Observable    │     │
│  │ + ... (all fields)          │       ├─────────────────────────────┤     │
│  │ + IsBusy: bool              │       │ + LoadCsvData(...)          │     │
│  │ + IsFormValid: bool         │       │ + OpenCsvCommand            │     │
│  │ + ValidationErrors: List    │       │ + CloseCommand              │     │
│  ├─────────────────────────────┤       └─────────────────────────────┘     │
│  │ + SubmitCommand             │                    ▲                      │
│  │ + ClearCommand              │                    │                      │
│  │ + PropertySubmitted: Event  │────────────────────┘                      │
│  └──────────────┬──────────────┘       navigates to                        │
│                 │                                                           │
│                 │ binds to                                                  │
│                 ▼                                                           │
│  ┌─────────────────────────────┐       ┌─────────────────────────────┐     │
│  │    PropertyFormView.xaml    │       │    CsvResultsView.xaml      │     │
│  ├─────────────────────────────┤       ├─────────────────────────────┤     │
│  │ - Required Fields Section   │       │ - Summary Header            │     │
│  │ - Optional Fields Section   │       │ - DataGrid (auto-columns)   │     │
│  │ - Observations TextBox      │       │ - Open CSV Button           │     │
│  │ - Validation Errors List    │       │ - Close Button              │     │
│  │ - Submit/Clear Buttons      │       └─────────────────────────────┘     │
│  │ - Busy Indicator Overlay    │                                           │
│  └─────────────────────────────┘                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Dependencies

```
CRM.WPF
  ├── CRM.Domain (PropertyInput)
  ├── CRM.Application (IAnalyzerAgent, CmaOrchestrator, AnalysisResult)
  └── CRM.Infrastructure (StubAnalyzerAgent)

Packages Used:
  - Microsoft.Extensions.DependencyInjection (8.0.0)
  - (Future) ModelContextProtocol for MCP integration
```

---

## 5. Data Flow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           USER INTERACTION FLOW                          │
└──────────────────────────────────────────────────────────────────────────┘

    User                    PropertyFormView          ViewModel           Agent
     │                            │                      │                  │
     │  1. Fill form fields       │                      │                  │
     │ ──────────────────────────▶│                      │                  │
     │                            │  2. Data binding     │                  │
     │                            │─────────────────────▶│                  │
     │                            │                      │                  │
     │                            │  3. Validate         │                  │
     │                            │◀─────────────────────│                  │
     │  4. See validation errors  │                      │                  │
     │ ◀──────────────────────────│                      │                  │
     │                            │                      │                  │
     │  5. Click Submit           │                      │                  │
     │ ──────────────────────────▶│                      │                  │
     │                            │  6. Execute command  │                  │
     │                            │─────────────────────▶│                  │
     │                            │                      │                  │
     │                            │                      │  7. AnalyzeAsync │
     │                            │                      │─────────────────▶│
     │                            │                      │                  │
     │                            │                      │  8. CSV result   │
     │                            │                      │◀─────────────────│
     │                            │                      │                  │
     │                            │  9. Open Results     │                  │
     │                            │◀─────────────────────│                  │
     │                            │                      │                  │
     │  10. View comparable       │                      │                  │
     │      properties in grid    │                      │                  │
     │ ◀──────────────────────────│                      │                  │
     │                            │                      │                  │
```

---

## 6. How to Test from UI

### Prerequisites
1. .NET 8 SDK installed
2. Windows OS (WPF requires Windows)

### Steps to Run

```bash
# Navigate to project
cd /home/jmsbpp/work/bienes-raices/crm

# Build the solution
dotnet build

# Run the WPF application
dotnet run --project src/CRM.WPF
```

### Test Scenarios

| # | Scenario | Steps | Expected Result |
|---|----------|-------|-----------------|
| 1 | **Empty form validation** | Open app, click Submit | Submit disabled, validation errors shown |
| 2 | **Fill required fields** | Enter: Address, Operation, Area, Bedrooms, Bathrooms, Price | Submit button enables |
| 3 | **Submit and get results** | Fill form, click Submit | Progress shown, then CsvResultsView opens with DataGrid |
| 4 | **View CSV file** | In results view, click "Open CSV File" | Default CSV app opens with file |
| 5 | **Clear form** | Fill some fields, click Clear | All fields reset to defaults |
| 6 | **Invalid stratum** | Enter Stratum = 7 | Validation error (must be 1-6) |

### Sample Test Data

```
Address:        Carrera 15 #100-25, Cedritos, Bogotá
Operation:      ARRIENDO
Area Habitable: 45
Bedrooms:       1
Bathrooms:      1
Price per m²:   45000
Stratum:        4
```

---

## 7. File Inventory

| File | Purpose |
|------|---------|
| `src/CRM.Domain/ValueObjects/PropertyInput.cs` | Immutable value object with validation |
| `src/CRM.Application/CmaPlugin/Interfaces/IAnalyzerAgent.cs` | Agent interface contract |
| `src/CRM.Application/CmaPlugin/Dtos/AnalysisResult.cs` | Analysis result record |
| `src/CRM.Application/CmaPlugin/Services/CmaOrchestrator.cs` | Orchestrates analysis workflow |
| `src/CRM.Infrastructure/AiAgent/StubAnalyzerAgent.cs` | Mock implementation for testing |
| `src/CRM.WPF/ViewModels/CmaPlugin/PropertyFormViewModel.cs` | Form ViewModel with commands |
| `src/CRM.WPF/ViewModels/CmaPlugin/CsvResultsViewModel.cs` | Results display ViewModel |
| `src/CRM.WPF/Views/CmaPlugin/PropertyFormView.xaml` | Property input form UI |
| `src/CRM.WPF/Views/CmaPlugin/CsvResultsView.xaml` | Results DataGrid UI |
| `tests/CRM.Domain.Tests/ValueObjects/PropertyInputTests.cs` | PropertyInput unit tests |
| `tests/CRM.Application.Tests/CmaPlugin/AnalyzerAgentTests.cs` | Agent tests |
| `tests/CRM.Application.Tests/CmaPlugin/CmaOrchestratorTests.cs` | Orchestrator tests |
| `tests/CRM.WPF.Tests/ViewModels/PropertyFormViewModelTests.cs` | ViewModel tests |
