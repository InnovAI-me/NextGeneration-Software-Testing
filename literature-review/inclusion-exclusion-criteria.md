# Inclusion and Exclusion Criteria

## Inclusion Criteria (IC)
- **IC1**: Peer-reviewed journal articles, conference papers, or
  workshop papers.
- **IC2**: Published between `[START_YEAR]` and `[END_YEAR]`.
- **IC3**: Primarily addresses software testing techniques involving
  AI/ML, autonomy, or automation beyond traditional scripted testing.
- **IC4**: Written in English.
- **IC5**: Reports an identifiable technique, tool, framework, or
  empirical study (not purely an opinion/vision piece), **unless**
  the paper is a highly cited vision/roadmap paper relevant to RQ4.

## Exclusion Criteria (EC)
- **EC1**: Duplicate publications (retain the most complete version,
  e.g., prefer journal extension over conference version).
- **EC2**: Non-peer-reviewed sources (blog posts, white papers),
  except where explicitly scoped as industry grey literature in a
  secondary multivocal review.
- **EC3**: Papers with fewer than 4 pages (extended abstracts, posters).
- **EC4**: Papers not available in full text after reasonable
  retrieval effort (document in `literature-review/exclusions-log.csv`).
- **EC5**: Papers focused solely on hardware testing or non-software
  domains.
- **EC6**: Secondary studies (other surveys/SLRs) are tracked
  separately for Section "Related Work," not counted as primary
  studies.

## Screening Process
1. **Title/Abstract screening** — two reviewers independently apply
   IC/EC; disagreements resolved by discussion or a third reviewer.
2. **Full-text screening** — same dual-reviewer process on the
   remaining candidate set.
3. Record inter-rater agreement (e.g., Cohen's kappa) in
   `literature-review/screening-agreement.md`.

## Quality Assessment Checklist (per included study)
Score each item 0 (no), 0.5 (partially), or 1 (yes):
1. Are the research objectives clearly stated?
2. Is the study design appropriate for the objectives?
3. Is the evaluation/validation methodology clearly described?
4. Are threats to validity discussed?
5. Are results clearly reported and linked to objectives?

Studies scoring below a defined threshold (e.g., 2.5/5) may be
flagged as lower-confidence evidence but are typically still included
with that caveat noted in the data extraction sheet.
