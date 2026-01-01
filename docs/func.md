# Function Refinement Tree

This document decomposes the system from high-level capabilities down to concrete functions.

---

## 1. Application

### 1.1 Initialize Application

* Load configuration
* Initialize local database
* Run migrations
* Load user session

### 1.2 Navigation & Shell

* Render main window
* Sidebar navigation
* Global search

---

## 2. CRM Module

### 2.1 Lead Management

* CreateLead()
* UpdateLead()
* DeleteLead()
* ChangeLeadStatus()
* AssignLeadToAgent()
* SearchLeads()

### 2.2 Contact Management

* CreateContact()
* UpdateContact()
* LinkContactToLead()
* MergeContacts()

### 2.3 Activity Tracking

* LogCall()
* LogEmail()
* LogMeeting()
* AddNote()
* ListActivitiesByEntity()

---

## 3. Property Module

### 3.1 Property Lifecycle

* CreateProperty()
* UpdateProperty()
* DeleteProperty()
* DuplicateProperty()

### 3.2 Custom Fields

* DefineCustomField()
* AttachCustomFieldToPropertyType()
* SerializeCustomFields()
* DeserializeCustomFields()

### 3.3 Attachments

* AddAttachment()
* RemoveAttachment()
* PreviewAttachment()

---

## 4. CMA Module (Core Value)

### 4.1 CMA Lifecycle

* CreateCMA()
* UpdateCMA()
* VersionCMA()
* DeleteCMA()

### 4.2 Comparable Management

* AddComparableProperty()
* RemoveComparableProperty()
* NormalizeComparableData()

### 4.3 Pricing Engine

* CalculatePricePerSqft()
* ApplyAdjustments()
* WeightComparables()
* ComputeAdjustedPrice()
* ComputeValuationRange()

### 4.4 Explainability

* GenerateAdjustmentBreakdown()
* TraceComputationSteps()

---

## 5. Reporting Module

### 5.1 CMA Report Generation

* BuildCMAReportModel()
* RenderComparableTables()
* RenderCharts()
* GeneratePDF()

### 5.2 Export

* ExportCSV()
* ExportPDF()

---

## 6. Persistence Layer

### 6.1 Database

* InitializeSchema()
* RunMigrations()
* ExecuteQuery()

### 6.2 Repositories

* LeadRepository
* ContactRepository
* PropertyRepository
* CMARepository

---

## 7. Infrastructure

### 7.1 Backup & Restore

* ScheduleBackup()
* RunBackup()
* RestoreFromBackup()

### 7.2 Security

* EncryptDatabase()
* DecryptDatabase()
* SecureFileStorage()

---

## 8. Cross-Cutting Concerns

### 8.1 Validation

* ValidateEntity()
* ValidateCustomFields()

### 8.2 Logging

* LogEvent()
* LogError()

### 8.3 Configuration

* LoadSettings()
* UpdateSettings()

---

## 9. Future Extensions

* SyncWithCloud()
* MLSImport()
* AIValuationAssist()
