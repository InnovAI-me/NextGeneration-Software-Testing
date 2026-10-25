# Research Protocol

## Title (working)
Next-Generation Software Testing: A Systematic Literature Review

## Target Venue
Computer science **review/survey journal** (e.g., ACM Computing
Surveys, IEEE Access, Journal of Systems and Software, Information and
Software Technology, or a dedicated "Software Testing, Verification
and Reliability" venue). Confirm target journal before formatting
the manuscript, since citation style and length limits vary
(`paper/main.tex` currently uses the IEEEtran class as a widely
accepted starting point — swap the document class/template to match
the chosen journal's author guidelines).

## Research Team Roles
| Role | Responsibility |
|---|---|
| Lead author | Protocol design, manuscript writing, final synthesis |
| Reviewer 1 | Independent screening, quality assessment |
| Reviewer 2 | Independent screening, quality assessment, conflict resolution |
| Data analyst | Runs `scripts/analyze_literature.py`, maintains figures/tables |

## Milestones
1. **Protocol finalization** — lock search strategy & IC/EC
   (`literature-review/search-strategy.md`,
   `literature-review/inclusion-exclusion-criteria.md`).
2. **Search execution** — run searches, log in
   `literature-review/search-log.csv`.
3. **Screening** — title/abstract and full-text screening,
   `literature-review/papers-tracking.csv` updated.
4. **Data extraction** — one file per study in
   `literature-review/extractions/`.
5. **Synthesis & analysis** — run `scripts/analyze_literature.py`;
   populate `paper/sections/05_results.tex`.
6. **Manuscript drafting** — complete all `paper/sections/*.tex`.
7. **Internal review** — co-authors review draft against target
   journal's author guidelines.
8. **Submission** — export PDF, prepare cover letter, submit.
9. **Revision** — address reviewer comments; track in
   `docs/revision-log.md` (create when revisions begin).

## Reproducibility Checklist
- [ ] Search strings and dates logged (`search-log.csv`)
- [ ] IC/EC applied consistently and documented
- [ ] Dual-reviewer screening with agreement metric recorded
- [ ] PRISMA counts match manuscript Section III numbers
- [ ] All data extraction records archived
- [ ] Analysis scripts re-run from a clean environment before submission
- [ ] Bibliography entries verified against publisher metadata
