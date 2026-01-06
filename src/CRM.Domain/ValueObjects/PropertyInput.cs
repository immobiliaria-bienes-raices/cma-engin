// TDD PHASE: GREEN
// This is the MINIMAL implementation to make all tests pass
// Using C# record for immutability (value object pattern)

#nullable enable

namespace CRM.Domain.ValueObjects;

/// <summary>
/// Value object representing property input data for CMA analysis.
/// Immutable by design - all validation happens in constructor.
/// </summary>
public record PropertyInput
{
    // Required fields
    public string Address { get; init; }
    public string Operation { get; init; }
    public decimal AreaHabitable { get; init; }
    public int Bedrooms { get; init; }
    public decimal Bathrooms { get; init; }
    public decimal PricePerM2 { get; init; }

    // Optional fields with defaults
    public decimal? AreaTotal { get; init; }
    public int Parking { get; init; }
    public int? Stratum { get; init; }
    public int? Floor { get; init; }
    public int? ConstructionAge { get; init; }
    public decimal? Administration { get; init; }
    public bool Terrace { get; init; }
    public bool Elevator { get; init; }
    public bool WalkingCloset { get; init; }
    public bool Loft { get; init; }
    public bool StudyRoom { get; init; }
    public int Deposit { get; init; }
    public string? InteriorExterior { get; init; }
    public int? FinishQuality { get; init; }
    public int? ConservationState { get; init; }
    public int? LocationQuality { get; init; }
    public string? Observations { get; init; }

    /// <summary>
    /// Creates a new PropertyInput with required fields.
    /// All validation is performed in the constructor to ensure invariants.
    /// </summary>
    public PropertyInput(
        string address,
        string operation,
        decimal areaHabitable,
        int bedrooms,
        decimal bathrooms,
        decimal pricePerM2,
        decimal? areTotal = null,
        int parking = 0,
        int? stratum = null,
        int? floor = null,
        int? constructionAge = null,
        decimal? administration = null,
        bool terrace = false,
        bool elevator = false,
        bool walkingCloset = false,
        bool loft = false,
        bool studyRoom = false,
        int deposit = 0,
        string? interiorExterior = null,
        int? finishQuality = null,
        int? conservationState = null,
        int? locationQuality = null,
        string? observations = null)
    {
        // Validate address
        if (string.IsNullOrWhiteSpace(address))
        {
            throw new ArgumentException("Address cannot be null or whitespace.", nameof(address));
        }

        // Validate operation (ARRIENDO or VENTA)
        if (string.IsNullOrWhiteSpace(operation) ||
            (operation != "ARRIENDO" && operation != "VENTA"))
        {
            throw new ArgumentException("Operation must be either 'ARRIENDO' or 'VENTA'.", nameof(operation));
        }

        // Validate area habitable
        if (areaHabitable <= 0)
        {
            throw new ArgumentException("Area habitable must be greater than zero.", nameof(areaHabitable));
        }

        // Validate bedrooms
        if (bedrooms < 0)
        {
            throw new ArgumentException("Bedrooms cannot be negative.", nameof(bedrooms));
        }

        // Validate bathrooms
        if (bathrooms <= 0)
        {
            throw new ArgumentException("Bathrooms must be greater than zero.", nameof(bathrooms));
        }

        // Validate price per m2
        if (pricePerM2 <= 0)
        {
            throw new ArgumentException("Price per m2 must be greater than zero.", nameof(pricePerM2));
        }

        // Validate stratum (1-6 in Colombia)
        if (stratum.HasValue && (stratum.Value < 1 || stratum.Value > 6))
        {
            throw new ArgumentException("Stratum must be between 1 and 6.", nameof(stratum));
        }

        // Validate interior/exterior (I or E)
        if (!string.IsNullOrWhiteSpace(interiorExterior) &&
            interiorExterior != "I" && interiorExterior != "E")
        {
            throw new ArgumentException("Interior/Exterior must be 'I' or 'E'.", nameof(interiorExterior));
        }

        // Validate quality scales (1-5)
        if (finishQuality.HasValue && (finishQuality.Value < 1 || finishQuality.Value > 5))
        {
            throw new ArgumentException("Finish quality must be between 1 and 5.", nameof(finishQuality));
        }

        if (conservationState.HasValue && (conservationState.Value < 1 || conservationState.Value > 5))
        {
            throw new ArgumentException("Conservation state must be between 1 and 5.", nameof(conservationState));
        }

        if (locationQuality.HasValue && (locationQuality.Value < 1 || locationQuality.Value > 5))
        {
            throw new ArgumentException("Location quality must be between 1 and 5.", nameof(locationQuality));
        }

        // Assign validated values
        Address = address;
        Operation = operation;
        AreaHabitable = areaHabitable;
        Bedrooms = bedrooms;
        Bathrooms = bathrooms;
        PricePerM2 = pricePerM2;
        AreaTotal = areTotal;
        Parking = parking;
        Stratum = stratum;
        Floor = floor;
        ConstructionAge = constructionAge;
        Administration = administration;
        Terrace = terrace;
        Elevator = elevator;
        WalkingCloset = walkingCloset;
        Loft = loft;
        StudyRoom = studyRoom;
        Deposit = deposit;
        InteriorExterior = interiorExterior;
        FinishQuality = finishQuality;
        ConservationState = conservationState;
        LocationQuality = locationQuality;
        Observations = observations;
    }
}
