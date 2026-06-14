# HostelHub - Premium Smart Hostel & Property Management System

HostelHub is an enterprise-grade, single-file property and hostel management system built using Python Flask, Tailwind CSS, and embedded interactive JS analytics.

## Features
- **Smart Room Floor Plans**: Interactive layout maps for 90 rooms grouped by building blocks (A, B, C) and floors (Ground, 1st, 2nd) with real-time bed occupancy stats.
- **Occupancy Heat Map**: Visual block grid colored dynamically by room allocation status (Vacant, Partial, Full, Maintenance).
- **Bed Allocations & Transfers**: In-app modals to assign new residents to vacant beds or transfer existing occupants between rooms.
- **Interactive Tenant Directory**: Dynamic table with instant search and status filters (Paid, Pending, Partial, Checked Out).
- **Financial Analytics & Ledger**: Real-time revenue utilization charts, collection progress trackers, and receivable balance logs.
- **SaaS Branding & Customization**: Dynamic currency settings, property name configurations, and database resets.

## Installation & Startup

To run HostelHub locally, run directly with Python:

```bash
python hostelhub.py
```

*Note: The application will automatically check for and install Flask using pip if it is not present on your system.*

Access the interactive dashboard in your browser at:
`http://127.0.0.1:5000`
