# Page Design — Hybrid CSV Analytics App (Desktop-first)

## Global Styles (Design Tokens)
- Layout width: desktop container max-width 1200px; content gutters 24px; section spacing 24–32px.
- Typography: base 14–16px; headings 24/20/16px (H1/H2/H3); monospace for file/ids.
- Colors:
  - Background: #0B1020 (app shell) / #0F172A (cards)
  - Text: #E5E7EB primary, #94A3B8 secondary
  - Accent: #3B82F6 (primary actions), #22C55E (success), #F59E0B (warning), #EF4444 (error)
- Buttons:
  - Primary: solid accent, 40px height, 8px radius; hover darken 5–8%; disabled 50% opacity.
  - Secondary: outline with accent; hover fill 8%.
- Tables:
  - Sticky header on desktop; zebra rows; right-align numeric columns.
- Charts:
  - Card-contained with a 16px internal padding; legend top-right on desktop.

## Responsive Behavior (Desktop-first)
- Desktop (≥1024px): 2-column layout on Dashboard (left: upload+history, right: analytics preview).
- Tablet (768–1023px): collapse to stacked sections; history becomes horizontal scroll list.
- Mobile (<768px): single column; charts become full-width with simplified legends.

---

## Page: Login

### Layout
- Flexbox centered layout: a full-height viewport with a centered card (max 420px).

### Meta Information
- Title: "Sign in — CSV Analytics"
- Description: "Sign in to upload CSV datasets and view analytics."
- Open Graph: title + description; no image required.

### Page Structure
1. App name header
2. Login card
3. Footer help text (small)

### Sections & Components
- Header
  - App name + short tagline.
- Login Card
  - Email input (type=email)
  - Password input (type=password)
  - Primary button: “Sign in”
  - Inline error area (auth errors)
  - Loading state on submit (spinner + disabled fields)
- Session handling
  - If already authenticated, redirect to Dashboard.

---

## Page: Dashboard

### Layout
- Desktop grid (CSS Grid):
  - Left column (380–420px): Upload + Recent history.
  - Right column (auto): Analytics preview.
- Use card-based sections with consistent padding and headers.

### Meta Information
- Title: "Dashboard — CSV Analytics"
- Description: "Upload CSV datasets, browse recent history, and preview summary analytics."
- Open Graph: title + description.

### Page Structure
1. Top app bar
2. Main content grid (left rail + main panel)

### Sections & Components
- Top App Bar
  - Left: App name
  - Center: optional dataset selector (shows current dataset filename)
  - Right: user menu (email) + “Sign out”
- Upload Card
  - Drag-and-drop zone (large)
  - Secondary button: “Choose file”
  - File requirements helper text (CSV only)
  - Progress area:
    - Upload progress bar
    - Processing status (uploaded/processing/ready/error)
    - Error message with retry action
- Recent History Card (Last 5)
  - List of up to 5 items, each row clickable:
    - Filename (truncate)
    - Timestamp
    - Status badge
  - Empty state: “No datasets yet. Upload a CSV to begin.”
- Analytics Preview Panel
  - Header: “Summary analytics” + link button “Open details”
  - Loading skeleton while fetching
  - Chart cards:
    - Primary chart (largest) on top
    - 1–2 smaller charts in a 2-column sub-grid
  - Metrics table:
    - Key-value table for headline numbers

Interaction states:
- Selecting a history item updates the preview panel.
- If dataset status is not ready, preview shows processing message.

---

## Page: Dataset Detail & Report

### Layout
- Desktop stacked layout with anchored header:
  - Header row: breadcrumb + dataset title + actions.
  - Body: tabs or segmented control to switch between “Charts” and “Tables” (still one page route).

### Meta Information
- Title: "Dataset — CSV Analytics"
- Description: "View summary analytics and export a PDF report."
- Open Graph: title + description.

### Page Structure
1. Breadcrumb + title
2. Dataset metadata strip
3. Analytics content (charts/tables)
4. Report actions

### Sections & Components
- Header
  - Breadcrumb: Dashboard / Dataset
  - Dataset title: filename
  - Actions:
    - Primary: “Download PDF report”
    - Secondary: “Back to dashboard”
- Metadata Strip (compact card)
  - Upload time
  - Rows / Columns
  - Status badge
- Analytics Area
  - Segmented control: Charts | Tables
  - Charts view:
    - 2-column grid of chart cards (desktop)
    - Each card has title, chart, and small caption
  - Tables view:
    - One or more tables from summary payload
    - Table toolbar: search within table + copy CSV (optional only if already supported by payload; otherwise omit)
- PDF Report
  - When clicking download:
    - Show modal or inline progress “Generating report…”
    - On success: trigger file download/open
    - On failure: show error with retry

Accessibility notes:
- Ensure upload area and buttons have clear focus rings.
- Provide ARIA labels for chart containers and table controls.
