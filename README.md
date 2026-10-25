# Next-Generation Software Testing — Systematic Literature Review

A research repository for producing a **systematic literature review
(SLR)** on next-generation software testing techniques (AI-driven,
autonomous, self-healing, LLM-based, and related approaches), structured
for submission to a computer science review/survey journal.

## Repository Structure

```
.
├── paper/                     # LaTeX manuscript (IEEEtran template)
│   ├── main.tex                # Entry point; assembles all sections
│   ├── sections/               # One .tex file per manuscript section
│   ├── figures/                # Generated/static figures (PDF/PNG)
│   ├── tables/                 # Generated/static LaTeX tables
│   └── references.bib          # Central bibliography
├── literature-review/         # SLR protocol & tracking (Kitchenham + PRISMA)
│   ├── search-strategy.md
│   ├── inclusion-exclusion-criteria.md
│   ├── prisma-flow.md
│   ├── data-extraction-form.md
│   ├── reference-set-provenance.md   # How papers-tracking.csv/references.bib were imported
│   ├── papers-tracking.csv     # Master spreadsheet of candidate/included studies
│   ├── search-log.csv
│   └── exclusions-log.csv
├── data/
│   ├── raw/                    # Unmodified exports from databases (CSV/RIS/BibTeX)
│   │   └── reference-list.xlsx # Curated source workbook (see reference-set-provenance.md)
│   └── processed/              # Cleaned/deduplicated datasets
├── scripts/
│   ├── analyze_literature.py   # Generates figures/tables from tracking sheet
│   └── import_reference_list.py # Imports data/raw/reference-list.xlsx into the tracking CSV + references.bib
├── results/
│   ├── figures/                 # Script-generated figures
│   └── tables/                  # Script-generated summary tables
├── docs/
│   ├── research-protocol.md     # Roles, milestones, reproducibility checklist
│   └── timeline.md              # Project schedule
├── requirements.txt            # Python deps for analysis scripts
├── CITATION.cff                # Citation metadata
└── LICENSE                     # MIT (code/tooling); see note on manuscript rights
```

## Getting Started

1. **Finalize the review protocol** in `literature-review/` (search
   strategy, inclusion/exclusion criteria, time window).
2. **Execute searches** across digital libraries; log each run in
   `literature-review/search-log.csv`; export raw results into
   `data/raw/`. A curated starter set of ~113 candidate studies is
   already imported from `data/raw/reference-list.xlsx` — see
   `literature-review/reference-set-provenance.md` for how it was
   produced and re-run `scripts/import_reference_list.py` after
   editing that workbook.
3. **Screen studies** (title/abstract, then full text) and update
   `literature-review/papers-tracking.csv` and `exclusions-log.csv`.
4. **Extract data** per included study using the template in
   `literature-review/data-extraction-form.md`.
5. **Run analysis**:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python scripts\analyze_literature.py
   ```
   This regenerates `results/figures/*.png` and
   `results/tables/summary_stats.csv` from the tracking sheet.
6. **Write the manuscript** by filling in `paper/sections/*.tex`
   (each file has inline guidance comments) and compiling
   `paper/main.tex` with your preferred LaTeX toolchain:
   ```powershell
   cd paper
   pdflatex main.tex
   bibtex main
   pdflatex main.tex
   pdflatex main.tex
   ```
7. **Adapt the template to your target journal.** `paper/main.tex`
   uses the IEEEtran class as a broadly accepted starting point;
   swap the document class/style file to match the specific journal's
   author guidelines (e.g., ACM `acmart`, Elsevier `elsarticle`).

## Reproducibility

All review decisions (search queries, screening outcomes, exclusion
reasons, quality scores) are tracked as plain-text/CSV files under
`literature-review/` so the entire review process is version-controlled
and auditable — see `docs/research-protocol.md` for the full
reproducibility checklist.

## License

Code and tooling (scripts, analysis) are released under the MIT
License (see `LICENSE`). Manuscript text is prepared for journal
submission; confirm the target journal's copyright/open-access policy
before distributing the final accepted version.

## Citation

See `CITATION.cff`.
