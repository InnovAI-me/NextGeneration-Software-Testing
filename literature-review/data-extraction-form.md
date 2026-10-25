# Data Extraction Form

One row per included primary study in `literature-review/papers-tracking.csv`
should be supplemented by a detailed extraction record. For rich,
free-text extraction, create one Markdown file per study under
`literature-review/extractions/S<ID>.md` using the template below.

```markdown
## Study ID: S0XX
- **Title**:
- **Authors**:
- **Year**:
- **Venue**:
- **DOI / URL**:

### Context
- **Problem addressed**:
- **Application domain** (web, mobile, embedded, ML systems, etc.):

### Technique
- **Testing technique category** (unit/integration/system/E2E, GUI,
  API, mutation, fuzzing, model-based, etc.):
- **AI/ML method used** (if any; e.g., LLM, RL, supervised ML,
  symbolic execution, search-based):
- **Automation level per test life-cycle phase**:
  - Test design:
  - Test case / input generation:
  - Test execution:
  - Test oracle / verdict:
  - Test maintenance (e.g., self-healing):

### Evaluation
- **Evaluation method** (case study, controlled experiment,
  benchmark, industrial deployment):
- **Subject systems / benchmarks used**:
- **Key metrics reported** (fault detection rate, coverage,
  precision/recall, time/cost savings):
- **Key quantitative results**:

### Quality Assessment
- Score (per `inclusion-exclusion-criteria.md` checklist):

### Relevance to Research Questions
- RQ1 (taxonomy):
- RQ2 (automation level):
- RQ3 (empirical evidence):
- RQ4 (open challenges identified by this paper):

### Notes / Quotes
-
```

Once extractions are complete, run
`scripts/analyze_literature.py` to regenerate the taxonomy tables and
publication-trend figures from `literature-review/papers-tracking.csv`.
