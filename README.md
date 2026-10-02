# Case Lab — money-flow case studies

Static site, no build step.

## Run locally
    python3 -m http.server 8000   # open http://localhost:8000

## Add a case study
1. Copy `cases/_template.json` to `cases/<name>.json` and fill it in.
2. Add the file name to `cases/index.json`.
3. Push to `main`; Render redeploys automatically.

## Evidence tags (required on every party)
- `<span class="tag V">PUBLIC</span>` reported in filings/press
- `<span class="tag U">YOU-STATED</span>` supplied by the author, not verified
- `<span class="tag I">INFERRED</span>` standard industry mechanics
- `<span class="tag X">ILLUSTRATIVE</span>` placeholder value

The Lenskart case is an independent reference model built from public data; it is not an official Lenskart document.
