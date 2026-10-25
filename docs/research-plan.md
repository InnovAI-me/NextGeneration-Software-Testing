# Research Plan

**Title:** The Next Generation of Software Testing: A Critical Review
of Agentic AI, Self-Adaptive Test Frameworks, and Autonomous Quality
Engineering

**Type:** Systematic Literature Review (SLR), Kitchenham/PRISMA-aligned
**Target outlet:** Computer science review/survey journal (e.g., ACM
Computing Surveys, IEEE Access, Information and Software Technology,
Software Testing Verification and Reliability — confirm before final
formatting; see `docs/research-protocol.md`)
**Status date:** 2026-10-25

This plan operationalizes the protocol in `docs/research-protocol.md`
into concrete phases, current status, and next actions, reflecting
work already completed in this repository.

---

## 1. Motivation & Scope

Traditional software testing (manual design, coverage-driven unit
tests, scripted regression) is increasingly augmented or replaced by
**agentic AI** (LLM-driven autonomous agents that plan, act, and
self-correct), **self-adaptive test frameworks** (locators/oracles/test
suites that repair themselves at runtime), and broader **autonomous
quality engineering** (end-to-end AI ownership of test design,
execution, triage, and maintenance). The literature is fragmented
across inconsistent terminology, evaluation benchmarks, and maturity
levels. This review consolidates that literature into a single
classification framework with reproducible screening.

## 2. Research Questions

(Canonical source: `paper/sections/01_introduction.tex` — keep both
in sync when revised.)

- **RQ1 (Landscape/Taxonomy):** What agentic-AI, self-adaptive, and
  autonomous testing techniques have been proposed, and how can they
  be classified across the test life cycle (design → generation →
  execution → oracle → maintenance/triage)?
- **RQ2 (Autonomy level):** What degree of autonomy do these
  techniques achieve (human-in-the-loop assist vs. fully autonomous
  agentic operation), and via what architectures (single-agent,
  multi-agent, tool-augmented LLM)?
- **RQ3 (Empirical evidence):** What effectiveness, efficiency, and
  industrial-adoption evidence exists (benchmarks, case studies,
  practitioner studies), and how rigorous/reproducible is it (data
  contamination, benchmark leakage, generalizability)?
- **RQ4 (Risks & open problems):** What risks (security of coding/
  testing agents, trust/acceptance, hallucination, flaky/self-healing
  failure modes) and open research gaps remain for next-generation,
  autonomous quality engineering?

## 3. Methodology Summary

Full protocol detail lives in `literature-review/search-strategy.md`,
`literature-review/inclusion-exclusion-criteria.md`,
`literature-review/prisma-flow.md`, and
`literature-review/data-extraction-form.md`. Summary:

1. **Search** — IEEE Xplore, ACM DL, Scopus, Web of Science, plus
   arXiv/Google Scholar for preprints; one round of backward/forward
   snowballing (Wohlin 2014).
2. **Seed set** — a curated 113-study starter corpus was imported from
   a reference workbook into `literature-review/papers-tracking.csv`
   (see `literature-review/reference-set-provenance.md`) to bootstrap
   screening and taxonomy design; full database searches per §3.1 of
   the protocol still need to be executed and logged to confirm
   saturation/completeness.
3. **Screening** — title/abstract, then full-text, against
   `literature-review/inclusion-exclusion-criteria.md`; dual-reviewer
   with conflict resolution; counts recorded in
   `literature-review/prisma-flow.md`.
4. **Full-text acquisition** — `scripts/fetch_full_papers.py`
   automates PDF retrieval (arXiv/direct link/landing-page scraping),
   Markdown extraction, and an abstract-only fallback (with a
   title-keyword-overlap guard against false positives) when full
   text is unreachable. Downloaded content stays local/gitignored
   (`data/papers/`) for copyright reasons; only the fetch manifest
   (`data/papers/fetch-log.csv`) and tracking-sheet status columns are
   committed.
5. **Data extraction** — per-study form in
   `literature-review/data-extraction-form.md`.
6. **Synthesis** — `scripts/analyze_literature.py` generates summary
   figures/tables from the tracking sheet into `results/`.
7. **Manuscript** — `paper/main.tex` (IEEEtran) with one `.tex` file
   per section under `paper/sections/`.

## 4. Current Status (as of this plan)

