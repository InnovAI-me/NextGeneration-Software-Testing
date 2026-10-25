# Reference Set Provenance

The initial candidate reference set in `papers-tracking.csv` was
imported from a curated Excel reference list
(`data/raw/reference-list.xlsx`) compiled during exploratory scoping
searches, using `scripts/import_reference_list.py`. That workbook
contains two complementary sheets:

- **Sheet1** — an early working checklist (IDs such as `G1`, `P2`,
  `HF6`) with author names and a "Verify" status column, organized
  under numbered topical headings (e.g., "6. GUI, mobile and web
  testing agents").
- **Sheet2** — a more complete, link-verified pass over the same
  topical headings plus an additional "Original list (29 papers)"
  section, with publication year, venue, URL, and a short
  **research-gap** note per study (the gap each paper leaves open,
  useful directly for Sections IV–VI of the manuscript).

The importer merges the two sheets (author names from Sheet1 onto the
corresponding Sheet2 record, matched by topical category and row
order) and writes:

- `literature-review/papers-tracking.csv` — one row per candidate
  study, including category, year, venue, URL, arXiv ID (parsed from
  the URL where available), research-gap note, and link-check status.
- `paper/references.bib` — an auto-generated BibTeX block (between
  `% --- BEGIN/END IMPORTED REFERENCES ---` markers) with one entry
  per study. Re-run the importer after updating the source workbook;
  it regenerates that block in place without touching manually curated
  entries above the marker.

**All imported studies default to `decision_title_abstract = include`
and an empty `decision_full_text`.** This reflects the fact that the
source workbook already represents a curated candidate set from
targeted scoping searches, not yet a dual-reviewer full-text screening
pass — apply the criteria in `inclusion-exclusion-criteria.md` and
record the full-text decision explicitly before relying on these
records as final included studies.

To refresh the import after editing the source workbook:

```powershell
python scripts\import_reference_list.py
```

Many "Original list (29 papers)" rows point to very recent
(2025–2026) arXiv preprints and a few grey-literature/industry
sources (ResearchGate uploads, vendor blog posts, theses) explicitly
flagged with link-check notes (e.g., `Blocked (403)`, `title differs`)
in the `link_check` column — verify venue, peer-review status, and
final title/DOI for each before citing them in the manuscript.
