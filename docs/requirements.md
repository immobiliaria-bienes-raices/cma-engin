# Real Estate CRM Desktop App (Windows)

## 1. Overview

A Windows-native desktop CRM application for real estate professionals, built using .NET, focused on lead management, property listings, and first-class Comparative Market Analysis (CMA). The system is offline-first with optional cloud synchronization.

## 2. Goals

* Provide a fast, native Windows experience
* Integrate CRM and CMA workflows seamlessly
* Support customizable property data models
* Enable transparent, explainable pricing analysis

## 3. Target Users

* Independent real estate agents
* Small brokerages (1–20 agents)

## 4. Functional Requirements

### 4.1 User & Agent Management

* Create and manage agent profiles
* Assign leads, properties, and CMA reports to agents
* Role support (Admin, Agent) [post-MVP]

### 4.2 CRM Core

* Lead creation, editing, deletion
* Lead status pipeline (configurable stages)
* Contact management (buyers, sellers, investors)
* Activity tracking (calls, emails, meetings, notes)
* Search and filtering across leads and contacts

### 4.3 Property & Listing Management

* Create and edit properties
* Support multiple property types
* Standard attributes (beds, baths, sqft, etc.)
* Custom fields per property type (stored as JSON)
* Attachments (images, PDFs)

### 4.4 Comparative Market Analysis (CMA)

* Create CMA linked to a subject property
* Add/remove comparable properties
* Compute price per square foot
* Manual and rule-based adjustments
* Generate valuation range
* Persist CMA versions

### 4.5 Reporting

* Generate CMA PDF reports
* Export property and lead data (CSV, PDF)
* Printable summaries

### 4.6 Data Import / Export

* CSV import for contacts, leads, properties
* CSV export for backup and interoperability

### 4.7 Offline & Persistence

* Local SQLite database
* Automatic local backups
* Data encryption at rest

## 5. Non-Functional Requirements

### 5.1 Performance

* App startup < 3 seconds
* CMA recalculation < 500ms for <50 comps

### 5.2 Usability

* Keyboard-first navigation
* Minimal modal dialogs
* Consistent Windows UI conventions

### 5.3 Security

* Local database encryption
* Secure storage of credentials
* Audit log for critical edits [post-MVP]

### 5.4 Maintainability

* MVVM architecture
* Strong domain separation
* Unit-testable CMA logic

## 6. Technology Stack

* Language: C#
* Framework: .NET 8
* UI: WPF or WinUI 3
* Database: SQLite
* PDF: QuestPDF or PdfSharp

## 7. Out of Scope (MVP)

* MLS live API integration
* AI-based valuation
* Mobile applications

## 8. Success Criteria

* Agents can complete a full CMA end-to-end
* Leads and properties persist reliably offline
* CMA reports are client-ready without external tools
