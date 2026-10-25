# Search Strategy

Defines the reproducible search protocol for the systematic literature
review (SLR) on **Next-Generation Software Testing**.

## Research Questions
See `paper/sections/01_introduction.tex` for the full RQ list (RQ1–RQ4).

## Digital Libraries / Databases
- IEEE Xplore
- ACM Digital Library
- Scopus
- Web of Science
- (Optional, with caution for quality) Google Scholar / arXiv for preprints

## Time Window
`[START_YEAR]` – `[END_YEAR]` (update once the protocol is finalized).

## Search String (template)
Combine population, intervention, and context terms with Boolean operators.
Adapt syntax per database (e.g., Scopus uses `TITLE-ABS-KEY(...)`).

```
("software testing" OR "test automation" OR "test generation")
AND
("artificial intelligence" OR "machine learning" OR "deep learning"
 OR "large language model" OR "LLM" OR "reinforcement learning"
 OR "autonomous" OR "self-healing")
AND
("next generation" OR "intelligent" OR "AI-driven" OR "AI-augmented")
```

## Example Per-Database Queries
| Database | Query Field | Notes |
|---|---|---|
| IEEE Xplore | `("Document Title":... OR "Abstract":...)` | Limit to Journals + Conferences |
| ACM DL | `Title:(...) OR Abstract:(...)` | Use ACM Guide to Computing Literature |
| Scopus | `TITLE-ABS-KEY(...)` | Limit to Subject Area: Computer Science |
| Web of Science | `TS=(...)` | Limit to Document Types: Article, Proceedings Paper |

## Snowballing
Perform one round of backward snowballing (references of included
studies) and forward snowballing (citing papers via Google Scholar/
Semantic Scholar) on the final included set, per
Wohlin (2014) guidelines.

## Search Execution Log
Record each database run in `literature-review/search-log.csv`
(database, query string, date executed, number of hits, executed by).