| Metric | Value |
|---|---|
| Candidate studies in tracking sheet | 113 |
| Full text successfully retrieved (new + pre-existing) | 99 (67 new + 32 already present) |
| Abstract-only fallback (full text unreachable, abstract verified) | 3 |
| Unresolved (paywalled/blocked/no content found) | 11 — require manual institutional access |
| Emerging taxonomy categories (from `category` column) | 18 (see §5) |

Remaining gap vs. a complete SLR: the 113-study set is a **curated
starter corpus**, not yet the product of the systematic multi-database
search in `literature-review/search-strategy.md`. Treat current
progress as advanced **pilot screening / taxonomy development**, not
a finished review — Phase 1 below closes this gap.

## 5. Emerging Taxonomy (from current tracking data)

Preliminary clusters observed in `papers-tracking.csv`, to be refined
during full-text synthesis (RQ1):

1. Surveys and literature reviews (10)
2. Unit test generation with LLMs (8)
3. CI failure triage and flaky-test classification (8)
4. GUI, mobile and web testing agents (6)
5. Human factors: trust and acceptance (6)
6. Industrial case studies (5)
7. Multi-agent and agentic test generation (4)
8. Test oracles and assertions (4)
9. Self-adaptive systems and runtime testing (4)
10. Benchmarks and data contamination (4)
11. Mobile GUI agents (4)
12. Security of coding and testing agents (4)
13. Agentic software engineering foundations (3)
14. Bug reproduction and test-based issue validation (3)
15. API testing (3)
16. LLM-based fuzzing (3)
17. Flaky tests and self-healing tests (3)
18. Mutation testing with LLMs (2)
19. Original/general reference-list carryover items pending re-categorization (29)

## 6. Phased Plan & Timeline

Fill in actual calendar dates in `docs/timeline.md` once the team
commits to a schedule; durations below are effort estimates (not
calendar weeks) for a 1–2 person review team.

| Phase | Key actions | Primary artifacts | Est. effort |
|---|---|---|---|
| **0. Protocol lock-in** (done) | Finalize title, RQs, IC/EC, taxonomy skeleton | `docs/research-protocol.md`, `literature-review/inclusion-exclusion-criteria.md` | — |
| **1. Systematic search** | Execute and log searches across IEEE/ACM/Scopus/WoS per `search-strategy.md`; merge with existing 113-study seed set; dedupe | `literature-review/search-log.csv` | 1–2 wks |
| **2. Screening** | Title/abstract screen all hits against IC/EC; resolve the 11 unresolved full texts via institutional access or exclude with reason | `papers-tracking.csv`, `exclusions-log.csv`, `prisma-flow.md` | 1–2 wks |
| **3. Full-text acquisition** | Re-run `fetch_full_papers.py --limit N` on newly added studies; manual retrieval for paywalled items | `data/papers/` (local), `fetch-log.csv` | ongoing/automatable |
| **4. Data extraction** | Populate one extraction record per included study (technique, autonomy level, evaluation method, metrics, threats) | `literature-review/data-extraction-form.md` instances | 2–3 wks |
| **5. Synthesis & taxonomy finalization** | Refine §5 taxonomy against RQ1–RQ2; run `analyze_literature.py` for figures/tables | `results/figures/`, `results/tables/` | 1–2 wks |
| **6. Manuscript drafting** | Write `paper/sections/02_background.tex` through `08_conclusion.tex`; cite via `paper/references.bib` | `paper/main.tex` (compiled PDF) | 2–3 wks |
| **7. Internal review** | Co-author/advisor review against target journal author guidelines; adapt LaTeX class if needed | reviewed draft | 1 wk |
| **8. Submission** | Finalize cover letter, format checks, submit | submission package | — |
| **9. Revision** | Address reviewer comments | `docs/revision-log.md` (create at this stage) | per journal timeline |

## 7. Immediate Next Actions

1. Execute and log the first systematic database search (Phase 1) to
   validate/extend the 113-study seed set — do not rely on the
   curated list alone as the final corpus.
2. Resolve or formally exclude (with reason in `exclusions-log.csv`)
   the 11 studies still unresolved for full text (paywalled/blocked).
3. Begin per-study data extraction for the ~32 "must-read" priority
   studies that already have full text, to start populating
   `paper/sections/05_results.tex` early.
4. Update `docs/timeline.md` with real target dates once the team and
   target journal are confirmed.

## 8. Reproducibility

Every step above is backed by a plain-text/CSV artifact under
`literature-review/` or `data/`, so the review is fully auditable and
re-runnable (see `docs/research-protocol.md` → Reproducibility
Checklist).
